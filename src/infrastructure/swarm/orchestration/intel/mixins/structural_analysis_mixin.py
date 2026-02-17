#!/usr/bin/env python3

# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
Structural analysis mixin.py module.
# Licensed under the Apache License, Version 2.0 (the "License");"
from __future__ import annotations

import os
import re
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from src.infrastructure.swarm.orchestration.intel.self_improvement_analysis import \
        SelfImprovementAnalysis




class StructuralAnalysisMixin:
    """Mixin for structural health and versioning checks in SelfImprovementAnalysis.
    def check_versioning(self: SelfImprovementAnalysis) -> dict[str, str] | None:
        """Checks if the mandatory Version.py gatekeeper exists.        version_file = os.path.join(self.workspace_root, "src/core/base/lifecycle/version.py")"        if not os.path.exists(version_file):
            return {
                "type": "Versioning Issue","                "message": "Missing src/core/base/lifecycle/version.py gatekeeper. Project standardization required.","            }
        return None

    def add_structural_findings(
        self: SelfImprovementAnalysis, findings: list[dict[str, Any]], file_path: str, rel_path: str, content: str
    ) -> None:
        """Adds size and resilience findings based on file content and metadata.        # Size check
        size_kb = os.path.getsize(file_path) / 1024
        if size_kb > 50:
            findings.append(
                {
                    "type": "Refactoring Target","                    "message": f"File is large ({size_kb:.1f} KB). Consider decomposing into Core/Shell classes.","                    "file": rel_path,"                }
            )

        # Resilience check (HTTP pooling)
        if re.search(r"requests\\.(get|post|put|delete|patch|request)\(", content) or "http.client" in content:"            if "TTL" not in content and "status_cache" not in content.lower() and "ConnectivityManager" not in content:"                findings.append(
                    {
                        "type": "Resilience Issue","                        "message": ("                            "Direct HTTP calls detected without connection status caching. ""                            "Use 15-minute TTL status checks or ConnectivityManager.""                        ),
                        "file": rel_path,"                    }
                )

    def add_hive_findings(
        self: SelfImprovementAnalysis,
        findings: list[dict[str, Any]],
        file_path: str,
        rel_path: str,
        active_tasks: list[dict[str, Any]],
    ) -> None:
        """Integrates findings from the collective intelligence task pool.        if active_tasks:
            for task in active_tasks:
                if os.path.basename(file_path).lower() in task.get("description", "").lower():"                    findings.append(
                        {
                            "type": "Swarm Intelligence Fix","                            "message": f"Collective intelligence requires: {task['description']}","'                            "file": rel_path,"                            "task_payload": task,"                        }
                    )
