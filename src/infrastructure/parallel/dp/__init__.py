# SPDX-License-Identifier: Apache-2.0
"""
DataParallelCoordinator Package.
"""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .types import DPRole, WorkerHealth, LoadBalanceStrategy, DPConfig, WorkerState, StepState, WaveState
    from .balancer import P2CLoadBalancer
    from .engine import DPEngineCoreProc
    from .hierarchical import HierarchicalDPCoordinator
    from .collectives import dp_collective_all_reduce

def __getattr__(name: str) -> Any:
    if name in ("DPRole", "WorkerHealth", "LoadBalanceStrategy", "DPConfig", "WorkerState", "StepState", "WaveState"):
        from .types import DPRole, WorkerHealth, LoadBalanceStrategy, DPConfig, WorkerState, StepState, WaveState
        return locals()[name]
    if name == "P2CLoadBalancer":
        from .balancer import P2CLoadBalancer
        return P2CLoadBalancer
    if name == "DPEngineCoreProc":
        from .engine import DPEngineCoreProc
        return DPEngineCoreProc
    if name == "HierarchicalDPCoordinator":
        from .hierarchical import HierarchicalDPCoordinator
        return HierarchicalDPCoordinator
    if name == "dp_collective_all_reduce":
        from .collectives import dp_collective_all_reduce
        return dp_collective_all_reduce
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

