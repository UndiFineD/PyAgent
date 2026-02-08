# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_guardian_cli.py\tools.py\testssl_d4dc64450f94.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-guardian-cli\tools\testssl.py

"""

TestSSL tool wrapper for SSL/TLS testing

"""

import re

from typing import Any, Dict, List

from tools.base_tool import BaseTool


class TestSSLTool(BaseTool):
    """TestSSL.sh SSL/TLS testing wrapper"""

    def __init__(self, config):
        super().__init__(config)

        self.tool_name = "testssl.sh"

    def get_command(self, target: str, **kwargs) -> List[str]:
        """Build testssl command"""

        command = ["testssl.sh"]

        # Machine-readable output

        command.append("--jsonfile=-")

        # Severity level

        severity = kwargs.get("severity", "HIGH")

        command.extend(["--severity", severity])

        # Fast mode

        if kwargs.get("fast", False):
            command.append("--fast")

        # Quiet mode

        command.append("--quiet")

        # Target (host:port or URL)

        command.append(target)

        return command

    def parse_output(self, output: str) -> Dict[str, Any]:
        """Parse testssl JSON output"""

        results = {
            "ssl_enabled": False,
            "tls_versions": [],
            "cipher_suites": [],
            "vulnerabilities": [],
            "certificate_info": {},
            "grade": None,
            "issues_count": 0,
        }

        try:
            import json

            # TestSSL outputs JSON lines

            for line in output.strip().split("\n"):
                if not line or not line.startswith("{"):
                    continue

                try:
                    data = json.loads(line)

                    # Extract certificate info

                    if data.get("id") == "cert_commonName":
                        results["certificate_info"]["common_name"] = data.get("finding")

                    elif data.get("id") == "cert_notAfter":
                        results["certificate_info"]["expiry"] = data.get("finding")

                    # Extract protocols

                    elif "SSLv" in data.get("id", "") or "TLS" in data.get("id", ""):
                        if data.get("finding") == "offered":
                            protocol = data.get("id").replace("_", " ")

                            results["tls_versions"].append(protocol)

                    # Extract vulnerabilities

                    elif data.get("severity") in ["HIGH", "CRITICAL", "MEDIUM"]:
                        vuln = {
                            "name": data.get("id"),
                            "severity": data.get("severity").lower(),
                            "finding": data.get("finding"),
                            "cve": data.get("cve", ""),
                        }

                        results["vulnerabilities"].append(vuln)

                        results["issues_count"] += 1

                except json.JSONDecodeError:
                    continue

            results["ssl_enabled"] = len(results["tls_versions"]) > 0

        except Exception as e:
            # Fallback to text parsing if JSON fails

            if "ssl" in output.lower() or "tls" in output.lower():
                results["ssl_enabled"] = True

        return results
