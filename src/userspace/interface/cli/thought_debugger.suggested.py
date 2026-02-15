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
Thought debugger.py module.
"""
# Phase 269: Interactive Thought Debugger

from __future__ import annotations

import logging
import sys
import time
from typing import Any

from src.core.base.lifecycle.version import VERSION
from src.infrastructure.swarm.orchestration.signals.signal_registry import SignalRegistry


class ThoughtDebugger:
    """
    Interactive CLI tool for real-time inspection of agent reasoning (thoughts).
    Subscribes to the 'thought_stream' signal and provides formatting and control.
    """

    def __init__(self, interactive: bool = True) -> None:
        self.signals = SignalRegistry()
        self.interactive = interactive
        self.thought_count = 0
        self.active = False

    def start(self) -> None:
        """Starts the debugger session. Use in a threaded or async context for non-blocking."""
        print(f"--- PyAgent Thought Debugger v{VERSION} ---")
        print(f"Mode: {'Interactive' if self.interactive else 'Passive Monitor'}")
        print("Waiting for thoughts from the swarm... (Ctrl+C to exit)\n")

        self.signals.subscribe("thought_stream", self._handle_thought)
        self.active = True

        try:
            # If we're the main entry point, block here using event-driven approach
            if __name__ == "__main__":
                import asyncio

                loop = asyncio.new_event_loop()
                loop.run_forever()
        except KeyboardInterrupt:
            self.stop()
        finally:
            pass

    def stop(self) -> None:
        """Stops the debugger session."""
        self.active = False
        print("\nDebugger session terminated.")

    def _handle_thought(self, event: dict[str, Any]) -> None:
        """Callback for thought_stream signals."""
        self.thought_count += 1
        data = event.get("data", {})
        agent = data.get("agent", "Unknown")
        thought = data.get("thought", "...")
        timestamp = event.get("timestamp", time.strftime("%H:%M:%S"))

        print(f"\r[{timestamp}] [{agent}] THOUGHT #{self.thought_count}:")
        print(f"  > {thought}")

        if self.interactive:
            # Note: This will block the thread emitting the signal!

            # In a live fleet, this acts as a 'breakpoint'.
            choice = input("\n[DEBUG] (ENTER=Continue, q=Quit, m=Menu): ").lower().strip()
            if choice == "q":
                self.stop()

                sys.exit(0)
            elif choice == "m":
                self._show_menu(data)
            else:
                print("Continuing...\n")

    def _show_menu(self, data: dict[str, Any]) -> None:
        """Displays extended thought metadata and controls."""
        print("\n--- Thought Metadata ---")
        for k, v in data.items():
            if k != "thought":
                print(f"  {k}: {v}")
        print("------------------------")
        input("Press ENTER to return to thought stream...")


if __name__ == "__main__":
    # Configure logging to not interfere too much with stdout
    logging.basicConfig(level=logging.WARNING)

    # If run directly, start the passive monitor or interactive REPL
    interactive_mode = "--passive" not in sys.argv
    debugger = ThoughtDebugger(interactive=interactive_mode)
    debugger.start()
