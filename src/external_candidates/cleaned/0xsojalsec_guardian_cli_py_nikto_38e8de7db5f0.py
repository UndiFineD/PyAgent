# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_guardian_cli.py\tools.py\nikto_38e8de7db5f0.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-guardian-cli\tools\nikto.py

"""

Nikto tool wrapper for web vulnerability scanning

"""

import re

from typing import Any, Dict, List

from tools.base_tool import BaseTool


class NiktoTool(BaseTool):
    """Nikto web vulnerability scanner wrapper"""

    def __init__(self, config):
        super().__init__(config)

        self.tool_name = "nikto"

    def get_command(self, target: str, **kwargs) -> List[str]:
        """Build nikto command"""

        command = ["nikto"]

        # Host

        command.extend(["-h", target])

        # Output format

        command.extend(["-Format", "txt"])

        # SSL

        if target.startswith("https"):
            command.append("-ssl")

        # Tuning options

        tuning = kwargs.get("tuning", "x")  # Default: all tests except DoS

        command.extend(["-Tuning", tuning])

        # Timeout

        timeout = kwargs.get("timeout", 10)

        command.extend(["-timeout", str(timeout)])

        # No interactive mode

        command.append("-nointeractive")

        return command

    def parse_output(self, output: str) -> Dict[str, Any]:
        """Parse nikto text output"""

        results = {
            "vulnerabilities": [],
            "server_info": {},
            "findings_count": 0,
            "target": "",
            "scan_duration": None,
        }

        vulnerabilities = []

        for line in output.split("\n"):
            line = line.strip()

            # Extract target

            if "+ Target:" in line:
                results["target"] = line.split("Target:")[-1].strip()

            # Extract server info

            elif "+ Server:" in line:
                results["server_info"]["server"] = line.split("Server:")[-1].strip()

            # Extract findings (lines starting with +)

            elif line.startswith("+") and line != "+":
                # Skip informational lines

                if any(skip in line.lower() for skip in ["target ip:", "start time:", "end time:"]):
                    continue

                # Determine severity based on keywords

                severity = "info"

                if any(keyword in line.lower() for keyword in ["vulnerability", "exploit", "vulnerable"]):
                    severity = "high"

                elif any(keyword in line.lower() for keyword in ["security", "risk", "disclosure"]):
                    severity = "medium"

                elif any(keyword in line.lower() for keyword in ["config", "misconfiguration"]):
                    severity = "low"

                vuln = {
                    "description": line.lstrip("+").strip(),
                    "severity": severity,
                    "type": "web_vulnerability",
                }

                vulnerabilities.append(vuln)

        results["vulnerabilities"] = vulnerabilities

        results["findings_count"] = len(vulnerabilities)

        return results
