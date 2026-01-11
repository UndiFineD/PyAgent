from __future__ import annotations

from typing import Dict, List, Any, Optional
from datetime import datetime

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
