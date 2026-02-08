# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-guardian-cli\tools\nmap.py
"""
Nmap tool wrapper for port scanning and service detection
"""

import json
import re
from typing import Any, Dict, List

from tools.base_tool import BaseTool


class NmapTool(BaseTool):
    """Nmap port scanner wrapper"""

    def get_command(self, target: str, **kwargs) -> List[str]:
        """Build nmap command"""
        config = self.config.get("tools", {}).get("nmap", {})

        # Base command
        command = ["nmap"]

        # Add default args from config
        default_args = config.get("default_args", "-sV -sC")
        if default_args:
            command.extend(default_args.split())

        # Timing template
        timing = config.get("timing", "T4")
        command.append(f"-{timing}")

        # XML output for parsing
        command.extend(["-oX", "-"])

        # Custom args from kwargs
        if "ports" in kwargs:
            command.extend(["-p", kwargs["ports"]])

        if "scan_type" in kwargs:
            command.append(kwargs["scan_type"])

        # Target
        command.append(target)

        return command

    def parse_output(self, output: str) -> Dict[str, Any]:
        """Parse nmap XML output"""
        results = {
            "open_ports": [],
            "services": [],
            "os_detection": None,
            "vulnerabilities": [],
        }

        # Simple regex parsing (in production, use proper XML parser)
        # Extract open ports
        port_pattern = r'portid="(\d+)".*?service name="([^"]*)".*?product="([^"]*)"'
        for match in re.finditer(port_pattern, output, re.DOTALL):
            port = match.group(1)
            service = match.group(2)
            product = match.group(3) if match.group(3) else "unknown"

            results["open_ports"].append(int(port))
            results["services"].append({"port": int(port), "service": service, "product": product})

        # Extract OS if available
        os_match = re.search(r'osclass type="([^"]*)".*?osfamily="([^"]*)"', output)
        if os_match:
            results["os_detection"] = {
                "type": os_match.group(1),
                "family": os_match.group(2),
            }

        return results
