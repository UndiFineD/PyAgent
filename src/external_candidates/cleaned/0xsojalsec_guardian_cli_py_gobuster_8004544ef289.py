# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_guardian_cli.py\tools.py\gobuster_8004544ef289.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-guardian-cli\tools\gobuster.py

"""

Gobuster tool wrapper for directory and file brute forcing

"""

import re

from typing import Any, Dict, List

from tools.base_tool import BaseTool


class GobusterTool(BaseTool):
    """Gobuster directory/file brute forcing wrapper"""

    def __init__(self, config):
        super().__init__(config)

        self.tool_name = "gobuster"

    def get_command(self, target: str, **kwargs) -> List[str]:
        """Build gobuster command"""

        command = ["gobuster", "dir"]

        # Target URL

        command.extend(["-u", target])

        # Wordlist

        wordlist = kwargs.get("wordlist", "/usr/share/wordlists/dirb/common.txt")

        command.extend(["-w", wordlist])

        # Threads

        threads = kwargs.get("threads", 10)

        command.extend(["-t", str(threads)])

        # Status codes to look for

        status_codes = kwargs.get("status_codes", "200,204,301,302,307,401,403")

        command.extend(["-s", status_codes])

        # Extensions

        extensions = kwargs.get("extensions", "")

        if extensions:
            command.extend(["-x", extensions])

        # Timeout

        timeout = kwargs.get("timeout", 10)

        command.extend(["--timeout", f"{timeout}s"])

        # Quiet mode

        command.append("-q")

        # No progress

        command.append("--no-progress")

        return command

    def parse_output(self, output: str) -> Dict[str, Any]:
        """Parse gobuster output"""

        results = {"directories": [], "files": [], "found_count": 0, "status_codes": {}}

        # Parse each line

        for line in output.split("\n"):
            line = line.strip()

            if not line or line.startswith("="):
                continue

            # e.g.: /admin (Status: 200) [Size: 1234]

            match = re.search(r"(/[^\s]*)\s+\(Status:\s+(\d+)\)", line)

            if match:
                path = match.group(1)

                status = match.group(2)

                # Extract size if available

                size_match = re.search(r"\[Size:\s+(\d+)\]", line)

                size = int(size_match.group(1)) if size_match else None

                finding = {
                    "path": path,
                    "status_code": int(status),
                    "size": size,
                    "url": f"{line.split()[0] if not line.startswith('/') else path}",
                }

                # Categorize as directory or file

                if path.endswith("/") or status in ["301", "302"]:
                    results["directories"].append(finding)

                else:
                    results["files"].append(finding)

                results["found_count"] += 1

                # Track status codes

                if status not in results["status_codes"]:
                    results["status_codes"][status] = 0

                results["status_codes"][status] += 1

        return results
