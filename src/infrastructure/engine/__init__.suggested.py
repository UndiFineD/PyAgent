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
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project

"""
Module: engine
PyAgent engine package initialization.

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

# Phase 30: Engine Core
from .engine_core import (
    EngineCore,
    EngineCoreOutput,
    EngineCoreOutputs,  # noqa: F401
    EngineCoreProc,
    Executor,
)
from .engine_core import FinishReason as CoreFinishReason  # noqa: F401
from .engine_core import MockExecutor, ModelRunnerOutput  # noqa: F401
from .engine_core import Request as CoreRequest  # noqa: F401
from .engine_core import RequestStatus as CoreRequestStatus  # noqa: F401
from .engine_core import (
    Scheduler,
    SchedulerOutput,
    SimpleScheduler,  # noqa: F401
    create_engine_core,
)

# Phase 30: Engine Core Client
from .engine_core_client import (
    AsyncMPClient,
    ClientConfig,
    EngineCoreClient,  # noqa: F401
    InprocClient,
    RequestType,
    SyncMPClient,
    create_client,
)
from .engine_lifecycle import EngineConfig, EngineLifecycleManager, EngineState  # noqa: F401

# Phase 30: Incremental Detokenizer
from .incremental_detokenizer import (  # noqa: F401
    INITIAL_INCREMENTAL_DETOKENIZATION_OFFSET,
    BaseIncrementalDetokenizer,
    FastIncrementalDetokenizer,
    IncrementalDetokenizer,
    NoOpDetokenizer,
    SlowIncrementalDetokenizer,
    StopMatch,
    check_stop_strings,
    check_stop_strings_rust,
    validate_utf8,
    validate_utf8_rust,
)

# Phase 30: Output Processor
from .output_processor import (
    EngineCoreRequest,
    EventType,
    IterationStats,  # noqa: F401
    LoRARequest,
    LoRARequestStates,
    OutputProcessor,
    OutputProcessorOutput,
    ParentRequest,
)
from .output_processor import RequestEvent as OutputRequestEvent  # noqa: F401
from .output_processor import (
    RequestOutput,
    RequestOutputCollector,  # noqa: F401
    RequestState,
    SamplingParams,
)

# Phase 30: Prefix Cache Manager
from .prefix_cache_manager import (
    BlockHash,
    CacheBlock,
    HashAlgorithm,  # noqa: F401
    PrefixCacheManager,
    compute_cache_keys,
    compute_cache_keys_rust,
    compute_prefix_match,
    compute_prefix_match_rust,
    get_hash_function,
    hash_block_tokens,
    hash_block_tokens_rust,
    init_none_hash,
)
from .request_lifecycle import (
    FinishReason,
    Request,
    RequestEvent,  # noqa: F401
    RequestEventType,
    RequestQueue,
    RequestStatus,
    RequestTracker,
)

__all__: list[str] = [
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
