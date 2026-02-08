# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_guardian_cli.py\tools.py\xsstrike_606ba37a6082.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-guardian-cli\tools\xsstrike.py

import json

import re

from typing import Any, Dict, List

from tools.base_tool import BaseTool


class XSStrikeTool(BaseTool):
    """Wrapper for XSStrike - Advanced XSS Detection Suite"""

    def get_command(self, target: str, **kwargs) -> List[str]:
        # XSStrike is often a python script, not always in path

        # Assuming it's installed as 'xsstrike' or runnable python module

        cmd = ["xsstrike", "-u", target]

        if kwargs.get("crawl", False):
            cmd.append("--crawl")

        if kwargs.get("level"):
            cmd.extend(["-l", str(kwargs["level"])])

        if kwargs.get("headers"):
            cmd.extend(["--headers", kwargs["headers"]])

        # JSON output support in XSStrike is limited/experimental in some versions

        # We'll rely on parsing stdout or --json if available in the specific installed version

        # For this wrapper, we'll try to use --json if supported, otherwise parse stdout

        if kwargs.get("json_output", True):
            cmd.append("--json")

        # Add timeout

        if kwargs.get("timeout"):
            cmd.extend(["--timeout", str(kwargs["timeout"])])

        return cmd

    def parse_output(self, output: str) -> Dict[str, Any]:
        result = {"vulnerabilities": [], "crawled_urls": [], "raw_output": output}

        # Try to parse JSON lines if mixed in output

        for line in output.splitlines():
            try:
                if line.strip().startswith("{") and "vulnerable" in line:
                    data = json.loads(line)

                    if data.get("vulnerable"):
                        result["vulnerabilities"].append(
                            {
                                "url": data.get("url"),
                                "param": data.get("param"),
                                "vector": data.get("vector"),
                                "payload": data.get("payload"),
                            }
                        )

            except json.JSONDecodeError:
                pass

        # Fallback: Regex parsing for standard output

        if not result["vulnerabilities"]:
            # Pattern for payloads found

            payloads = re.findall(r"Payload: (.*)", output)

            vectors = re.findall(r"Vector: (.*)", output)

            for i, payload in enumerate(payloads):
                result["vulnerabilities"].append(
                    {
                        "payload": payload,
                        "vector": vectors[i] if i < len(vectors) else "Unknown",
                    }
                )

        return result
