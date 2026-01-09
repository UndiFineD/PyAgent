#!/usr/bin/env python3

"""A simple event-driven signal registry for inter-agent communication."""

import logging
from typing import Dict, List, Callable, Any, Optional
from datetime import datetime

from .SignalCore import SignalCore

class SignalRegistry:
    """
    Central hub for publishing and subscribing to agent signals.
    Shell for SignalCore.
    """
    
    _instance = None
    
    def __new__(cls, *args, **kwargs) -> "SignalRegistry":
        if cls._instance is None:
            cls._instance = super(SignalRegistry, cls).__new__(cls)
            cls._instance.subscribers = {} # signal_name -> list of callbacks
            cls._instance.history = []
            cls._instance.core = SignalCore()
        return cls._instance

    def subscribe(self, signal_name: str, callback: Callable[[Any], None]) -> None:
        """Subscribe a callback to a signal."""
        if signal_name not in self.subscribers:
            self.subscribers[signal_name] = []
        self.subscribers[signal_name].append(callback)
        logging.debug(f"Subscribed callback to signal: {signal_name}")

    def emit(self, signal_name: str, data: Any = None, sender: str = "system") -> None:
        """Emit a signal to all subscribers."""
        event = self.core.create_event(signal_name, data, sender)
        self.history.append(event)
        
        logging.info(f"Signal emitted: {signal_name} from {sender}")
        
        if signal_name in self.subscribers:
            for callback in self.subscribers[signal_name]:
                try:
                    callback(event)
                except Exception as e:
                    logging.error(f"Error in signal callback for {signal_name}: {e}")

    def get_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get the recent signal history."""
        return self.core.prune_history(self.history, limit)
