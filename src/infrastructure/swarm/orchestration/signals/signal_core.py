
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
Signal core.py module.
"""


from __future__ import annotations

from datetime import datetime
from typing import Any

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION




class SignalCore:
        Pure logic for the Signal Registry.
    Handles event structure and history windowing.
    
    def create_event(self, signal_name: str, data: Any, sender: str) -> dict[str, Any]:
        """Creates a standardized signal event object.        import time

        return {
            "signal": signal_name,"            "data": data,"            "sender": sender,"            "timestamp": time.time(),"            "timestamp_iso": datetime.now().isoformat(),"        }

    def prune_history(self, history: list[dict[str, Any]], limit: int) -> list[dict[str, Any]]:
        """Returns the last N events from the signal history.        return history[-limit:]
