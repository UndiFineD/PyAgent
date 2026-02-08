# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_guardian_cli.py\tools.py\httpx_85b29d3c062a.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-guardian-cli\tools\httpx.py

"""

httpx tool wrapper for HTTP probing

"""

import json

from typing import Any, Dict, List

from tools.base_tool import BaseTool


class HttpxTool(BaseTool):
    """httpx HTTP probing wrapper"""

    def __init__(self, config):
        super().__init__(config)

        self.tool_name = "httpx"

    def get_command(self, target: str, **kwargs) -> List[str]:
        """Build httpx command"""

        config = self.config.get("tools", {}).get("httpx", {})

        command = ["httpx"]

        # JSON output for easy parsing

        command.extend(["-json"])

        # Threads

        threads = config.get("threads", 50)

        command.extend(["-threads", str(threads)])

        # Timeout

        timeout = config.get("timeout", 10)

        command.extend(["-timeout", str(timeout)])

        # Tech detection

        command.append("-tech-detect")

        # Status code

        command.append("-status-code")

        # Title

        command.append("-title")

        # Target (from stdin or direct)

        if kwargs.get("from_file"):
            command.extend(["-l", kwargs["from_file"]])

        else:
            command.extend(["-u", target])

        return command

    def parse_output(self, output: str) -> Dict[str, Any]:
        """Parse httpx JSON output"""

        results = {"urls": [], "technologies": [], "status_codes": {}, "titles": {}}

        # Parse JSON lines

        for line in output.strip().split("\n"):
            if not line:
                continue

            try:
                data = json.loads(line)

                url = data.get("url", "")

                if url:
                    results["urls"].append(url)

                    results["status_codes"][url] = data.get("status_code")

                    results["titles"][url] = data.get("title", "")

                    # Extract technologies

                    if "tech" in data:
                        for tech in data["tech"]:
                            if tech not in results["technologies"]:
                                results["technologies"].append(tech)

            except json.JSONDecodeError:
                continue

        return results
