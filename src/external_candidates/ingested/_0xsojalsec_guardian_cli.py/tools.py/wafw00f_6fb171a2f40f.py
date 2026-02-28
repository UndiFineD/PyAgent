# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-guardian-cli\tools\wafw00f.py
"""
Wafw00f tool wrapper for WAF detection
"""

import re
from typing import Any, Dict, List

from tools.base_tool import BaseTool


class Wafw00fTool(BaseTool):
    """Wafw00f Web Application Firewall detection wrapper"""

    def __init__(self, config):
        super().__init__(config)
        self.tool_name = "wafw00f"

    def get_command(self, target: str, **kwargs) -> List[str]:
        """Build wafw00f command"""
        command = ["wafw00f"]

        # Verbose output
        command.append("-v")

        # Find all WAFs
        if kwargs.get("find_all", True):
            command.append("-a")

        # Target
        command.append(target)

        return command

    def parse_output(self, output: str) -> Dict[str, Any]:
        """Parse wafw00f output"""
        results = {
            "waf_detected": False,
            "waf_type": None,
            "waf_vendor": None,
            "confidence": "unknown",
            "details": [],
        }

        # Look for WAF detection patterns
        if "is behind" in output.lower():
            results["waf_detected"] = True

            # Extract WAF name
            waf_match = re.search(r"is behind ([^\(]+)", output, re.IGNORECASE)
            if waf_match:
                results["waf_type"] = waf_match.group(1).strip()

            # Extract vendor if available
            vendor_match = re.search(r"\(([^)]+)\)", output)
            if vendor_match:
                results["waf_vendor"] = vendor_match.group(1).strip()

        elif "no waf detected" in output.lower():
            results["waf_detected"] = False
            results["confidence"] = "high"

        # Extract additional details
        for line in output.split("\n"):
            if line.strip() and not line.startswith("["):
                results["details"].append(line.strip())

        return results
