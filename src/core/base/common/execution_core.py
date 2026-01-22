<<<<<<< HEAD
<<<<<<< HEAD
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
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.
=======
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
"""
Unified Execution Core for PyAgent.
Handles concurrent, parallel, and serial task orchestration.
"""

from __future__ import annotations
<<<<<<< HEAD
<<<<<<< HEAD

import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable, List

from .base_core import BaseCore
=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from typing import Any, List, Callable, Optional
<<<<<<< HEAD
<<<<<<< HEAD
from src.core.base.common.base_core import BaseCore
<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
from .base_core import BaseCore
>>>>>>> 8d4d334f2 (chore: stabilize rust_core and resolve pylint diagnostics in base common cores)
=======
from .base_core import BaseCore
>>>>>>> 2a6f2626e (chore: stabilize rust_core and resolve pylint diagnostics in base common cores)

try:
    import rust_core as rc
except ImportError:
    rc = None

<<<<<<< HEAD
<<<<<<< HEAD

=======
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
class ExecutionCore(BaseCore):
    """
    Standard implementation for task orchestration.
    Supports ThreadPool, ProcessPool, and native Rust-based async scheduling.
    """
<<<<<<< HEAD
<<<<<<< HEAD

    def __init__(self, max_workers: int = 4) -> None:
=======
    
    def __init__(self, max_workers: int = 4):
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
    
    def __init__(self, max_workers: int = 4):
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        super().__init__()
        self.max_workers = max_workers
        self._thread_pool = ThreadPoolExecutor(max_workers=max_workers)

    async def execute_parallel(self, tasks: List[Callable]) -> List[Any]:
        """Executes a list of callables in parallel using threads."""
        if rc and hasattr(rc, "execute_parallel_rust"):
<<<<<<< HEAD
<<<<<<< HEAD
            return rc.execute_parallel_rust(tasks)  # pylint: disable=no-member

=======
            return rc.execute_parallel_rust(tasks)
            
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
            return rc.execute_parallel_rust(tasks)
            
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        loop = asyncio.get_event_loop()
        futures = [loop.run_in_executor(self._thread_pool, task) for task in tasks]
        return await asyncio.gather(*futures)

    def map_seq(self, func: Callable, items: List[Any]) -> List[Any]:
        """Sequenced map implementation."""
        return [func(item) for item in items]
