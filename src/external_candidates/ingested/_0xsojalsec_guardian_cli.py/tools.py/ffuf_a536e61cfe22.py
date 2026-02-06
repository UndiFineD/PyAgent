# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-guardian-cli\tools\ffuf.py
"""
FFuf tool wrapper for fast web fuzzing
"""

import json
from typing import Any, Dict, List

from tools.base_tool import BaseTool


class FFufTool(BaseTool):
    """FFuf fast web fuzzer wrapper"""

    def __init__(self, config):
        super().__init__(config)
        self.tool_name = "ffuf"

    def get_command(self, target: str, **kwargs) -> List[str]:
        """Build ffuf command"""
        config = self.config.get("tools", {}).get("ffuf", {})

        command = ["ffuf"]

        # Target URL with FUZZ keyword
        if "FUZZ" not in target:
            # If no FUZZ keyword, append it to the end
            target = f"{target}/FUZZ"
        command.extend(["-u", target])

        # Wordlist (required)
        wordlist = kwargs.get(
            "wordlist", config.get("wordlist", "/usr/share/wordlists/dirb/common.txt")
        )
        command.extend(["-w", wordlist])

        # JSON output for parsing
        command.extend(["-of", "json"])
        command.extend(["-o", "-"])  # Output to stdout

        # Threads
        threads = config.get("threads", 40)
        command.extend(["-t", str(threads)])

        # Timeout
        timeout = config.get("timeout", 10)
        command.extend(["-timeout", str(timeout)])

        # Filter by status code
        if "filter_status" in kwargs:
            command.extend(["-fc", kwargs["filter_status"]])

        # Match status code
        if "match_status" in kwargs:
            command.extend(["-mc", kwargs["match_status"]])
        else:
            # Default: match success codes
            command.extend(["-mc", "200,204,301,302,307,401,403"])

        # Filter by size
        if "filter_size" in kwargs:
            command.extend(["-fs", str(kwargs["filter_size"])])

        # Extensions
        if "extensions" in kwargs:
            command.extend(["-e", kwargs["extensions"]])

        # Recursion
        if kwargs.get("recursion"):
            command.append("-recursion")
            recursion_depth = kwargs.get("recursion_depth", 1)
            command.extend(["-recursion-depth", str(recursion_depth)])

        # Follow redirects
        if config.get("follow_redirects", False):
            command.append("-r")

        # Rate limit (requests per second)
        if "rate" in kwargs:
            command.extend(["-rate", str(kwargs["rate"])])

        # Silent mode (less verbose)
        command.append("-s")

        return command

    def parse_output(self, output: str) -> Dict[str, Any]:
        """Parse ffuf JSON output"""
        results = {
            "discovered_paths": [],
            "status_codes": {},
            "sizes": {},
            "total_requests": 0,
            "total_filtered": 0,
        }

        try:
            # FFuf outputs JSON
            if not output.strip():
                return results

            data = json.loads(output)

            # Extract results
            if "results" in data:
                for result in data["results"]:
                    url = result.get("url", "")
                    status = result.get("status", 0)
                    length = result.get("length", 0)

                    results["discovered_paths"].append(
                        {
                            "url": url,
                            "status": status,
                            "length": length,
                            "words": result.get("words", 0),
                            "lines": result.get("lines", 0),
                        }
                    )

                    results["status_codes"][url] = status
                    results["sizes"][url] = length

            # Extract metadata
            if "config" in data:
                results["total_requests"] = (
                    data.get("config", {}).get("matcher", {}).get("count", 0)
                )

        except json.JSONDecodeError:
            # Fallback: try to parse line by line if not valid JSON
            pass

        return results
