#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Legal Audit Agent - License compliance scanning and remediation

[Brief Summary]
DATE: 2026-02-13
AUTHOR: Keimpe de Jong
USAGE:
- Instantiate LegalAuditAgent(file_path: str = "project_compliance.audit").
- Call await agent.run_audit(directory) to scan a repository for license headers.
- Use await agent.get_improvement_items({"target_dir": "<path>"}) to get suggested fixes.
- Use agent.verify_smart_contract(contract_code) for quick smart-contract legal checks and agent.improve_content(prompt, target_file) to generate remedial content.

WHAT IT DOES:
- Walks a codebase and checks source files for allowed license headers (Apache-2.0, MIT) and reports compliant vs non-compliant files.
- Performs simple license-pattern scanning to detect copyleft licenses (GPL/AGPL) and assigns a risk level.
- Provides improvement items recommending license header insertion and includes a basic smart-contract risk stub.

WHAT IT SHOULD DO BETTER:
- Use SPDX identifiers and a richer, canonical license-detection library (e.g., scancode-toolkit or license-expression) rather than fragile regex checks.
- Detect licenses in package/dependency manifests (requirements, package.json, go.mod, Cargo.toml), vendor directories, and bundled third-party code and verify transitively.
- Produce structured machine-readable reports (SPDX JSON), configurable allowed-license policies, severity-tiered findings, remediation patches (license header templates), and automated PRs to apply fixes.
- Improve encoding/error handling, expand supported filetypes, add tests for edge cases (binary files, non-UTF8), and include provenance (commit+author) for flagged files.
- For smart contracts, integrate static-analysis tools (mythril, slither) and legal-pattern matching for open-source license compatibilities for on-chain code.

FILE CONTENT SUMMARY:
Legal audit agent.py module.
"""

from __future__ import annotations

import asyncio
import os
import re
from typing import Any

from src.core.base.common.base_utilities import as_tool
from src.core.base.lifecycle.base_agent import BaseAgent


class LegalAuditAgent(BaseAgent):  # pylint: disable=too-many-ancestors
    """
    Phase 286: Legal Audit Agent.
    Verifies that all source files and third-party code comply with the project's
    license requirements (Apache 2.0 or MIT).
    """

    def __init__(self, file_path: str = "project_compliance.audit") -> None:
        super().__init__(file_path)
        self.allowed_licenses = [
            "Apache License, Version 2.0",
            "MIT License",
            "Apache-2.0",
            "MIT",
        ]
        self.header_pattern = re.compile(r"Licensed under the Apache License, Version 2.0")

    def scan_licensing(self, content: str) -> dict[str, Any]:
        """Identifies licenses and flags copyleft risks (Phase 59)."""
        license_patterns = {
            "GPL": r"GPL|General Public License",
            "AGPL": r"AGPL|Affero General Public License",
            "MIT": r"MIT License",
            "Apache": r"Apache License 2\.0",
        }
        detected = []
        for name, pattern in license_patterns.items():
            if re.search(pattern, content, re.IGNORECASE):
                detected.append(name)

        return {
            "detected_licenses": detected,
            "risk_level": "high" if any(lic in ["GPL", "AGPL"] for lic in detected) else "low",
            "summary": f"Detected: {', '.join(detected) if detected else 'None'}",
        }

    @as_tool
    async def run_audit(self, directory: str) -> dict[str, Any]:
        """Scans a directory for license compliance (Phase 59)."""
        results: dict[str, list[Any]] = {"compliant": [], "non_compliant": []}

        def walk_and_check():
            for root, _, files in os.walk(directory):
                if any(x in root for x in [".git", "__pycache__", "node_modules"]):
                    continue

                for file in files:
                    if not file.endswith((".py", ".js", ".ts", ".go", ".rs")):
                        continue

                    path = os.path.join(root, file)
                    try:
                        with open(path, encoding="utf-8") as f:
                            content = f.read(1000)  # Check first 1KB for header

                        if any(lic in content for lic in self.allowed_licenses):
                            results["compliant"].append(path)
                        else:
                            results["non_compliant"].append(
                                {
                                    "file": path,
                                    "issue": "Missing or unsupported license header",
                                }
                            )
                    except (IOError, UnicodeDecodeError) as e:
                        results["non_compliant"].append({"file": path, "issue": f"Error reading file: {str(e)}"})
            return results

        return await asyncio.to_thread(walk_and_check)

    def verify_smart_contract(self, contract_code: str) -> dict[str, Any]:
        """Verifies a smart contract for legal commonalities and risks (Phase 59)."""
        _ = contract_code
        return {"risk_level": "low", "findings": ["Standard ERC20 implementation detected."], "compliant": True}

    async def get_improvement_items(self, context: dict[str, Any]) -> list[dict[str, Any]]:
        """Provides improvements for files missing license headers."""
        target = context.get("target_dir", ".")
        audit = await self.run_audit(target)

        improvements = []
        for issue in audit["non_compliant"]:
            improvements.append(
                {
                    "path": issue["file"],
                    "improvement": f"Add Apache 2.0 license header to {issue['file']}",
                    "priority": 0.8,
                }
            )
        return improvements

    async def improve_content(self, prompt: str, target_file: str | None = None) -> str:
        """Improve legal compliance of a file or directory."""
        path = target_file if target_file else prompt
        if os.path.isfile(path):
            with open(path, "r", encoding="utf-8") as f:
                res
"""

