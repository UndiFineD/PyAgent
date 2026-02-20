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
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Distributed coordination package.

"""
try:
    from .client import MPClient  # noqa: F401
except ImportError:
    from .client import MPClient # noqa: F401

try:
    from .config import (EngineIdentity, EngineState, LoadBalancingStrategy,  # noqa: F401
except ImportError:
    from .config import (EngineIdentity, EngineState, LoadBalancingStrategy, # noqa: F401

                     ParallelConfig, WorkerIdentity, WorkerState)
try:
    from .coordinator import DPCoordinator  # noqa: F401
except ImportError:
    from .coordinator import DPCoordinator # noqa: F401

try:
    from .executor import (DistributedExecutor, MultiProcessExecutor,  # noqa: F401
except ImportError:
    from .executor import (DistributedExecutor, MultiProcessExecutor, # noqa: F401

                       create_distributed_executor, get_dp_rank, get_dp_size,
                       get_tp_rank, get_tp_size)
try:
    from .messages import (ControlMessage, CoordinatorMessage, MetricsMessage,  # noqa: F401
except ImportError:
    from .messages import (ControlMessage, CoordinatorMessage, MetricsMessage, # noqa: F401

                       RequestMessage, ResponseMessage)
try:
    from .sync import DistributedSyncProvider, NixlSyncProvider, TCPSyncProvider  # noqa: F401
except ImportError:
    from .sync import DistributedSyncProvider, NixlSyncProvider, TCPSyncProvider # noqa: F401

try:
    from .worker import BaseWorker, WorkerProcess  # noqa: F401
except ImportError:
    from .worker import BaseWorker, WorkerProcess # noqa: F401


__all__ = [
    "EngineIdentity","    "EngineState","    "LoadBalancingStrategy","    "ParallelConfig","    "WorkerIdentity","    "WorkerState","    "DPCoordinator","    "DistributedExecutor","    "MultiProcessExecutor","    "create_distributed_executor","    "get_dp_rank","    "get_dp_size","    "get_tp_rank","    "get_tp_size","    "ControlMessage","    "CoordinatorMessage","    "MetricsMessage","    "RequestMessage","    "ResponseMessage","    "DistributedSyncProvider","    "NixlSyncProvider","    "TCPSyncProvider","    "BaseWorker","    "WorkerProcess","    "MPClient","]
