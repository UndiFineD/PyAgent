
"""
Complexity analysis mixin.py module.
"""
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

from __future__ import annotations

import logging
import os
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from src.infrastructure.swarm.orchestration.intel.self_improvement_analysis import \
        SelfImprovementAnalysis


class ComplexityAnalysisMixin:
    """Mixin for workspace-wide complexity scanning in SelfImprovementAnalysis."""

    def scan_workspace_complexity(self: SelfImprovementAnalysis, target_dir: str = "src") -> list[dict[str, Any]]:
        """
        Scans the workspace for high-complexity files using the Rust bridge.
        Returns a sorted list of complexity targets.
        """
        try:
            import rust_core as rc
        except ImportError:
            logging.warning("Self-Improvement: Rust core not found. Complexity scan using Python fallback.")
            return []

        targets: list[dict[str, Any]] = []
        scan_path = os.path.join(self.workspace_root, target_dir)

        for root, _, files in os.walk(scan_path):
            for file in files:
                if file.endswith(".py"):
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, self.workspace_root)
                    try:
                        with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()

                        comp = rc.calculate_cyclomatic_complexity(content)
                        if comp > 25:
                            targets.append({"file": rel_path, "complexity": comp, "type": "Complexity Issue"})
                    except Exception as e:
                        logging.debug(f"Complexity scan failed for {rel_path}: {e}")

        # Sort by complexity descending
        targets.sort(key=lambda x: x["complexity"], reverse=True)
        return targets
