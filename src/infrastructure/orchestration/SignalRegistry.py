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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""A simple event-driven signal registry for inter-agent communication."""

from __future__ import annotations
from src.core.base.version import VERSION
import logging
from typing import Dict, List, Callable, Any
from .SignalCore import SignalCore

__version__ = VERSION

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
            cls._instance.capabilities: Dict[str, List[str]] = {} # Phase 241: agent_name -> capabilities
            
            # Phase 241: Automatically subscribe to capability registration
            cls._instance.subscribe("agent_capability_registration", cls._instance._on_capability_registration)
        return cls._instance

    def _on_capability_registration(self, event: Dict[str, Any]) -> None:
        """Phase 241: Handles capability registration signals."""
        data = event.get("data", {})
        agent = data.get("agent")
        caps = data.get("capabilities", [])
        if agent:
            self.capabilities[agent] = caps
            logging.debug(f"SignalRegistry: Registered capabilities for {agent}: {caps}")

    def get_agent_by_capability(self, capability: str) -> List[str]:
        """Phase 241: Returns a list of agents that possess a specific capability."""
        return [agent for agent, caps in self.capabilities.items() if capability in caps]

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