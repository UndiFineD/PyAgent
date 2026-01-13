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
from datetime import datetime

__version__ = VERSION

class SignalCore:
    """
    Pure logic for the Signal Registry.
    Handles event structure and history windowing.
    """

    def create_event(self, signal_name: str, data: Any, sender: str) -> Dict[str, Any]:
        """Creates a standardized signal event object."""
        return {
            "signal": signal_name,
            "data": data,
            "sender": sender,
            "timestamp": datetime.now().isoformat()
        }

    def prune_history(self, history: List[Dict[str, Any]], limit: int) -> List[Dict[str, Any]]:
        """Returns the last N events from the signal history."""
        return history[-limit:]