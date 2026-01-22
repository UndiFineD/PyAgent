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
Engine Coordinator (V2) for Phase 54.
Manages the lifecycle of the inference engine, error recovery, and async state transitions.
"""

<<<<<<< HEAD
import asyncio
import logging
=======
import logging
import asyncio
from typing import Dict, List, Optional, Any
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
from enum import Enum

try:
    import rust_core as rc
except ImportError:
    rc = None

logger = logging.getLogger(__name__)

<<<<<<< HEAD

class EngineState(Enum):
    """
    Possible states for the EngineCoordinator.
    """
=======
class EngineState(Enum):
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
    STARTING = 0
    RUNNING = 1
    COOLDOWN = 2
    ERROR = 3
    STOPPED = 4

<<<<<<< HEAD

=======
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
class EngineCoordinator:
    """
    Coordinates the global engine state and recovery procedures.
    Integrates with Rust for high-throughput state transitions.
    """
<<<<<<< HEAD

    def __init__(self) -> None:
        self.state = EngineState.STOPPED
        self._error_count = 0
        self._max_errors = 5

    def transition_to(self, new_state: EngineState) -> None:
=======
    
    def __init__(self):
        self.state = EngineState.STOPPED
        self._error_count = 0
        self._max_errors = 5
        
    def transition_to(self, new_state: EngineState):
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        """
        Transitions the engine to a new state with safety checks.
        """
        old_state = self.state
<<<<<<< HEAD

        if rc and hasattr(rc, "engine_state_transition_rust"):
            rc.engine_state_transition_rust(old_state.value, new_state.value)

        self.state = new_state
        logger.info(f"Engine transitioned from {old_state.name} to {new_state.name}")

    async def handle_error(self, error_msg: str) -> bool:
=======
        
        if rc and hasattr(rc, "engine_state_transition_rust"):
            rc.engine_state_transition_rust(old_state.value, new_state.value)
            
        self.state = new_state
        logger.info(f"Engine transitioned from {old_state.name} to {new_state.name}")

    async def handle_error(self, error_msg: str):
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        """
        Self-healing logic for engine errors.
        """
        self._error_count += 1
        logger.error(f"Engine Error #{self._error_count}: {error_msg}")
<<<<<<< HEAD

        if self._error_count >= self._max_errors:
            self.transition_to(EngineState.ERROR)
            return False

=======
        
        if self._error_count >= self._max_errors:
            self.transition_to(EngineState.ERROR)
            return False
            
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        # Attempt soft restart
        self.transition_to(EngineState.COOLDOWN)
        await asyncio.sleep(1.0)
        self.transition_to(EngineState.RUNNING)
        return True

<<<<<<< HEAD
    def reset_stats(self) -> None:
=======
    def reset_stats(self):
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        """Resets coordinator statistics."""
        self._error_count = 0
        if self.state == EngineState.ERROR:
            self.transition_to(EngineState.STOPPED)
<<<<<<< HEAD

=======
            
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
    def is_healthy(self) -> bool:
        """Returns True if the engine is in a functional state."""
        return self.state in [EngineState.RUNNING, EngineState.STARTING, EngineState.COOLDOWN]
