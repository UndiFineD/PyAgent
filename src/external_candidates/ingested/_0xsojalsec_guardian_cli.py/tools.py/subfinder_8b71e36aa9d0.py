# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-guardian-cli\tools\subfinder.py
"""
Subfinder tool wrapper for subdomain discovery
"""

import json
from typing import Any, Dict, List

from tools.base_tool import BaseTool


class SubfinderTool(BaseTool):
    """Subfinder subdomain enumeration wrapper"""

    def __init__(self, config):
        super().__init__(config)
        self.tool_name = "subfinder"

    def get_command(self, target: str, **kwargs) -> List[str]:
        """Build subfinder command"""
        config = self.config.get("tools", {}).get("subfinder", {})

        command = ["subfinder"]

        # Domain
        command.extend(["-d", target])

        # JSON output
        command.append("-json")

        # Silent mode (only output)
        command.append("-silent")

        # Sources
        sources = config.get("sources", [])
        if sources:
            command.extend(["-sources", ",".join(sources)])

        # All sources
        if kwargs.get("all_sources"):
            command.append("-all")

        return command

    def parse_output(self, output: str) -> Dict[str, Any]:
        """Parse subfinder JSON output"""
        results = {"subdomains": [], "count": 0, "sources": {}}

        # Parse JSON lines
        for line in output.strip().split("\n"):
            if not line:
                continue

            try:
                data = json.loads(line)
                subdomain = data.get("host", "")

                if subdomain and subdomain not in results["subdomains"]:
                    results["subdomains"].append(subdomain)
                    results["count"] += 1

                    # Track sources
                    source = data.get("source", "unknown")
                    if source not in results["sources"]:
                        results["sources"][source] = 0
                    results["sources"][source] += 1

            except json.JSONDecodeError:
                # Plain text mode
                subdomain = line.strip()
                if subdomain and subdomain not in results["subdomains"]:
                    results["subdomains"].append(subdomain)
                    results["count"] += 1

        return results
