#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Observability agents for monitoring, reporting, and transparency.

from __future__ import annotations
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any
from src.core.base.BaseAgent import BaseAgent
from .Engine import StatsCore
from .observability_core import Alert, Metric, MetricSnapshot, MetricType, Threshold

logger = logging.getLogger(__name__)


class StatsAgent:
    """Agent that calculates statistics for fleet progress and file maintenance."""

    def __init__(self, files: list[str]) -> None:
        self.files = [Path(f) for f in files if Path(f).exists()]
        self.core = StatsCore()
        self._metrics: dict[str, list[Metric]] = {}
        self._thresholds: list[Threshold] = []
        self._alerts: list[Alert] = []
        self._snapshots: list[MetricSnapshot] = []

    def add_metric(
        self, name: str, value: float, type: MetricType = MetricType.GAUGE
    ) -> Metric:
        m = Metric(
            name=name,
            value=value,
            metric_type=type,
            timestamp=datetime.now().isoformat(),
        )
        if name not in self._metrics:
            self._metrics[name] = []
        self._metrics[name].append(m)
        self.core.record(m)
        return m

    def calculate_stats(self) -> dict[str, int]:
        total = len(self.files)
        with_tests = 0
        with_context = 0
        with_changes = 0
        with_errors = 0
        with_improvements = 0

        for f in self.files:
            # Check for test file
            if (f.parent / f"test_{f.stem}.py").exists() or (
                f.parent / f"test_{f.name}"
            ).exists():
                with_tests += 1

            # Check for context files (assumed collocated for this agent version)
            # In broader system these might be in docs/autodoc, but for local stats agent we check colloquial locations
            has_desc = (f.parent / f"{f.stem}.description.md").exists()
            if has_desc:
                with_context += 1

            if (f.parent / f"{f.stem}.changes.md").exists():
                with_changes += 1

            if (f.parent / f"{f.stem}.errors.md").exists():
                with_errors += 1

            if (f.parent / f"{f.stem}.improvements.md").exists():
                with_improvements += 1

        return {
            "total_files": total,
            "files_with_tests": with_tests,
            "files_with_context": with_context,
            "files_with_changes": with_changes,
            "files_with_errors": with_errors,
            "files_with_improvements": with_improvements,
        }


class ReportingAgent(BaseAgent):
    """Observer agent that generates executive dashboards and reports."""

    def __init__(self, fleet: Any) -> None:
        super().__init__("Reporting", "Expert report generation and dashboarding.")
        self.fleet = fleet

    async def generate_dashboard(self) -> str:
        summary = self.fleet.telemetry.summarize_performance()
        return f"# 🚀 PyAgent Active Progress Dashboard\n\n## 🛡️ Executive Summary\n{json.dumps(summary, indent=2)}"


class TransparencyAgent(BaseAgent):
    """Provides a detailed audit trail of agent thoughts, signals, and dependencies."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._system_prompt = (
            "You are the Transparency Agent. Explain WHY decisions were made."
        )

    def generate_audit_trail(self) -> str:
        return "# fleet Transparency Audit Trail\n\n### 📡 Signal Event Log\n- Audit trail active."
