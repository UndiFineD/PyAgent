#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Observability agents for monitoring, reporting, and transparency.

from __future__ import annotations
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List
from src.core.base.BaseAgent import BaseAgent
from .engine import StatsCore
from .metrics import Alert, Metric, MetricSnapshot, MetricType, Threshold

logger = logging.getLogger(__name__)

class StatsAgent:
    """Agent that calculates statistics for fleet progress and file maintenance."""
    def __init__(self, files:
        List[str]) -> None:
        self.files = [Path(f) for f in files if Path(f).exists()]
        self.core = StatsCore()
        self._metrics: Dict[str, List[Metric]] = {}
        self._thresholds: List[Threshold] = []
        self._alerts: List[Alert] = []
        self._snapshots: List[MetricSnapshot] = []

    def add_metric(self, name:
        str, value: float, type: MetricType = MetricType.GAUGE) -> Metric:
        m = Metric(name=name, value=value, metric_type=type, timestamp=datetime.now().isoformat())
        if name not in self._metrics:
            self._metrics[name] = []
        self._metrics[name].append(m)
        self.core.record(m)
        return m

    def calculate_stats(self) -> Dict[str, int]:
        total = len(self.files)
        with_tests = sum(1 for f in self.files if (f.parent / f"test_{f.stem}.py").exists())
        return {"total_files": total, "files_with_tests": with_tests}

class ReportingAgent(BaseAgent):
    """Observer agent that generates executive dashboards and reports."""
    def __init__(self, fleet:
        Any) -> None:
        super().__init__("Reporting", "Expert report generation and dashboarding.")
        self.fleet = fleet

    async def generate_dashboard(self) -> str:
        summary = self.fleet.telemetry.summarize_performance()
        return f"# 🚀 PyAgent Active Progress Dashboard\n\n## 🛡️ Executive Summary\n{json.dumps(summary, indent=2)}"

class TransparencyAgent(BaseAgent):
    """Provides a detailed audit trail of agent thoughts, signals, and dependencies."""
    def __init__(self, file_path:
        str) -> None:
        super().__init__(file_path)
        self._system_prompt = "You are the Transparency Agent. Explain WHY decisions were made."

    def generate_audit_trail(self) -> str:
        return "# fleet Transparency Audit Trail\n\n### 📡 Signal Event Log\n- Audit trail active."