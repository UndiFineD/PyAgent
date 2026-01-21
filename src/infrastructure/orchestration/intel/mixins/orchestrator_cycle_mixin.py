# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

import logging
from typing import Any
from src.core.base.version import is_gate_open

class OrchestratorCycleMixin:
    """Methods for managing the improvement cycle and gates."""

    def run_improvement_cycle(self, target_dir: str = "src") -> dict[str, Any]:
        """Runs a full scan and fix cycle across the specified directory."""
        if not self._check_gate_stability():
            return {
                "error": "Stability gate closed - system requires manual stabilization"
            }

        logging.info(f"Self-Improvement: Starting cycle for {target_dir}...")
        self._ingest_hive_tasks()

        results: dict[str, Any] = {
            "files_scanned": 0,
            "issues_found": 0,
            "fixes_applied": 0,
            "details": [],
        }

        debt_records: list[tuple[str, str, str, int, float]] = self._scan_and_repair_files(target_dir, results)
        self._record_debt_to_sql(debt_records)
        self._log_results(results)

        # Extract intelligence and perform DB maintenance
        lessons: list[str] | None = self._evaluate_and_optimize(results)

        # Self-Research: Update the roadmap (Phase 104)
        self.analysis.update_research_report(results, lessons=lessons)

        return results

    def _check_gate_stability(self) -> bool:
        """Verifies if the system is stable enough for autonomous changes."""
        from src.core.base.version import STABILITY_SCORE
        if not is_gate_open(100) or STABILITY_SCORE < 0.8:
            logging.error(
                f"Self-Improvement: System stability too low ({STABILITY_SCORE}) for autonomous code modification."
            )
            return False
        return True

    def _ingest_hive_tasks(self) -> None:
        """Ingests actionable tasks from Collective Intelligence."""
        self.active_tasks = []
        if self.fleet and hasattr(self.fleet, "intelligence"):
            try:
                self.active_tasks = (
                    self.fleet.intelligence.get_actionable_improvement_tasks()
                )
                if self.active_tasks:
                    logging.info(
                        f"Self-Improvement: Hive mind provided {len(self.active_tasks)} actionable tasks."
                    )
            except Exception as e:
                logging.debug(f"Hive task ingestion failed: {e}")
