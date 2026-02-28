# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-guardian-cli\tools\arjun.py
import json
import os
from typing import Any, Dict, List

from tools.base_tool import BaseTool


class ArjunTool(BaseTool):
    """Wrapper for Arjun - HTTP Parameter Discovery Tool"""

    def get_command(self, target: str, **kwargs) -> List[str]:
        cmd = ["arjun", "-u", target, "--json"]

        # Add optional arguments
        if kwargs.get("method"):
            cmd.extend(["-m", kwargs["method"]])

        if kwargs.get("threads"):
            cmd.extend(["-t", str(kwargs["threads"])])

        if kwargs.get("delay"):
            cmd.extend(["--delay", str(kwargs["delay"])])

        # Output to a temporary JSON file
        self.output_file = f"arjun_{self._get_timestamp()}.json"
        cmd.extend(["-oJ", self.output_file])

        return cmd

    def parse_output(self, output: str) -> Dict[str, Any]:
        result = {"params": [], "method": "GET", "raw_output": output}

        if os.path.exists(self.output_file):
            try:
                with open(self.output_file, "r") as f:
                    data = json.load(f)

                # Arjun JSON format varies slightly by version, handle common structures
                # Typical: {"url": "...", "params": ["id", "user"], "method": "GET"}
                # Or dictionary of results

                if isinstance(data, dict):
                    # Check if it's the direct result format
                    if "params" in data:
                        result["params"] = data["params"]
                        result["method"] = data.get("method", "GET")
                    else:
                        # Iterate through keys (URLs) if it's a multi-target result
                        for url, info in data.items():
                            if isinstance(info, dict) and "params" in info:
                                result["params"].extend(info["params"])
                                result["method"] = info.get("method", "GET")

                # Cleanup
                os.remove(self.output_file)
            except Exception as e:
                self.logger.error(f"Error parsing Arjun JSON: {e}")

        return result

    def _get_timestamp(self):
        import time

        return int(time.time())
