"""
Phase 45: Engine Client Factory
Factory functions for creating engine clients.
"""

from __future__ import annotations
from typing import Optional, Callable, TYPE_CHECKING
from src.infrastructure.engine.engine_client.types import ClientMode, EngineClientConfig
from src.infrastructure.engine.engine_client.inproc import InprocClient
from src.infrastructure.engine.engine_client.sync_mp import SyncMPClient
from src.infrastructure.engine.engine_client.async_mp import AsyncMPClient
from src.infrastructure.engine.engine_client.dp_async import DPAsyncMPClient

if TYPE_CHECKING:
    from src.infrastructure.engine.engine_client.types import SchedulerOutput, EngineOutput
    from src.infrastructure.engine.engine_client.base import EngineCoreClientBase


def auto_select_client_mode(num_gpus: int = 1, use_dp: bool = False) -> ClientMode:
    """
    Auto-select client mode based on GPU topology.

    Beyond vLLM: Automatic optimal configuration.
    """
    if num_gpus == 1 and not use_dp:
        return ClientMode.INPROC
    elif use_dp and num_gpus > 1:
        return ClientMode.DP_ASYNC
    elif num_gpus > 1:
        return ClientMode.ASYNC_MP
    else:
        return ClientMode.SYNC_MP


def create_engine_client(
    config: Optional[EngineClientConfig] = None,
    num_gpus: int = 1,
    use_dp: bool = False,
    engine_core: Optional[Callable[[SchedulerOutput], EngineOutput]] = None
) -> EngineCoreClientBase:
    """
    Factory function to create appropriate engine client.

    Beyond vLLM: Unified factory with auto-selection.
    """
    if config is None:
        config = EngineClientConfig()

    if config.auto_select_mode:
        config.mode = auto_select_client_mode(num_gpus, use_dp)

    if config.mode == ClientMode.INPROC:
        client = InprocClient(config, engine_core)
    elif config.mode == ClientMode.SYNC_MP:
        client = SyncMPClient(config)
    elif config.mode == ClientMode.ASYNC_MP:
        client = AsyncMPClient(config)
    elif config.mode == ClientMode.DP_ASYNC:
        config.num_workers = num_gpus
        client = DPAsyncMPClient(config)
    else:
        raise ValueError(f"Unknown client mode: {config.mode}")

    return client
