# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

import json
import time
import logging
from typing import Any

class OrchestratorResultsMixin:
    """Methods for evaluation and logging results."""

    def _evaluate_and_optimize(self, results: dict[str, Any]) -> list[Any] | None:
        """Performs intelligence review and database optimization after the cycle."""
        lessons = None
        try:
            logging.info("Self-Improvement: Reviewing local interaction shards for AI lessons...")
            lessons = self.analysis.review_ai_lessons(self.fleet, self.ai)
            if lessons:
                results["lessons_learned"] = len(lessons)
                logging.info(f"Self-Improvement: Extracted {len(lessons)} lessons.")

            if self.fleet and hasattr(self.fleet, "sql_metadata"):
                results["intelligence_summary"] = self.fleet.sql_metadata.get_intelligence_summary()

                logging.info("Self-Improvement: Optimizing relational metadata indices...")
                self.fleet.sql_metadata.optimize_db()
        except Exception as e:
            logging.error(f"Post-cycle evaluation or optimization failed: {e}")
        return lessons

    def _log_results(self, results: dict[str, Any]) -> None:
        """Persists the improvement result to a log file."""
        entry = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "summary": {
                "scanned": results["files_scanned"],
                "found": results["issues_found"],
                "fixed": results["fixes_applied"],
            },
        }
        try:
            with open(self.improvement_log, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception:
            pass
