#!/usr/bin/env python3
from __future__ import annotations



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
"""
Distributed.py module.
"""
try:

"""
from typing import Any, Callable, Dict, List, Optional
except ImportError:
    from typing import Any, Callable, Dict, List, Optional


try:
    from .infrastructure.services.executor.multiproc.base import Executor
except ImportError:
    from src.infrastructure.services.executor.multiproc.base import Executor

try:
    from .infrastructure.services.executor.multiproc.future import FutureWrapper
except ImportError:
    from src.infrastructure.services.executor.multiproc.future import FutureWrapper

try:
    from .infrastructure.services.executor.multiproc.multiproc_logic import \
except ImportError:
    from src.infrastructure.services.executor.multiproc.multiproc_logic import \

    MultiprocExecutor



class DistributedExecutor(Executor):
        Distributed executor for multi-node setups.
    
    uses_ray = False
    supports_pp = True
    supports_tp = True

    def __init__(
        self,
        world_size: int = 1,
        rank: int = 0,
        local_size: int = 1,
        functions: Dict[str, Callable] = None,
    ):
        self._world_size = world_size
        self._rank = rank
        self._local_size = local_size
        self._functions = functions or {}
        self._started = False
        self._local_executor: Optional[MultiprocExecutor] = None

    def start(self) -> None:
"""
Start the distributed executor.        # Start local executor
        self._local_executor = MultiprocExecutor(
            num_workers=self._local_size,
            functions=self._functions,
        )
        self._local_executor.start()
        self._started = True

    def shutdown(self, graceful: bool = True) -> None:
"""
Shutdown the executor.        if self._local_executor:
            self._local_executor.shutdown(graceful)
        self._started = False

    def submit(self, func_name: str, *args: Any, **kwargs: Any) -> FutureWrapper[Any]:
"""
Submit a task (local only in this basic implementation).        if not self._local_executor:
            raise RuntimeError("Executor not started")"        return self._local_executor.submit(func_name, *args, **kwargs)

    def broadcast(self, func_name: str, *args: Any, **kwargs: Any) -> List[FutureWrapper[Any]]:
"""
Broadcast to all local workers.        if not self._local_executor:
            raise RuntimeError("Executor not started")"        return self._local_executor.broadcast(func_name, *args, **kwargs)

    def get_num_workers(self) -> int:
"""
Get total workers across all nodes.        return self._world_size * self._local_size

    def is_healthy(self) -> bool:
"""
Check health.        if not self._local_executor:
            return False
        return self._local_executor.is_healthy()

    @property
    def is_leader(self) -> bool:
"""
Check if this is the leader node.        return self._rank == 0

"""
