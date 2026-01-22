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

<<<<<<< HEAD
<<<<<<< HEAD
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.
=======
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
"""
Standardized Base for all stateful Managers in the swarm.
Inherits from BaseCore for lifecycle and I/O.
"""

<<<<<<< HEAD
<<<<<<< HEAD
import logging
from typing import Any, Dict, Optional

from .base_core import BaseCore


=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
from __future__ import annotations
import logging
from typing import Any, Dict
from .base_core import BaseCore

<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
class BaseManager(BaseCore):
    """
    Standard implementation for stateful Managers.
    Provides a dictionary-based state cache and standard operations.
    """
<<<<<<< HEAD
<<<<<<< HEAD

    def __init__(self, name: Optional[str] = None) -> None:
=======
    
    def __init__(self, name: str | None = None) -> None:
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
    
    def __init__(self, name: str | None = None) -> None:
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        super().__init__()
        self._name = name or self.__class__.__name__
        self._state: Dict[str, Any] = {}
        self._logger = logging.getLogger(f"pyagent.manager.{self._name.lower()}")

    def set_state(self, key: str, value: Any) -> None:
        """Set a state value in the manager's cache."""
        self._state[key] = value
<<<<<<< HEAD
<<<<<<< HEAD
        self._logger.debug("State set: %s = %s", key, value)
=======
        self._logger.debug(f"State set: {key} = {value}")
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
        self._logger.debug(f"State set: {key} = {value}")
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)

    def get_state(self, key: str, default: Any = None) -> Any:
        """Retrieve a state value from the manager's cache."""
        return self._state.get(key, default)

    def clear_state(self) -> None:
        """Clear the manager's state cache."""
        self._state.clear()
        self._logger.debug("State cleared.")

    def __repr__(self) -> str:
        return f"<{self._name} state_count={len(self._state)}>"
