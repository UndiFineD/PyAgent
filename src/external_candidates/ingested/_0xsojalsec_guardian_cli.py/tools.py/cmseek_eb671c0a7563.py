# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-guardian-cli\tools\cmseek.py
import json
import re
from typing import Any, Dict, List

from tools.base_tool import BaseTool


class CMSeekTool(BaseTool):
    """Wrapper for CMSeek - CMS Detection and Exploitation Tool"""

    def get_command(self, target: str, **kwargs) -> List[str]:
        # python3 cmseek.py -u <target>
        # Assuming installed as 'cmseek' command or python script
        cmd = ["cmseek", "-u", target]

        if kwargs.get("batch"):
            cmd.append("--batch")

        if kwargs.get("random_agent"):
            cmd.append("--random-agent")

        if kwargs.get("light_scan"):
            cmd.append("--light-scan")

        return cmd

    def parse_output(self, output: str) -> Dict[str, Any]:
        result = {"cms": None, "version": None, "url": None, "raw_output": output}

        # CMSeek output parsing (JSON output support is limited in some versions, parsing stdout is safer)
        # Look for "CMS: WordPress" etc.

        cms_match = re.search(r"CMS Detected: (.*)", output, re.IGNORECASE)
        if cms_match:
            result["cms"] = cms_match.group(1).strip()

        version_match = re.search(r"CMS Version: (.*)", output, re.IGNORECASE)
        if version_match:
            result["version"] = version_match.group(1).strip()

        url_match = re.search(r"Target: (.*)", output, re.IGNORECASE)
        if url_match:
            result["url"] = url_match.group(1).strip()

        return result
