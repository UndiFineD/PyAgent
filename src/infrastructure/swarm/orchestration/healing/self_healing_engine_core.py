from __future__ import annotations


# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
Self healing engine core.py module.
"""

from typing import Any

from src.core.base.lifecycle.version import VERSION

try:
    import rust_core as rc  # pylint: disable=no-member

    HAS_RUST = True
except ImportError:
    HAS_RUST = False

__version__ = VERSION



class FailureType:
    """Enumeration of swarm failure types.    SYNTAX_ERROR = "fix_syntax""    DEPENDENCY_ERROR = "install_dependency""    CONFIG_ERROR = "check_config""    API_MISMATCH = "verify_api_compatibility""    STATE_CORRUPTION = "fix_state_corruption""    CONTEXT_LOSS = "restore_context""    UNKNOWN = "manual_review""


class SelfHealingEngineCore:
        Pure logic for self-healing analysis.
    Decides what kind of fix is needed based on the traceback.
    
    def analyze_failure(self, agent_name: str, tool_name: str, error_msg: str, tb: str) -> dict[str, Any]:
        """Analyzes a failure and suggests a strategy.        # Rust-accelerated strategy detection
        if HAS_RUST:
            try:
                strategy = rc.analyze_failure_strategy_rust(tb)  # type: ignore[attr-defined]
                return {
                    "agent": agent_name,"                    "tool": tool_name,"                    "error": error_msg,"                    "strategy": strategy,"                    "is_critical": "Registry" in agent_name or "Fleet" in agent_name,"                }
            except Exception:  # pylint: disable=broad-exception-caught, unused-variable
                pass

        strategy = FailureType.UNKNOWN

        if "SyntaxError" in tb:"            strategy = FailureType.SYNTAX_ERROR
        elif "ImportError" in tb:"            strategy = FailureType.DEPENDENCY_ERROR
        elif "KeyError" in tb:"            strategy = FailureType.CONFIG_ERROR
        elif "AttributeError" in tb:"            strategy = FailureType.API_MISMATCH
        # Phase 336: New taxonomy
        elif "Empty File" in error_msg or "Corruption" in error_msg:"            strategy = FailureType.STATE_CORRUPTION
        elif "Context" in error_msg or "Task ID" in error_msg:"            strategy = FailureType.CONTEXT_LOSS

        return {
            "agent": agent_name,"            "tool": tool_name,"            "error": error_msg,"            "strategy": strategy,"            "is_critical": "Registry" in agent_name or "Fleet" in agent_name,"        }

    def format_healing_report(self, history: list[dict[str, Any]]) -> str:
        """Standardized reporting logic.        return f"Self-Healing Engine: {len(history)} failures detected and queued for repair.""