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

# SPDX-License-Identifier: Apache-2.0
"""
DataParallelCoordinator Package.
"""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .balancer import P2CLoadBalancer
    from .collectives import dp_collective_all_reduce
    from .engine import DPEngineCoreProc
    from .hierarchical import HierarchicalDPCoordinator
    from .types import (DPConfig, DPRole, LoadBalanceStrategy, StepState,
                        WaveState, WorkerHealth, WorkerState)


def __getattr__(name: str) -> Any:
    if name in ("DPRole", "WorkerHealth", "LoadBalanceStrategy", "DPConfig", "WorkerState", "StepState", "WaveState"):
        from . import types as _types

        return getattr(_types, name)
    if name == "P2CLoadBalancer":
        from . import balancer as _balancer

        return getattr(_balancer, name)
    if name == "DPEngineCoreProc":
        from . import engine as _engine

        return getattr(_engine, name)
    if name == "HierarchicalDPCoordinator":
        from . import hierarchical as _hierarchical

        return getattr(_hierarchical, name)
    if name == "dp_collective_all_reduce":
        from . import collectives as _collectives

        return getattr(_collectives, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "DPRole",
    "WorkerHealth",
    "LoadBalanceStrategy",
    "DPConfig",
    "WorkerState",
    "StepState",
    "WaveState",
    "P2CLoadBalancer",
    "DPEngineCoreProc",
    "HierarchicalDPCoordinator",
    "dp_collective_all_reduce",
]
