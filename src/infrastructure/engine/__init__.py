# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""
Engine infrastructure module.

Provides request lifecycle management, engine state control,
engine core orchestration, output processing, detokenization, and prefix caching.
Inspired by vLLM's v1/engine architecture.

Phase 30 additions:
- EngineCore: Central engine orchestration loop
- OutputProcessor: Request output management
- IncrementalDetokenizer: Fast streaming decode
- PrefixCacheManager: Block-level caching
- EngineCoreClient: Engine communication clients
"""

from .RequestLifecycle import (
    FinishReason,
    Request,
    RequestEvent,
    RequestEventType,
    RequestQueue,
    RequestStatus,
    RequestTracker,
)
from .EngineLifecycle import (
    EngineConfig,
    EngineLifecycleManager,
    EngineState,
)

# Phase 30: Engine Core
from .EngineCore import (
    RequestStatus as CoreRequestStatus,
    FinishReason as CoreFinishReason,
    Request as CoreRequest,
    SchedulerOutput,
    ModelRunnerOutput,
    EngineCoreOutput,
    EngineCoreOutputs,
    Scheduler,
    SimpleScheduler,
    Executor,
    MockExecutor,
    EngineCore,
    EngineCoreProc,
    create_engine_core,
)

# Phase 30: Output Processor
from .OutputProcessor import (
    EventType,
    RequestEvent as OutputRequestEvent,
    LoRARequest,
    ParentRequest,
    SamplingParams,
    EngineCoreRequest,
    RequestOutput,
    OutputProcessorOutput,
    RequestOutputCollector,
    RequestState,
    LoRARequestStates,
    OutputProcessor,
    IterationStats,
)

# Phase 30: Incremental Detokenizer
from .IncrementalDetokenizer import (
    StopMatch,
    check_stop_strings,
    check_stop_strings_rust,
    IncrementalDetokenizer,
    NoOpDetokenizer,
    BaseIncrementalDetokenizer,
    FastIncrementalDetokenizer,
    SlowIncrementalDetokenizer,
    validate_utf8,
    validate_utf8_rust,
    INITIAL_INCREMENTAL_DETOKENIZATION_OFFSET,
)

# Phase 30: Prefix Cache Manager
from .PrefixCacheManager import (
    HashAlgorithm,
    BlockHash,
    CacheBlock,
    get_hash_function,
    hash_block_tokens,
    hash_block_tokens_rust,
    init_none_hash,
    PrefixCacheManager,
    compute_prefix_match,
    compute_prefix_match_rust,
    compute_cache_keys,
    compute_cache_keys_rust,
)

# Phase 30: Engine Core Client
from .EngineCoreClient import (
    RequestType,
    ClientConfig,
    EngineCoreClient,
    InprocClient,
    SyncMPClient,
    AsyncMPClient,
    create_client,
)


__all__ = [
    # Request Lifecycle
    "FinishReason",
    "Request",
    "RequestEvent",
    "RequestEventType",
    "RequestQueue",
    "RequestStatus",
    "RequestTracker",
    # Engine Lifecycle
    "EngineConfig",
    "EngineLifecycleManager",
    "EngineState",
    # Phase 30: EngineCore
    "CoreRequestStatus",
    "CoreFinishReason",
    "CoreRequest",
    "SchedulerOutput",
    "ModelRunnerOutput",
    "EngineCoreOutput",
    "EngineCoreOutputs",
    "Scheduler",
    "SimpleScheduler",
    "Executor",
    "MockExecutor",
    "EngineCore",
    "EngineCoreProc",
    "create_engine_core",
    # Phase 30: OutputProcessor
    "EventType",
    "OutputRequestEvent",
    "LoRARequest",
    "ParentRequest",
    "SamplingParams",
    "EngineCoreRequest",
    "RequestOutput",
    "OutputProcessorOutput",
    "RequestOutputCollector",
    "RequestState",
    "LoRARequestStates",
    "OutputProcessor",
    "IterationStats",
    # Phase 30: IncrementalDetokenizer
    "StopMatch",
    "check_stop_strings",
    "check_stop_strings_rust",
    "IncrementalDetokenizer",
    "NoOpDetokenizer",
    "BaseIncrementalDetokenizer",
    "FastIncrementalDetokenizer",
    "SlowIncrementalDetokenizer",
    "validate_utf8",
    "validate_utf8_rust",
    "INITIAL_INCREMENTAL_DETOKENIZATION_OFFSET",
    # Phase 30: PrefixCacheManager
    "HashAlgorithm",
    "BlockHash",
    "CacheBlock",
    "get_hash_function",
    "hash_block_tokens",
    "hash_block_tokens_rust",
    "init_none_hash",
    "PrefixCacheManager",
    "compute_prefix_match",
    "compute_prefix_match_rust",
    "compute_cache_keys",
    "compute_cache_keys_rust",
    # Phase 30: EngineCoreClient
    "RequestType",
    "ClientConfig",
    "EngineCoreClient",
    "InprocClient",
    "SyncMPClient",
    "AsyncMPClient",
    "create_client",
]
