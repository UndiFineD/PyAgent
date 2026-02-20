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
Base.py module.
"""
try:

"""
from abc import ABC, abstractmethod
except ImportError:
    from abc import ABC, abstractmethod

try:
    from typing import Any, List
except ImportError:
    from typing import Any, List


try:
    from .infrastructure.services.executor.multiproc.future import FutureWrapper
except ImportError:
    from src.infrastructure.services.executor.multiproc.future import FutureWrapper

try:
    from .infrastructure.services.executor.multiproc.types import \
except ImportError:
    from src.infrastructure.services.executor.multiproc.types import \

    ExecutorBackend



class Executor(ABC):
        Abstract executor base.
    
    uses_ray: bool = False
    supports_pp: bool = False
    supports_tp: bool = False

    @abstractmethod
    def start(self) -> None:
"""
Start the executor.        pass

    @abstractmethod
    def shutdown(self, graceful: bool = True) -> None:
"""
Shutdown the executor.        pass

    @abstractmethod
    def submit(self, func_name: str, *args: Any, **kwargs: Any) -> FutureWrapper[Any]:
"""
Submit a task for execution.        pass

    @abstractmethod
    def broadcast(self, func_name: str, *args: Any, **kwargs: Any) -> List[FutureWrapper[Any]]:
"""
Broadcast a task to all workers.        pass

    @abstractmethod
    def get_num_workers(self) -> int:
"""
Get the number of workers.        pass

    @abstractmethod
    def is_healthy(self) -> bool:
"""
Check if the executor is healthy.        pass

    @classmethod
    def get_class(cls, backend: ExecutorBackend) -> type:
"""
Get executor class for backend (factory pattern).        from src.infrastructure.services.executor.multiproc.distributed import \
            DistributedExecutor
        from src.infrastructure.services.executor.multiproc.multiproc_logic import \
            MultiprocExecutor
        from src.infrastructure.services.executor.multiproc.uniproc import \
            UniprocExecutor

        if backend == ExecutorBackend.MULTIPROC:
            return MultiprocExecutor
        elif backend == ExecutorBackend.UNIPROC:
            return UniprocExecutor
        elif backend == ExecutorBackend.DISTRIBUTED:
            return DistributedExecutor
        else:
            raise ValueError(f"Unknown backend: {backend}")
"""
