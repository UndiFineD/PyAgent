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

"""
Core logic for performance-based routing and task distribution.
"""

from __future__ import annotations

import os
from typing import Any, Dict, Optional

from .base_core import BaseCore

try:
    import rust_core as rc  # pylint: disable=import-error
except ImportError:
    rc = None


class RoutingCore(BaseCore):
    """
    Authoritative engine for task routing and provider selection.
    Balances latency, cost, and quality metrics across backend providers.
    """

    def __init__(self) -> None:
        super().__init__()
        self.providers = [
            "github_models",
            "openai",
            "codex",
            "local",
            "federated_cluster",
        ]

    def select_best_provider(
        self,
        task_type: str = "general",
        priority: str = "balanced",
        performance_report: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Optimal provider selection logic.
        Hot path for Rust acceleration in docs/RUST_MAPPING.md.
        """
        if rc and hasattr(rc, "select_provider_rust"):  # pylint: disable=no-member
            try:
                return rc.select_provider_rust(  # pylint: disable=no-member
                    task_type, priority, performance_report or {}
                )  # type: ignore
            except Exception:  # pylint: disable=broad-exception-caught
                pass

        # Default logic (can be expanded with weighted averages)
        if performance_report:
            # Simple heuristic: lower latency for "latency" priority
            if priority == "latency":
                best_p = min(performance_report.items(), key=lambda x: x[1].get("avg_latency", 999))[0]
                if best_p in self.providers:
                    return best_p

        return os.environ.get("DV_AGENT_BACKEND", "github_models")
