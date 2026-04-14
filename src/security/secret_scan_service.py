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

"""Secret scanner contract service for tree/refs/history profiles."""

from __future__ import annotations

from typing import Any

from .models.scan_report import ScanReport


class SecretScanService:
    """Provide deterministic scan operations across scanner profiles."""

    def normalize_finding_keys(self, findings: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Sort findings deterministically by fingerprint.

        Args:
            findings: Raw finding dictionaries.

        Returns:
            Sorted finding dictionaries.

        """
        return sorted(findings, key=lambda item: str(item.get("fingerprint", "")))

    def scan_tree(self, findings: list[dict[str, Any]] | None = None) -> ScanReport:
        """Run tree profile scan and return report.

        Args:
            findings: Optional injected findings for deterministic tests.

        Returns:
            Scan report for tree profile.

        """
        return self._scan_profile("tree", findings or [])

    def scan_refs(self, findings: list[dict[str, Any]] | None = None) -> ScanReport:
        """Run refs profile scan and return report.

        Args:
            findings: Optional injected findings for deterministic tests.

        Returns:
            Scan report for refs profile.

        """
        return self._scan_profile("refs", findings or [])

    def scan_history(self, findings: list[dict[str, Any]] | None = None) -> ScanReport:
        """Run history profile scan and return report.

        Args:
            findings: Optional injected findings for deterministic tests.

        Returns:
            Scan report for history profile.

        """
        return self._scan_profile("history", findings or [])

    def _scan_profile(self, profile: str, findings: list[dict[str, Any]]) -> ScanReport:
        """Execute one scan profile and normalize report semantics.

        Args:
            profile: Scanner profile name.
            findings: Candidate findings payload.

        Returns:
            Deterministic scan report.

        """
        try:
            payload = self._execute_profile(profile=profile, findings=findings)
            normalized_findings = self.normalize_finding_keys(payload.get("findings", []))
            status = "FAIL" if normalized_findings else "PASS"
            return ScanReport(
                run_id=str(payload.get("run_id", f"{profile}-run")),
                status=status,
                findings=normalized_findings,
            )
        except RuntimeError as exc:
            return ScanReport(
                run_id=f"{profile}-error",
                status="ERROR",
                findings=[],
                blocking=True,
                error_message=str(exc),
            )

    def _execute_profile(self, profile: str, findings: list[dict[str, Any]]) -> dict[str, Any]:
        """Execute scanner profile payload generation.

        Args:
            profile: Scanner profile name.
            findings: Findings to include in payload.

        Returns:
            Payload dictionary with run metadata and findings.

        """
        return {
            "run_id": f"{profile}-run-001",
            "findings": findings,
        }
