# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-guardian-cli\tools\dnsrecon.py
import json
import os
from typing import Any, Dict, List

from tools.base_tool import BaseTool


class DnsReconTool(BaseTool):
    """Wrapper for DnsRecon - DNS Enumeration Script"""

    def get_command(self, target: str, **kwargs) -> List[str]:
        cmd = ["dnsrecon", "-d", target]

        # Output to JSON
        self.output_file = f"dnsrecon_{self._get_timestamp()}.json"
        cmd.extend(["-j", self.output_file])

        # Tool options
        if kwargs.get("type"):
            cmd.extend(["-t", kwargs["type"]])  # std, rvl, brt, etc.

        if kwargs.get("dictionary"):
            cmd.extend(["-D", kwargs["dictionary"]])

        if kwargs.get("threads"):
            cmd.extend(["--threads", str(kwargs["threads"])])

        return cmd

    def parse_output(self, output: str) -> Dict[str, Any]:
        result = {"records": [], "raw_output": output}

        if os.path.exists(self.output_file):
            try:
                with open(self.output_file, "r") as f:
                    data = json.load(f)

                if isinstance(data, list):
                    result["records"] = data

                # Cleanup
                os.remove(self.output_file)
            except Exception as e:
                self.logger.error(f"Error parsing DnsRecon JSON: {e}")

        return result

    def _get_timestamp(self):
        import time

        return int(time.time())
