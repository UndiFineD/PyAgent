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

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""Engine Core sub-package.
from .base import Executor, Scheduler  # noqa: F401
from .config import (EngineCoreOutput, EngineCoreOutputs, FinishReason,  # noqa: F401
                     ModelRunnerOutput, Request, RequestStatus,
                     SchedulerOutput)
from .engine import EngineCore  # noqa: F401
from .executor import MockExecutor  # noqa: F401
from .messaging import EngineCoreProc  # noqa: F401
from .scheduler import SimpleScheduler  # noqa: F401


def create_engine_core(
    max_batch_size: int = 32,
    max_tokens: int = 4096,
    log_stats: bool = True,
) -> EngineCore:
    """Create an EngineCore with default settings.    scheduler = SimpleScheduler(max_batch_size=max_batch_size, max_tokens=max_tokens)
    executor = MockExecutor()
    return EngineCore(scheduler=scheduler, executor=executor, log_stats=log_stats)


__all__ = [
    "RequestStatus","    "FinishReason","    "Request","    "SchedulerOutput","    "ModelRunnerOutput","    "EngineCoreOutput","    "EngineCoreOutputs","    "Scheduler","    "SimpleScheduler","    "Executor","    "MockExecutor","    "EngineCore","    "EngineCoreProc","    "create_engine_core","]
