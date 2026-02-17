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


"""Common package."""



try:
    from src.core.base.common.analysis_core import AnalysisCore  # type: ignore
    from src.core.base.common.auth_core import AuthCore  # type: ignore
    from src.core.base.common.base_core import BaseCore  # type: ignore
    from src.core.base.common.batch_core import BatchCore  # type: ignore
    from src.core.base.common.cache_core import CacheCore  # type: ignore
    from src.core.base.common.connectivity_core import ConnectivityCore  # type: ignore
    from src.core.base.common.consensus_core import ConsensusCore  # type: ignore
    from src.core.base.common.diff_core import DiffCore  # type: ignore
    from src.core.base.common.execution_core import ExecutionCore  # type: ignore
    from src.core.base.common.formula_core import FormulaCore  # type: ignore
    from src.core.base.common.git_core import GitCore  # type: ignore
    from src.core.base.common.hardware_core import HardwareCore  # type: ignore
    from src.core.base.common.health_core import HealthCore  # type: ignore
    from src.core.base.common.inference_core import InferenceCore  # type: ignore
    from src.core.base.common.lock_core import LockCore  # type: ignore
    from src.core.base.common.multimodal_core import (
        MultimodalCore, MultimodalStreamSession, StreamingAudioProcessor, StreamingVisionEncoder, TemporalModalityBuffer
    )  # type: ignore
    from src.core.base.common.registry_core import RegistryCore  # type: ignore
    from src.core.base.common.resource_core import ResourceCore  # type: ignore
    from src.core.base.common.routing_core import RoutingCore  # type: ignore
    from src.core.base.common.scaling_core import ScalingCore  # type: ignore
    from src.core.base.common.search_core import SearchCore  # type: ignore
    from src.core.base.common.secret_core import SecretCore  # type: ignore
    from src.core.base.common.shard_core import ShardCore  # type: ignore
    from src.core.base.common.shell_core import ShellCore  # type: ignore
    from src.core.base.common.signal_core import SignalCore  # type: ignore
    from src.core.base.common.stability_core import StabilityCore  # type: ignore
    from src.core.base.common.telemetry_core import TelemetryCore  # type: ignore
    from src.core.base.common.template_core import TemplateCore  # type: ignore
    from src.core.base.common.time_core import TimeCore  # type: ignore
    from src.core.base.common.validation_core import ValidationCore  # type: ignore
    from src.core.base.common.workspace_core import WorkspaceCore  # type: ignore
except ImportError:
    from .analysis_core import AnalysisCore  # noqa: F401
    from .auth_core import AuthCore  # noqa: F401
    from .base_core import BaseCore  # noqa: F401
    from .batch_core import BatchCore  # noqa: F401
    from .cache_core import CacheCore  # noqa: F401
    from .connectivity_core import ConnectivityCore  # noqa: F401
    from .consensus_core import ConsensusCore  # noqa: F401
    from .diff_core import DiffCore  # noqa: F401
    from .execution_core import ExecutionCore  # noqa: F401
    from .formula_core import FormulaCore  # noqa: F401
    from .git_core import GitCore  # noqa: F401
    from .hardware_core import HardwareCore  # noqa: F401
    from .health_core import HealthCore  # noqa: F401
    from .inference_core import InferenceCore  # noqa: F401
    from .lock_core import LockCore  # noqa: F401
    from .multimodal_core import (
        MultimodalCore, MultimodalStreamSession, StreamingAudioProcessor, StreamingVisionEncoder, TemporalModalityBuffer
    )  # noqa: F401
    from .registry_core import RegistryCore  # noqa: F401
    from .resource_core import ResourceCore  # noqa: F401
    from .routing_core import RoutingCore  # noqa: F401
    from .scaling_core import ScalingCore  # noqa: F401
    from .search_core import SearchCore  # noqa: F401
    from .secret_core import SecretCore  # noqa: F401
    from .shard_core import ShardCore  # noqa: F401
    from .shell_core import ShellCore  # noqa: F401
    from .signal_core import SignalCore  # noqa: F401
    from .stability_core import StabilityCore  # noqa: F401
    from .telemetry_core import TelemetryCore  # noqa: F401
    from .template_core import TemplateCore  # noqa: F401
    from .time_core import TimeCore  # noqa: F401
    from .validation_core import ValidationCore  # noqa: F401
    from .workspace_core import WorkspaceCore  # noqa: F401

__all__ = [
    "BaseCore",
    "StabilityCore",
    "ConsensusCore",
    "ValidationCore",
    "InferenceCore",
    "ConnectivityCore",
    "AuthCore",
    "TelemetryCore",
    "RoutingCore",
    "SignalCore",
    "SearchCore",
    "ShardCore",
    "WorkspaceCore",
    "AnalysisCore",
    "HealthCore",
    "FormulaCore",
    "DiffCore",
    "GitCore",
    "ScalingCore",
    "SecretCore",
    "ExecutionCore",
    "RegistryCore",
    "CacheCore",
    "BatchCore",
    "LockCore",
    "ResourceCore",
    "TemplateCore",
    "MultimodalCore",
    "StreamingAudioProcessor",
    "TemporalModalityBuffer",
    "StreamingVisionEncoder",
    "MultimodalStreamSession",
    "HardwareCore",
    "ShellCore",
    "TimeCore",
]
