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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Background Agent Execution Manager for the PyAgent GUI."""

from __future__ import annotations
from src.core.base.version import VERSION
from typing import Any, Dict, List
import threading
import logging
import tkinter as tk
from src.interface.ui.gui.WidgetLogger import WidgetLogger

__version__ = VERSION

class AgentRunner:
    """Manages background threads and execution lifecycle for agents."""
    def __init__(self, callbacks) -> None:
        self.callbacks: Any = callbacks
        self.history = {} # Store history per agent instance

    def run_agent(self, column) -> None:
        cfg = column.get_config()
        agent_type = cfg["type"]
        cfg["backend"]
        agent_id: int = id(column)
        
        # Initialize history for this instance if not present
        if agent_id not in self.history:
            self.history[agent_id] = []
            
        # Get content from callbacks
        global_ctx: str = ""
        if "get_global_context" in self.callbacks:
            global_ctx = self.callbacks["get_global_context"]()
            
        column.on_start()
        column.stop_event = threading.Event()
        
        # Setup specific logger
        logger_name: str = f"agent_{agent_id}"
        logger: logging.Logger = logging.getLogger(logger_name)
        logger.setLevel(logging.INFO)
        for h in logger.handlers[:]:
            logger.removeHandler(h)
        logger.addHandler(WidgetLogger(column.log_text, thread_id=None)) 

        def task() -> None:
            try:
                # Add current request to history
                prompt = column.prompt_text.get("1.0", tk.END).strip()
                self.history[agent_id].append({"role": "user", "content": prompt})

                # Truncate memory based on model limits
                from .Constants import MODEL_TOKENS
                limit: int = MODEL_TOKENS.get(cfg["model"], MODEL_TOKENS["default"])
                self.optimize_memory(agent_id, limit)

                # Dynamic import implementation
                module_map: dict[str, str] = {
                    "Coder": "src.agent_coder", 
                    "Developer": "src.agent_coder",
                    "Architect": "src.agent_architect",
                    "PM": "src.agent_pm",
                    "Analyst": "src.agent_pm",
                    "Reviewer": "src.agent_reviewer",
                    "Test Architect": "src.agent_tester",
                    "UX Designer": "src.agent_ux",
                    "BMad Master": "src.agent_master",
                    "Scrum Master": "src.agent_pm",
                    "Security Auditor": "src.agent_security"
                }
                module_map.get(agent_type, "src.agent_coder")
                
                logger.info(f"Initialized {agent_type} agent on thread.")
                logger.info(f"Target Scope: {cfg['file'] or 'Workspace'}")
                logger.info(f"Context Snippet: {global_ctx[:50]}...")
                logger.info(f"Memory Depth: {len(self.history[agent_id])} turns")
                
                # Simulation - In a real app we'd call the backend here
                # result = backend_call(self.history[agent_id], global_ctx, agent_type)
                
                for i in range(5):
                    if column.stop_event.is_set():
                        logger.warning("Execution aborted by user.")
                        return
                    logger.info(f"Processing chunk {i+1}/5...")
                    column.stop_event.wait(timeout=1.0)
                
                # Update history with a mock response
                mock_response: str = f"Simulated response from {agent_type}."
                self.history[agent_id].append({"role": "assistant", "content": mock_response})

                logger.info("Agent execution completed successfully.")
                if "set_status" in self.callbacks:
                    self.callbacks["set_status"](f"{agent_type} agent finished.")
            except Exception as e:
                logger.error(f"Agent Failure: {str(e)}")
            finally:
                column.on_finish()

        thread = threading.Thread(target=task, daemon=True)
        column.running_thread = thread
        thread.start()

    def stop_agent(self, column, reset_history=False) -> None:
        if hasattr(column, 'stop_event') and column.stop_event:
            column.stop_event.set()
            if "set_status" in self.callbacks:
                self.callbacks["set_status"]("Stopping agent...")
        
        if reset_history:
            agent_id: int = id(column)
            if agent_id in self.history:
                self.history[agent_id] = []

    def get_history(self, column: Any) -> list[dict[str, Any]]:
        """Returns the conversation history for a specific agent column."""
        return self.history.get(id(column), [])

    def set_history(self, column, new_history) -> None:
        """Updates the conversation history for a specific agent column."""
        self.history[id(column)] = new_history

    def optimize_memory(self, agent_id, token_limit) -> None:
        """Truncates history if it exceeds estimated token limit, preserving marked messages."""
        chars_per_token = 4 # Simple heuristic
        char_limit = token_limit * chars_per_token
        
        current_history = self.history.get(agent_id, [])
        total_chars: int = sum(len(m["content"]) for m in current_history)
        
        # Start dropping from the beginning, but skip "keep" messages
        i = 0
        while total_chars > char_limit and i < len(current_history) - 2:
            # Check if this exchange should be kept
            msg_user = current_history[i]
            msg_assist = current_history[i+1]
            
            if msg_user.get("metadata", {}).get("keep") or msg_assist.get("metadata", {}).get("keep"):
                i += 2
                continue
                
            # Drop earliest exchange
            removed_user = current_history.pop(i)
            removed_assist = current_history.pop(i)
            total_chars -= (len(removed_user["content"]) + len(removed_assist["content"]))
            logging.info(f"Optimized memory for agent {agent_id}: dropped exchange at index {i}.")
            # i stays same as we popped