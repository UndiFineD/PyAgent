# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-guardian-cli\tools\masscan.py
"""
Masscan tool wrapper for ultra-fast TCP port scanning
"""

import json
import re
from typing import Any, Dict, List

from tools.base_tool import BaseTool


class MasscanTool(BaseTool):
    """Masscan ultra-fast port scanner wrapper"""

    def __init__(self, config):
        super().__init__(config)
        self.tool_name = "masscan"

    def get_command(self, target: str, **kwargs) -> List[str]:
        """Build masscan command"""
        config = self.config.get("tools", {}).get("masscan", {})
        safe_mode = self.config.get("pentest", {}).get("safe_mode", True)

        command = ["masscan"]

        # Target
        command.append(target)

        # Ports
        ports = kwargs.get("ports", config.get("ports", "1-1000"))
        command.extend(["-p", ports])

        # Output format - JSON
        command.extend(["-oJ", "-"])  # Output to stdout

        # Rate limiting (packets per second)
        if safe_mode:
            # Conservative rate for safe mode
            rate = config.get("safe_rate", 100)
        else:
            rate = kwargs.get("rate", config.get("rate", 1000))
        command.extend(["--rate", str(rate)])

        # Banners (grab service banners)
        if kwargs.get("banners", config.get("banners", False)):
            command.append("--banners")

        # Exclude targets (for safety)
        exclude = config.get("exclude", [])
        if exclude:
            for exc in exclude:
                command.extend(["--exclude", exc])

        # Wait time (how long to wait for responses)
        wait = config.get("wait", 10)
        command.extend(["--wait", str(wait)])

        # Interface (if specified)
        if "interface" in kwargs:
            command.extend(["-e", kwargs["interface"]])

        # Source port
        if "source_port" in kwargs:
            command.extend(["--source-port", str(kwargs["source_port"])])

        return command

    def parse_output(self, output: str) -> Dict[str, Any]:
        """Parse masscan JSON output"""
        results = {
            "open_ports": [],
            "hosts": {},
            "banners": {},
            "total_hosts": 0,
            "total_ports": 0,
        }

        # Masscan outputs JSON lines, but not as a single JSON array
        # Each line is a JSON object
        for line in output.strip().split("\n"):
            if not line or line.strip() == "[" or line.strip() == "]":
                continue

            # Remove trailing comma if present
            line = line.rstrip(",").strip()

            try:
                data = json.loads(line)

                # Extract port information
                if "ports" in data:
                    ip = data.get("ip", "")

                    if ip not in results["hosts"]:
                        results["hosts"][ip] = []
                        results["total_hosts"] += 1

                    for port_info in data["ports"]:
                        port = port_info.get("port", 0)
                        protocol = port_info.get("proto", "tcp")
                        status = port_info.get("status", "open")

                        port_data = {
                            "port": port,
                            "protocol": protocol,
                            "status": status,
                        }

                        # Banner information
                        if "service" in port_info:
                            service = port_info["service"]
                            port_data["service"] = service.get("name", "")
                            port_data["banner"] = service.get("banner", "")

                            results["banners"][f"{ip}:{port}"] = service.get(
                                "banner", ""
                            )

                        results["hosts"][ip].append(port_data)

                        if port not in results["open_ports"]:
                            results["open_ports"].append(port)
                            results["total_ports"] += 1

            except json.JSONDecodeError:
                continue

        # Sort open ports
        results["open_ports"].sort()

        return results
