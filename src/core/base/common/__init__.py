#!/usr/bin/env python3
"""Core common package safe initializer for repair runs.

This file intentionally avoids heavy imports to prevent cascading
import errors during automated repairs. It exposes a conservative
__all__ to preserve references used by tests and lightweight code.
"""

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
