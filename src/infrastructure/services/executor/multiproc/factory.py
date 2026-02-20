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
Factory.py module.
"""

try:
    from typing import Any, Callable, Dict
except ImportError:
    from typing import Any, Callable, Dict


try:
    from .infrastructure.services.executor.multiproc.base import Executor
except ImportError:
    from src.infrastructure.services.executor.multiproc.base import Executor

try:
    from .infrastructure.services.executor.multiproc.distributed import \
except ImportError:
    from src.infrastructure.services.executor.multiproc.distributed import \

    DistributedExecutor
try:
    from .infrastructure.services.executor.multiproc.multiproc_logic import \
except ImportError:
    from src.infrastructure.services.executor.multiproc.multiproc_logic import \

    MultiprocExecutor
try:
    from .infrastructure.services.executor.multiproc.types import \
except ImportError:
    from src.infrastructure.services.executor.multiproc.types import \

    ExecutorBackend
try:
    from .infrastructure.services.executor.multiproc.uniproc import \
except ImportError:
    from src.infrastructure.services.executor.multiproc.uniproc import \

    UniprocExecutor



class ExecutorFactory:
    """Factory for creating executors.
    @staticmethod
    def create(
        backend: ExecutorBackend,
        num_workers: int = 4,
        functions: Dict[str, Callable] = None,
        **kwargs: Any,
    ) -> Executor:
        """Create an executor.        if backend == ExecutorBackend.MULTIPROC:
            return MultiprocExecutor(num_workers=num_workers, functions=functions, **kwargs)
        elif backend == ExecutorBackend.UNIPROC:
            return UniprocExecutor(functions=functions)
        elif backend == ExecutorBackend.DISTRIBUTED:
            return DistributedExecutor(local_size=num_workers, functions=functions, **kwargs)
        else:
            raise ValueError(f"Unknown backend: {backend}")"