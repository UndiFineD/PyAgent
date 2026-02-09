# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-guardian-cli\tools\sqlmap.py
"""
SQLMap tool wrapper for automated SQL injection testing
"""

import json
import re
from typing import Any, Dict, List

from tools.base_tool import BaseTool


class SQLMapTool(BaseTool):
    """SQLMap SQL injection testing wrapper"""

    def __init__(self, config):
        super().__init__(config)
        self.tool_name = "sqlmap"

    def get_command(self, target: str, **kwargs) -> List[str]:
        """Build sqlmap command"""
        config = self.config.get("tools", {}).get("sqlmap", {})
        safe_mode = self.config.get("pentest", {}).get("safe_mode", True)

        command = ["sqlmap"]

        # Target URL
        command.extend(["-u", target])

        # Batch mode (non-interactive)
        command.append("--batch")

        # Output format
        command.append("--parse-errors")

        # Risk and level (safe mode uses conservative settings)
        if safe_mode:
            risk = config.get("risk", 1)  # 1 = safe
            level = config.get("level", 1)  # 1 = basic
        else:
            risk = kwargs.get("risk", config.get("risk", 2))
            level = kwargs.get("level", config.get("level", 3))

        command.extend(["--risk", str(risk)])
        command.extend(["--level", str(level)])

        # Threads for speed
        threads = config.get("threads", 1)
        command.extend(["--threads", str(threads)])

        # Timeout per HTTP request
        timeout = config.get("timeout", 30)
        command.extend(["--timeout", str(timeout)])

        # Techniques (if specified)
        if "technique" in kwargs:
            command.extend(["--technique", kwargs["technique"]])

        # Database enumeration (only if not in safe mode)
        if not safe_mode and kwargs.get("enumerate"):
            command.append("--dbs")

        # Specific database
        if "database" in kwargs:
            command.extend(["-D", kwargs["database"]])

        # POST data
        if "data" in kwargs:
            command.extend(["--data", kwargs["data"]])

        # Cookie
        if "cookie" in kwargs:
            command.extend(["--cookie", kwargs["cookie"]])

        # Tamper scripts
        if "tamper" in kwargs:
            command.extend(["--tamper", kwargs["tamper"]])

        # Random user agent
        command.append("--random-agent")

        return command

    def parse_output(self, output: str) -> Dict[str, Any]:
        """Parse sqlmap output"""
        results = {
            "vulnerable": False,
            "injection_points": [],
            "databases": [],
            "dbms": None,
            "injection_types": [],
            "payloads": [],
        }

        # Check if vulnerable
        if "sqlmap identified the following injection point" in output.lower():
            results["vulnerable"] = True

        # Extract DBMS
        dbms_match = re.search(r"back-end DBMS:\s*([^\n]+)", output, re.IGNORECASE)
        if dbms_match:
            results["dbms"] = dbms_match.group(1).strip()

        # Extract injection types
        type_patterns = [r"Type:\s*([^\n]+)", r"injection point[s]?.*?Type:\s*([^\n]+)"]
        for pattern in type_patterns:
            for match in re.finditer(pattern, output, re.IGNORECASE):
                injection_type = match.group(1).strip()
                if injection_type and injection_type not in results["injection_types"]:
                    results["injection_types"].append(injection_type)

        # Extract parameters
        param_match = re.search(r"Parameter:\s*([^\n]+)", output)
        if param_match:
            param = param_match.group(1).strip()
            results["injection_points"].append({"parameter": param, "vulnerable": True})

        # Extract payloads
        payload_pattern = r"Payload:\s*([^\n]+)"
        for match in re.finditer(payload_pattern, output):
            payload = match.group(1).strip()
            if payload:
                results["payloads"].append(payload)

        # Extract databases (if enumeration was done)
        db_section = re.search(
            r"available databases \[(\d+)\]:(.*?)(\n\n|\Z)",
            output,
            re.DOTALL | re.IGNORECASE,
        )
        if db_section:
            db_text = db_section.group(2)
            # Extract database names from bulleted list
            db_names = re.findall(r"\[\*\]\s*([^\n]+)", db_text)
            results["databases"] = [db.strip() for db in db_names]

        return results
