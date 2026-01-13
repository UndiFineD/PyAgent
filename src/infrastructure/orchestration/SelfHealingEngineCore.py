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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

from __future__ import annotations
from src.core.base.version import VERSION
from typing import Dict, List, Any

__version__ = VERSION

class SelfHealingEngineCore:
    """
    Pure logic for self-healing analysis.
    Decides what kind of fix is needed based on the traceback.
    """
    
    def analyze_failure(self, agent_name: str, tool_name: str, error_msg: str, tb: str) -> Dict[str, Any]:
        """Analyzes a failure and suggests a strategy."""
        strategy = "manual_review"
        
        if "SyntaxError" in tb:
            strategy = "fix_syntax"
        elif "ImportError" in tb:
            strategy = "install_dependency"
        elif "KeyError" in tb:
            strategy = "check_config"
        elif "AttributeError" in tb:
            strategy = "verify_api_compatibility"
            
        return {
            "agent": agent_name,
            "tool": tool_name,
            "error": error_msg,
            "strategy": strategy,
            "is_critical": "Registry" in agent_name or "Fleet" in agent_name
        }

    def format_healing_report(self, history: List[Dict[str, Any]]) -> str:
        """Standardized reporting logic."""
        return f"Self-Healing Engine: {len(history)} failures detected and queued for repair."