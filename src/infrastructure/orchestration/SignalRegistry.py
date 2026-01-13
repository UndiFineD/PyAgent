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
import asyncio
import time
from typing import Dict, List, Any
from collections.abc import Callable, Coroutine
from .SignalCore import SignalCore

__version__ = VERSION

class SignalRegistry:
    """
    Central hub for publishing and subscribing to agent signals.
    Phase 279: Refactored emit to be async with history pruning.
    """
    
    _instance = None
    
    def __new__(cls, *args, **kwargs) -> SignalRegistry:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.subscribers = {} # signal_name -> list of callbacks
            cls._instance.history = []
            cls._instance.core = SignalCore()
            cls._instance.capabilities: dict[str, list[str]] = {} # Phase 241: agent_name -> capabilities
            
            # Phase 241: Automatically subscribe to capability registration
            # Note: We keep this synchronous for now as it's an internal bootstrap
            cls._instance.subscribe("agent_capability_registration", cls._instance._on_capability_registration)
        return cls._instance

    def _on_capability_registration(self, event: dict[str, Any]) -> None:
        """Phase 241: Handles capability registration signals."""
        data = event.get("data", {})
        agent = data.get("agent")
        caps = data.get("capabilities", [])
        if agent:
            self.capabilities[agent] = caps
            logging.debug(f"SignalRegistry: Registered capabilities for {agent}: {caps}")

    def get_agent_by_capability(self, capability: str) -> list[str]:
        """Phase 241: Returns a list of agents that possess a specific capability."""
        return [agent for agent, caps in self.capabilities.items() if capability in caps]

    def subscribe(self, signal_name: str, callback: Callable[[Any], None | Coroutine[Any, Any, None]]) -> None:
        """Subscribe a callback to a signal."""
        if signal_name not in self.subscribers:
            self.subscribers[signal_name] = []
        self.subscribers[signal_name].append(callback)
        logging.debug(f"Subscribed callback to signal: {signal_name}")

    async def emit(self, signal_name: str, data: Any = None, sender: str = "system") -> None:
        """Emit a signal to all subscribers (Async Phase 279)."""
        event = self.core.create_event(signal_name, data, sender)
        self.history.append(event)
        
        # Phase 279: History pruning (discard > 1 hour old)
        now = time.time()
        one_hour_ago = now - 3600
        self.history = [e for e in self.history if e.get("timestamp", now) > one_hour_ago]
        
        logging.info(f"Signal emitted: {signal_name} from {sender}")
        
        if signal_name in self.subscribers:
            tasks = []
            for callback in self.subscribers[signal_name]:
                try:
                    if asyncio.iscoroutinefunction(callback):
                        tasks.append(callback(event))
                    else:
                        callback(event) # Legacy sync callback
                except Exception as e:
                    logging.error(f"Error in signal callback for {signal_name}: {e}")
            
            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)

    def get_history(self, limit: int = 50) -> list[dict[str, Any]]:
        """Get the recent signal history."""
        return self.core.prune_history(self.history, limit)