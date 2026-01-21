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
from src.core.base.version import VERSION
from pathlib import Path
from .mixins.privacy_scanner_mixin import PrivacyScannerMixin
from .mixins.privacy_assessment_mixin import PrivacyAssessmentMixin
from src.core.base.base_agent import BaseAgent
from src.infrastructure.backend.local_context_recorder import LocalContextRecorder

__version__ = VERSION


class ComplianceAgent(BaseAgent, PrivacyScannerMixin, PrivacyAssessmentMixin):
    """
    Phase 57: Data Privacy & Compliance.
    Scans memory shards for PII and sensitive data patterns.
    """

    def __init__(self, path: str) -> None:
        super().__init__(path)
        self.pii_patterns = {
            "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
            "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
            "credit_card": r"\b\d{4}-\d{4}-\d{4}-\d{4}\b",
            "phone": r"\b\d{3}-\d{3}-\d{4}\b",
        }

        # Phase 108: Intelligence Recording
        work_root = getattr(self, "_workspace_root", None)
        self.recorder = LocalContextRecorder(Path(work_root)) if work_root else None


    # Logic delegated to mixins

    def scan_shard(self, content: str) -> dict:
        """Scans a memory shard for compliance issues (Phase 57)."""
        import re
        findings = []
        for name, pattern in self.pii_patterns.items():
            if re.search(pattern, content):
                findings.append(name)
        return {
            "compliant": len(findings) == 0,
            "findings": findings,
            "pii_detected": len(findings) > 0
        }
