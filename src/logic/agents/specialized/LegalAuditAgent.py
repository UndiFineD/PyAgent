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

from __future__ import annotations
import os
import re
import asyncio
from typing import List, Dict, Any
from src.core.base.BaseAgent import BaseAgent
from src.core.base.utilities import as_tool

class LegalAuditAgent(BaseAgent):
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
            "MIT"
        ]
        self.header_pattern = re.compile(r"Licensed under the Apache License, Version 2.0")

    @as_tool
    async def run_audit(self, target_dir: str) -> dict[str, Any]:
        """Scans a directory for license compliance issues."""
        def walk_and_check() -> dict[str, Any]:
            results = {
                "compliant": [],
                "non_compliant": [],
                "missing_hashes": []
            }

            for root, _, files in os.walk(target_dir):
                if "node_modules" in root or ".git" in root or "__pycache__" in root:
                    continue
                    
                for file in files:
                    if not file.endswith((".py", ".js", ".ts", ".go", ".rs")):
                        continue
                        
                    path = os.path.join(root, file)
                    try:
                        with open(path, encoding="utf-8") as f:
                            content = f.read(1000) # Check first 1KB for header
                            
                        if any(lic in content for lic in self.allowed_licenses):
                            results["compliant"].append(path)
                        else:
                            results["non_compliant"].append({
                                "file": path,
                                "issue": "Missing or unsupported license header"
                            })
                    except Exception as e:
                        results["non_compliant"].append({
                            "file": path,
                            "issue": f"Error reading file: {str(e)}"
                        })
            return results

        return await asyncio.to_thread(walk_and_check)

    async def get_improvement_items(self, context: dict[str, Any]) -> list[dict[str, Any]]:
        """Provides improvements for files missing license headers."""
        target = context.get("target_dir", ".")
        audit = await self.run_audit(target)
        
        improvements = []
        for issue in audit["non_compliant"]:
            improvements.append({
                "path": issue["file"],
                "improvement": f"Add Apache 2.0 license header to {issue['file']}",
                "priority": 0.8
            })
        return improvements
