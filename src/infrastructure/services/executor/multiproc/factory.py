#!/usr/bin/env python3

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

from __future__ import annotations

from typing import Any, Callable, Dict

from src.infrastructure.services.executor.multiproc.base import Executor
from src.infrastructure.services.executor.multiproc.distributed import \
    DistributedExecutor
from src.infrastructure.services.executor.multiproc.multiproc_logic import \
    MultiprocExecutor
from src.infrastructure.services.executor.multiproc.types import \
    ExecutorBackend
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