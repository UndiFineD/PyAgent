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
Phase 45: Multiprocess Executor
vLLM-inspired multiprocess executor with advanced coordination.

Refactored to modular package structure for Phase 317.
Decomposed into types, future, base, and specific implementation modules.

from src.infrastructure.services.executor.multiproc.base import Executor
from src.infrastructure.services.executor.multiproc.distributed import \
    DistributedExecutor
from src.infrastructure.services.executor.multiproc.factory import \
    ExecutorFactory
from src.infrastructure.services.executor.multiproc.future import FutureWrapper
from src.infrastructure.services.executor.multiproc.multiproc_logic import \
    MultiprocExecutor
from src.infrastructure.services.executor.multiproc.types import (
    ExecutorBackend, ResultMessage, TaskMessage, WorkerInfo, WorkerState)
from src.infrastructure.services.executor.multiproc.uniproc import \
    UniprocExecutor

__all__ = [
    "ExecutorBackend","    "WorkerState","    "WorkerInfo","    "TaskMessage","    "ResultMessage","    "FutureWrapper","    "Executor","    "UniprocExecutor","    "MultiprocExecutor","    "DistributedExecutor","    "ExecutorFactory","]