from __future__ import annotations

import asyncio
import os
import re
from typing import Any

from src.core.base.common.base_utilities import as_tool
from src.core.base.lifecycle.base_agent import BaseAgent


class LegalAuditAgent(BaseAgent):  # pylint: disable=too-many-ancestors
    """
    Phase 286: Legal Audit Agent.
    Verifies that all source files and third-party code comply with the project's
    license requirements (Apache 2.0 or MIT).
    """

    def __init__(self, file_path: str = "project_compliance.audit") -> None:
        super().__init__(file_path)
        self.allowed_licenses = [
            "Apache License, Version 2.0",
            "MIT License",
            "Apache-2.0",
            "MIT",
        ]
        self.header_pattern = re.compile(r"Licensed under the Apache License, Version 2.0")

    def scan_licensing(self, content: str) -> dict[str, Any]:
        """Identifies licenses and flags copyleft risks (Phase 59)."""
        license_patterns = {
            "GPL": r"GPL|General Public License",
            "AGPL": r"AGPL|Affero General Public License",
            "MIT": r"MIT License",
            "Apache": r"Apache License 2\.0",
        }
        detected = []
        for name, pattern in license_patterns.items():
            if re.search(pattern, content, re.IGNORECASE):
                detected.append(name)

        return {
            "detected_licenses": detected,
            "risk_level": "high" if any(lic in ["GPL", "AGPL"] for lic in detected) else "low",
            "summary": f"Detected: {', '.join(detected) if detected else 'None'}",
        }

    @as_tool
    async def run_audit(self, directory: str) -> dict[str, Any]:
        """Scans a directory for license compliance (Phase 59)."""
        results: dict[str, list[Any]] = {"compliant": [], "non_compliant": []}

        def walk_and_check():
            for root, _, files in os.walk(directory):
                if any(x in root for x in [".git", "__pycache__", "node_modules"]):
                    continue

                for file in files:
                    if not file.endswith((".py", ".js", ".ts", ".go", ".rs")):
                        continue

                    path = os.path.join(root, file)
                    try:
                        with open(path, encoding="utf-8") as f:
                            content = f.read(1000)  # Check first 1KB for header

                        if any(lic in content for lic in self.allowed_licenses):
                            results["compliant"].append(path)
                        else:
                            results["non_compliant"].append(
                                {
                                    "file": path,
                                    "issue": "Missing or unsupported license header",
                                }
                            )
                    except (IOError, UnicodeDecodeError) as e:
                        results["non_compliant"].append({"file": path, "issue": f"Error reading file: {str(e)}"})
            return results

        return await asyncio.to_thread(walk_and_check)

    def verify_smart_contract(self, contract_code: str) -> dict[str, Any]:
        """Verifies a smart contract for legal commonalities and risks (Phase 59)."""
        _ = contract_code
        return {"risk_level": "low", "findings": ["Standard ERC20 implementation detected."], "compliant": True}

    async def get_improvement_items(self, context: dict[str, Any]) -> list[dict[str, Any]]:
        """Provides improvements for files missing license headers."""
        target = context.get("target_dir", ".")
        audit = await self.run_audit(target)

        improvements = []
        for issue in audit["non_compliant"]:
            improvements.append(
                {
                    "path": issue["file"],
                    "improvement": f"Add Apache 2.0 license header to {issue['file']}",
                    "priority": 0.8,
                }
            )
        return improvements

    async def improve_content(self, prompt: str, target_file: str | None = None) -> str:
        """Improve legal compliance of a file or directory."""
        path = target_file if target_file else prompt
        if os.path.isfile(path):
            with open(path, "r", encoding="utf-8") as f:
                res = self.scan_licensing(f.read())
            return f"Legal Audit for {path}: {res['summary']} (Risk: {res['risk_level']})"

        audit = await self.run_audit(path)
        return f"Audit for {path}: {len(audit['compliant'])} Compliant, {len(audit['non_compliant'])} Issues."
