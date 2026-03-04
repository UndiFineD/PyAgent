# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""
Disaggregated Scheduler Facade.
Redirects to the modular implementation in .disaggregated
"""

 from .disaggregated import (
    InstanceRole,
    SchedulingPolicy,
    InstanceInfo,
    DCPConfig,
    KVTransferParams,
    ScheduledRequest,
    InstanceSelector,
    RoundRobinSelector,
    LeastLoadedSelector,
    RandomSelector,
    HashSelector,
    DisaggregatedScheduler,
    SchedulerFactory,
)

# Backwards-compat exports: ProxyOrchestrator and create_dcp_scheduler live in
# the engine-level implementation. Import and expose them here so callers of
# `src.infrastructure.scheduling.DisaggregatedScheduler` continue to work.
try:
    from src.infrastructure.engine.scheduling.disaggregated.orchestrator import ProxyOrchestrator  # type: ignore
except Exception:
    # Best-effort shim: define a lightweight placeholder to avoid import errors
    class ProxyOrchestrator:  # pragma: no cover - compatibility shim
        def __init__(self, *args, **kwargs):
            raise RuntimeError("ProxyOrchestrator is not available in this environment")

try:
    from src.infrastructure.engine.scheduling.disaggregated.factory import create_dcp_scheduler  # type: ignore
except Exception:
    def create_dcp_scheduler(*args, **kwargs):  # pragma: no cover - compatibility shim
        raise RuntimeError("create_dcp_scheduler is not available in this environment")

__all__ = [
    "InstanceRole",
    "SchedulingPolicy",
    "InstanceInfo",
    "DCPConfig",
    "KVTransferParams",
    "ScheduledRequest",
    "InstanceSelector",
    "RoundRobinSelector",
    "LeastLoadedSelector",
    "RandomSelector",
    "HashSelector",
    "DisaggregatedScheduler",
    "SchedulerFactory",
]
