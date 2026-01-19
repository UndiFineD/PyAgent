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


"""Auto-extracted class from agent_stats.py"""

from __future__ import annotations
from src.core.base.Version import VERSION
from src.observability.stats.observability_core import Alert
from src.observability.stats.observability_core import AlertSeverity
from src.observability.stats.observability_core import Metric
from src.observability.stats.observability_core import MetricSnapshot
from src.observability.stats.observability_core import MetricType
from src.observability.stats.observability_core import RetentionPolicy
from src.observability.stats.observability_core import Threshold
from src.observability.stats.observability_core import StatsCore
from datetime import datetime
from pathlib import Path
from typing import Any
from collections.abc import Callable
import csv
import hashlib
import json
import logging
from src.observability.StructuredLogger import StructuredLogger
import zlib

__version__ = VERSION

logger = StructuredLogger(__name__)


class StatsAgent:
    """Reports statistics on file update progress."""

    def __init__(self, files: list[str]) -> None:
        self.files = [Path(f) for f in files]
        self.stats: dict[str, Any] = {}
        self._validate_files()
        # New features
        self._metrics: dict[str, list[Metric]] = {}
        self._custom_metrics: dict[str, Callable[[], float]] = {}
        self._snapshots: list[MetricSnapshot] = []
        self._thresholds: list[Threshold] = []
        self._alerts: list[Alert] = []
        self._retention_policies: dict[str, RetentionPolicy] = {}
        self._anomaly_scores: dict[str, list[float]] = {}
        self._metric_history: dict[str, list[tuple[str, float]]] = {}

    def _validate_files(self) -> None:
        """Validate input files."""
        if not self.files:
            raise ValueError("No files provided")
        invalid = [f for f in self.files if not f.exists()]
        if invalid:
            logging.warning(f"Files not found: {', '.join(map(str, invalid))}")
            # Filter out invalid files
            self.files = [f for f in self.files if f.exists()]
        if not self.files:
            raise ValueError("No valid files found after filtering")

    # ========== Custom Metrics ==========
    def register_custom_metric(
        self,
        name: str,
        metric_type: MetricType = MetricType.GAUGE,
        description: str = "",
    ) -> Metric:
        """Register a custom metric type."""
        if name not in self._custom_metrics:
            self._custom_metrics[name] = lambda: 0.0
        # Return a Metric object for the custom metric
        return Metric(
            name=name,
            value=0.0,
            metric_type=metric_type,
            timestamp=datetime.now().isoformat(),
        )

    def get_metric(self, name: str) -> Metric | None:
        """Get a registered metric by name."""
        if name in self._custom_metrics:
            if name in self._metrics and self._metrics[name]:
                value = self._metrics[name][-1].value
            else:
                value = 0.0
            return Metric(
                name=name,
                value=value,
                metric_type=MetricType.GAUGE,
                timestamp=datetime.now().isoformat(),
            )
        return None

    def collect_custom_metrics(self) -> dict[str, float]:
        """Collect all custom metrics."""
        results: dict[str, float] = {}
        for name in self._custom_metrics:
            if name in self._metrics and self._metrics[name]:
                # Get the latest value for this metric
                latest_metric = self._metrics[name][-1]
                results[name] = latest_metric.value
        return results

    def add_metric(
        self,
        name: str,
        value: float,
        metric_type: MetricType = MetricType.GAUGE,
        namespace: str = "default",
        tags: dict[str, str] | None = None,
    ) -> Metric:
        """Add a metric value."""
        metric = Metric(
            name=name,
            value=value,
            metric_type=metric_type,
            timestamp=datetime.now().isoformat(),
            namespace=namespace,
            tags=tags or {},
        )
        if name not in self._metrics:
            self._metrics[name] = []
        self._metrics[name].append(metric)

        # Compatibility history used by some tests.
        if name not in self._metric_history:
            self._metric_history[name] = []
        self._metric_history[name].append((metric.timestamp, float(metric.value)))

        # Check thresholds
        self._check_thresholds(metric)
        return metric

    def get_metric_history(self, name: str, limit: int = 100) -> list[Metric]:
        """Get metric history."""
        metrics = self._metrics.get(name, [])
        return metrics[-limit:]

    # ========== Anomaly Detection ==========
    def detect_anomaly(
        self, metric_name: str, value: float | None = None, threshold_std: float = 2.0
    ) -> bool | tuple[bool, float]:
        """Detect if a value is anomalous using standard deviation."""
        history = self._metrics.get(metric_name, [])
        if value is None:
            if not history:
                return False
            val_to_check = history[-1].value
            hist_to_check = history[:-1]
            is_anom, _ = StatsCore.detect_anomaly(
                hist_to_check, val_to_check, threshold_std
            )
            return is_anom

        is_anomaly, z_score = StatsCore.detect_anomaly(history, value, threshold_std)
        if metric_name not in self._anomaly_scores:
            self._anomaly_scores[metric_name] = []
        self._anomaly_scores[metric_name].append(z_score)
        return is_anomaly, z_score

    def get_anomaly_scores(self, metric_name: str) -> list[float]:
        """Get anomaly scores for a metric."""
        return self._anomaly_scores.get(metric_name, [])

    # ========== Thresholds & Alerting ==========
    def add_threshold(
        self,
        metric_name: str,
        min_value: float | None = None,
        max_value: float | None = None,
        severity: AlertSeverity | None = None,
        message: str = "",
        operator: str = "",  # deprecated, for backwards compatibility
        value: float = 0.0,  # deprecated, for backwards compatibility
    ) -> Threshold:
        """Add a threshold for alerting."""
        if severity is None:
            severity = AlertSeverity.MEDIUM

        # Backwards compatible operator/value support.
        # If caller used min/max thresholds, synthesize an operator/value pair
        # so downstream alert rendering has a single numeric threshold.
        if not operator:
            if max_value is not None and value == 0.0:
                operator = ">"
                value = float(max_value)
            elif min_value is not None and value == 0.0:
                operator = "<"
                value = float(min_value)
        threshold = Threshold(
            metric_name=metric_name,
            min_value=min_value,
            max_value=max_value,
            severity=severity,
            message=message or f"{metric_name} threshold",
            operator=operator,
            value=value,
        )
        self._thresholds.append(threshold)
        return threshold

    def remove_threshold(self, metric_name: str) -> bool:
        """Remove all thresholds for a metric."""
        original_count = len(self._thresholds)
        self._thresholds = [t for t in self._thresholds if t.metric_name != metric_name]
        return len(self._thresholds) < original_count

    def _check_thresholds(self, metric: Metric) -> None:
        """Check if metric breaches any thresholds."""
        for threshold in self._thresholds:
            if threshold.metric_name != metric.name:
                continue
            breached = False

            # Preferred API: min/max thresholds.
            if threshold.max_value is not None and metric.value > threshold.max_value:
                breached = True
            if threshold.min_value is not None and metric.value < threshold.min_value:
                breached = True

            # Legacy API: operator/value thresholds.
            if threshold.operator == ">" and metric.value > threshold.value:
                breached = True
            elif threshold.operator == "<" and metric.value < threshold.value:
                breached = True
            elif threshold.operator == ">=" and metric.value >= threshold.value:
                breached = True
            elif threshold.operator == "<=" and metric.value <= threshold.value:
                breached = True
            elif threshold.operator == "==" and metric.value == threshold.value:
                breached = True
            if breached:
                self._create_alert(metric, threshold)

    def _create_alert(self, metric: Metric, threshold: Threshold) -> Alert:
        """Create an alert."""
        threshold_value = threshold.value
        if threshold.max_value is not None:
            threshold_value = float(threshold.max_value)
        elif threshold.min_value is not None:
            threshold_value = float(threshold.min_value)
        alert = Alert(
            id=hashlib.md5(f"{metric.name}:{metric.timestamp}".encode()).hexdigest()[
                :8
            ],
            metric_name=metric.name,
            current_value=metric.value,
            threshold_value=threshold_value,
            severity=threshold.severity or AlertSeverity.MEDIUM,
            message=threshold.message,
            timestamp=datetime.now().isoformat(),
        )
        self._alerts.append(alert)
        logging.warning(f"Alert: {alert.message} (value={metric.value})")
        return alert

    def get_alerts(self, severity: AlertSeverity | None = None) -> list[Alert]:
        """Get alerts, optionally filtered by severity."""
        if severity:
            return [a for a in self._alerts if a.severity == severity]
        return self._alerts

    def clear_alerts(self) -> int:
        """Clear all alerts and return count."""
        count = len(self._alerts)
        self._alerts = []
        return count

    # ========== Snapshots ==========
    def create_snapshot(
        self, name: str = "", tags: dict[str, str] | None = None
    ) -> MetricSnapshot:
        """Create a snapshot of current metrics."""
        current_stats: dict[str, float] = {
            k: float(v) for k, v in self.calculate_stats().items()
        }
        custom: dict[str, float] = self.collect_custom_metrics()
        metrics: dict[str, float] = {**current_stats, **custom}
        snapshot = MetricSnapshot(
            name=name or f"snapshot_{len(self._snapshots)}",
            id=hashlib.md5(datetime.now().isoformat().encode()).hexdigest()[:8],
            timestamp=datetime.now().isoformat(),
            metrics=metrics,
            tags=tags or {},
        )
        self._snapshots.append(snapshot)
        return snapshot

    def get_snapshot(self, name: str) -> MetricSnapshot | None:
        """Get a snapshot by name."""
        return next((s for s in self._snapshots if s.name == name), None)

    def get_snapshots(self, limit: int = 100) -> list[MetricSnapshot]:
        """Get recent snapshots."""
        return self._snapshots[-limit:]

    def compare_snapshots(
        self, snapshot1_name: str, snapshot2_name: str
    ) -> dict[str, dict[str, float | int]]:
        """Compare two snapshots."""
        s1 = self.get_snapshot(snapshot1_name)
        s2 = self.get_snapshot(snapshot2_name)
        if not s1 or not s2:
            return {}
        return StatsCore.compare_snapshots(s1, s2)

    # ========== Retention Policies ==========
    def add_retention_policy(
        self,
        metric_name: str | None = None,
        namespace: str | None = None,
        max_age_days: int = 0,
        max_points: int = 0,
        compression_after_days: int = 7,
    ) -> RetentionPolicy:
        """Add a retention policy."""
        key = metric_name or namespace or ""
        policy = RetentionPolicy(
            metric_name=metric_name,
            namespace=namespace or "",
            max_age_days=max_age_days,
            max_points=max_points,
            compression_after_days=compression_after_days,
        )
        self._retention_policies[key] = policy
        return policy

    def apply_retention_policies(self) -> int:
        """Apply retention policies and return count of removed items."""
        return StatsCore.apply_retention(self._metrics, self._retention_policies)

    # ========== Forecasting ==========
    def forecast(self, metric_name: str, periods: int = 5) -> list[float]:
        """Simple linear forecasting for a metric."""
        return StatsCore.forecast(self._metrics.get(metric_name, []), periods)

    # ========== Data Compression ==========
    def compress_metrics(self, metric_name: str) -> bytes:
        """Compress metric history."""
        # Tests might seed _metric_history directly.
        if metric_name in self._metric_history:
            return zlib.compress(
                json.dumps(
                    [
                        {"timestamp": ts, "value": val}
                        for ts, val in self._metric_history[metric_name]
                    ]
                ).encode("utf-8")
            )
        return StatsCore.compress_metrics(self._metrics.get(metric_name, []))

    def decompress_metrics(
        self,
        compressed: bytes,
        metric_name: str | None = None,
        metric_type: MetricType = MetricType.GAUGE,
        namespace: str = "default",
    ) -> list[Any]:
        """Decompress metric data."""
        if not compressed:
            return []
        data = json.loads(zlib.decompress(compressed).decode("utf-8"))
        if not metric_name:
            return [
                (item.get("timestamp", ""), item.get("value", 0.0)) for item in data
            ]
        return [
            Metric(
                name=metric_name,
                value=item["value"],
                metric_type=metric_type,
                timestamp=item["timestamp"],
                namespace=namespace,
                tags=item.get("tags", {}),
            )
            for item in data
        ]

    # ========== Original Methods ==========
    def get_missing_items(self) -> dict[str, list[str]]:
        """Identify files missing specific auxiliary components."""
        missing: dict[str, list[str]] = {
            "context": [],
            "changes": [],
            "errors": [],
            "improvements": [],
            "tests": [],
        }
        for file_path in self.files:
            base = file_path.stem
            dir_path = file_path.parent
            if not (dir_path / f"{base}.description.md").exists():
                missing["context"].append(str(file_path))
            if not (dir_path / f"{base}.changes.md").exists():
                missing["changes"].append(str(file_path))
            if not (dir_path / f"{base}.errors.md").exists():
                missing["errors"].append(str(file_path))
            if not (dir_path / f"{base}.improvements.md").exists():
                missing["improvements"].append(str(file_path))
            if not (dir_path / f"test_{base}.py").exists():
                missing["tests"].append(str(file_path))
        return missing

    def calculate_stats(self) -> dict[str, int]:
        """Calculate statistics for each file."""
        total_files = len(self.files)
        files_with_context = 0
        files_with_changes = 0
        files_with_errors = 0
        files_with_improvements = 0
        files_with_tests = 0
        for file_path in self.files:
            base = file_path.stem
            dir_path = file_path.parent
            if (dir_path / f"{base}.description.md").exists():
                files_with_context += 1
            if (dir_path / f"{base}.changes.md").exists():
                files_with_changes += 1
            if (dir_path / f"{base}.errors.md").exists():
                files_with_errors += 1
            if (dir_path / f"{base}.improvements.md").exists():
                files_with_improvements += 1
            if (dir_path / f"test_{base}.py").exists():
                files_with_tests += 1
        self.stats = {
            "total_files": total_files,
            "files_with_context": files_with_context,
            "files_with_changes": files_with_changes,
            "files_with_errors": files_with_errors,
            "files_with_improvements": files_with_improvements,
            "files_with_tests": files_with_tests,
        }
        return self.stats

    def add_trend_analysis(self, previous_stats: dict[str, int]) -> dict[str, str]:
        """Compare current stats with previous run and calculate deltas."""
        deltas: dict[str, str] = {}
        for key, current_value in self.stats.items():
            previous_value = previous_stats.get(key, 0)
            delta = current_value - previous_value
            percentage_change = (delta / previous_value * 100) if previous_value else 0
            deltas[key] = f"{delta:+} ({percentage_change:.1f}%)"
        return deltas

    def visualize_stats(self) -> None:
        """Generate CLI graphs for stats visualization."""
        StatsCore.visualize_stats(self.stats)

    def track_code_coverage(self, coverage_report: str) -> None:
        """Track code coverage metrics from a coverage report."""
        with open(coverage_report) as file:
            coverage_data = json.load(file)
        self.stats["code_coverage"] = coverage_data.get("total_coverage", 0)

    def export_stats(self, output_path: str, formats: list[str]) -> None:
        """Export stats to multiple formats."""
        for fmt in formats:
            if fmt == "json":
                with open(f"{output_path}.json", "w") as json_file:
                    json.dump(self.stats, json_file, indent=2)
            elif fmt == "csv":
                with open(f"{output_path}.csv", "w", newline="") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(self.stats.keys())
                    writer.writerow(self.stats.values())
            elif fmt == "html":
                with open(f"{output_path}.html", "w") as html_file:
                    html_file.write("<html><body><h1>Stats Report</h1><table>")
                    for key, value in self.stats.items():
                        html_file.write(f"<tr><td>{key}</td><td>{value}</td></tr>")
                    html_file.write("</table></body></html>")
            elif fmt == "sqlite":
                import sqlite3

                conn = sqlite3.connect(f"{output_path}.db")
                cursor = conn.cursor()
                cursor.execute(
                    "CREATE TABLE IF NOT EXISTS stats (metric TEXT, value INTEGER)"
                )
                cursor.executemany(
                    "INSERT INTO stats (metric, value) VALUES (?, ?)",
                    self.stats.items(),
                )
                conn.commit()
                conn.close()

    def generate_comparison_report(self, baseline_stats: dict[str, int]) -> None:
        """Generate a comparison report between current and baseline stats."""
        comparison = {}
        for key, current_value in self.stats.items():
            baseline_value = baseline_stats.get(key, 0)
            comparison[key] = {
                "current": current_value,
                "baseline": baseline_value,
                "difference": current_value - baseline_value,
            }
        report = json.dumps(comparison, indent=2)
        logger.info(report)
        print(report)

    def report_stats(self, output_format: str = "text") -> None:
        """Print the statistics report."""
        stats = self.calculate_stats()
        total = stats["total_files"]

        if output_format == "json":
            logger.info(json.dumps(stats, indent=2))
        elif output_format == "csv":
            import io

            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(stats.keys())
            writer.writerow(stats.values())
            logger.info(output.getvalue())
        else:

            def fmt(count: int) -> str:
                if total > 0:
                    return f"{count}/{total} ({count / total * 100:.1f}%)"
                else:
                    return "0 / 0 (0.0%)"

            logger.info("=== Stats Report ===")
            logger.info(f"Total files: {total}")
            logger.info(f"Files with descriptions: {fmt(stats['files_with_context'])}")
            logger.info(f"Files with changelogs: {fmt(stats['files_with_changes'])}")
            logger.info(f"Files with error reports: {fmt(stats['files_with_errors'])}")
            logger.info(
                f"Files with improvements: {fmt(stats['files_with_improvements'])}"
            )
            logger.info(f"Files with tests: {fmt(stats['files_with_tests'])}")
            logger.info("====================")
