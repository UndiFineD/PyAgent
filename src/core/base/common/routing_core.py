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
<<<<<<< HEAD
<<<<<<< HEAD

import os
from typing import Any, Dict, Optional

from .base_core import BaseCore

try:
    import rust_core as rc  # pylint: disable=import-error
except ImportError:
    rc = None

=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
import logging
import os
from typing import Any, List, Dict, Optional
from .base_core import BaseCore

try:
    import rust_core as rc
except ImportError:
    rc = None

logger = logging.getLogger("pyagent.routing")
<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)

class RoutingCore(BaseCore):
    """
    Authoritative engine for task routing and provider selection.
    Balances latency, cost, and quality metrics across backend providers.
    """
<<<<<<< HEAD
<<<<<<< HEAD

=======
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
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
<<<<<<< HEAD
<<<<<<< HEAD
        performance_report: Optional[Dict[str, Any]] = None,
=======
        performance_report: Optional[Dict[str, Any]] = None
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
        performance_report: Optional[Dict[str, Any]] = None
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
    ) -> str:
        """
        Optimal provider selection logic.
        Hot path for Rust acceleration in docs/RUST_MAPPING.md.
        """
<<<<<<< HEAD
<<<<<<< HEAD
        if rc and hasattr(rc, "select_provider_rust"):  # pylint: disable=no-member
            try:
                return rc.select_provider_rust(  # pylint: disable=no-member
                    task_type, priority, performance_report or {}
                )  # type: ignore
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
 # pylint: disable=broad-exception-caught
                pass

=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        if rc and hasattr(rc, "select_provider_rust"):
            try:
                return rc.select_provider_rust(task_type, priority, performance_report or {})
            except Exception:
                pass
        
<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        # Default logic (can be expanded with weighted averages)
        if performance_report:
            # Simple heuristic: lower latency for "latency" priority
            if priority == "latency":
                best_p = min(performance_report.items(), key=lambda x: x[1].get("avg_latency", 999))[0]
                if best_p in self.providers:
                    return best_p
<<<<<<< HEAD
<<<<<<< HEAD

=======
        
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
        
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        return os.environ.get("DV_AGENT_BACKEND", "github_models")
