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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""
Hardcoded bootstrap configurations for essential system components.
These must remain static to ensure the system can boot up before dynamic discovery.
"""

from __future__ import annotations
from src.core.base.version import VERSION
from src.infrastructure.fleet.RegistryOverlay import RegistryOverlay

__version__ = VERSION

_overlay = RegistryOverlay()




def get_bootstrap_agents() -> dict[str, tuple[str, str, str | None]]:
    """Returns the bootstrap agents with dynamic overrides applied."""
    defaults = {
        "Orchestrator": (
            "src.logic.agents.swarm.PatternOrchestrator",
            "PatternOrchestrator",
            None
        ),
        "Sandbox": (
            "src.logic.agents.development.SandboxAgent",
            "SandboxAgent",
            None
        ),
        "Linguist": (
            "src.logic.agents.cognitive.LinguisticAgent",
            "LinguisticAgent",
            None
        ),
        "Audit": (
            "src.logic.agents.security.EternalAuditAgent",
            "EternalAuditAgent",
            None
        ),
        "LegalAudit": (
            "src.logic.agents.security.LegalAuditAgent",
            "LegalAuditAgent",
            None
        ),
        "Logging": (
            "src.logic.agents.system.LoggingAgent",
            "LoggingAgent",
            None
        ),
        "agent_dao": (
            "src.infrastructure.orchestration.AgentDAO",
            "AgentDAO",
            None
        ),










        "weight_orchestrator": (
            "src.infrastructure.orchestration.WeightOrchestrator",
            "WeightOrchestrator",
            None










        ),
        "immune_orchestrator": (
            "src.logic.agents.security.ImmuneResponseOrchestrator",
            "ImmuneResponseOrchestrator",
            None









        ),
        "quantum_shard": (
            "src.infrastructure.orchestration.QuantumShardOrchestrator",
            "QuantumShardOrchestrator",
            None

        )
    }

    return {k: _overlay.get_agent_config(k, v) for k, v in defaults.items()}





BOOTSTRAP_AGENTS = get_bootstrap_agents()

BOOTSTRAP_ORCHESTRATORS = {
    "self_healing": (
        "src.infrastructure.orchestration.SelfHealingOrchestrator",
        "SelfHealingOrchestrator"
    ),
    "telemetry": (
        "src.observability.stats.metrics_engine",
        "ObservabilityEngine"
    ),
    "self_improvement": (
        "src.infrastructure.orchestration.SelfImprovementOrchestrator",
        "SelfImprovementOrchestrator"
    ),
    "registry": (
        "src.infrastructure.orchestration.ToolRegistry",
        "ToolRegistry"
    ),
    "signals": (
        "src.infrastructure.orchestration.SignalRegistry",
        "SignalRegistry"
    ),
    "recorder": (
        "src.infrastructure.backend.LocalContextRecorder",
        "LocalContextRecorder"
    ),
    "sql_metadata": (
        "src.infrastructure.backend.SqlMetadataHandler",
        "SqlMetadataHandler"
    ),
    "global_context": (
        "src.logic.agents.cognitive.context.engines.GlobalContextEngine",
        "GlobalContextEngine"
    ),
    "market": (
        "src.infrastructure.fleet.AgentEconomy",
        "AgentEconomy"
    ),
    "resources": (
        "src.observability.stats.monitoring",
        "ResourceMonitor"
    ),
    "gossip": (
        "src.infrastructure.orchestration.GossipProtocolOrchestrator",
        "GossipProtocolOrchestrator"
    ),
    "sharding": (
        "src.infrastructure.fleet.ShardManager",
        "ShardManager"
    ),
    "load_balancer": (
        "src.infrastructure.api.FleetLoadBalancer",
        "FleetLoadBalancer"
    ),
    "fallback_engine": (
        "src.observability.stats.ModelFallbackEngine",
        "ModelFallbackEngine"
    ),
    "core": (
        "src.infrastructure.fleet.FleetCore",
        "FleetCore"
    ),
    "speciation": (
        "src.infrastructure.orchestration.SpeciationOrchestrator",
        "SpeciationOrchestrator"
    ),
    "sovereignty_orchestrator": (
        "src.infrastructure.orchestration.SovereigntyOrchestrator",
        "SovereigntyOrchestrator"
    ),
    "fractal_orchestrator": (
        "src.infrastructure.orchestration.FractalOrchestrator",
        "FractalOrchestrator"
    ),
    "sub_swarm_spawner": (
        "src.infrastructure.orchestration.SubSwarmSpawner",
        "SubSwarmSpawner"
    ),
    "discovery": (
        "src.infrastructure.orchestration.DiscoveryOrchestrator",
        "DiscoveryOrchestrator"
    ),
    "scaling": (
        "src.infrastructure.fleet.ScalingManager",
        "ScalingManager"
    ),
    "blackboard": (
        "src.infrastructure.orchestration.BlackboardManager",
        "BlackboardManager"
    ),
    "experiment_orchestrator": (
        "src.infrastructure.orchestration.ExperimentOrchestrator",
        "ExperimentOrchestrator"
    ),
    "evolution": (
        "src.infrastructure.fleet.EvolutionEngine",
        "EvolutionEngine"
    ),
    "fleet_telemetry": (
        "src.infrastructure.orchestration.FleetTelemetryVisualizer",
        "FleetTelemetryVisualizer"
    ),
    "consciousness": (
        "src.infrastructure.fleet.ConsciousnessRegistry",
        "ConsciousnessRegistry"
    )
}
