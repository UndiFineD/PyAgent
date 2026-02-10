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


"""
Hardcoded bootstrap configurations for essential system components.
These must remain static to ensure the system can boot up before dynamic discovery.
"""

from __future__ import annotations

from src.core.base.lifecycle.version import VERSION
from src.infrastructure.swarm.fleet.registry_overlay import RegistryOverlay

__version__ = VERSION

_overlay = RegistryOverlay()


def get_bootstrap_agents() -> dict[str, tuple[str, str, str | None]]:
    """Returns the bootstrap agents with dynamic overrides applied."""
    defaults = {
        "Orchestrator": (
            "src.logic.agents.swarm.pattern_orchestrator",
            "PatternOrchestrator",
            None,
        ),
        "Sandbox": ("src.logic.agents.system.sandbox_agent", "SandboxAgent", None),
        "Linguist": (
            "src.logic.agents.cognitive.linguistic_agent",
            "LinguisticAgent",
            None,
        ),
        "Audit": (
            "src.logic.agents.security.eternal_audit_agent",
            "EternalAuditAgent",
            None,
        ),
        "LegalAudit": (
            "src.logic.agents.security.legal_audit_agent",
            "LegalAuditAgent",
            None,
        ),
        "Logging": ("src.logic.agents.system.logging_agent", "LoggingAgent", None),
        "Telemetry": ("src.logic.agents.system.telemetry_agent", "TelemetryAgent", None),
        "FleetDeployer": (
            "src.logic.agents.swarm.fleet_deployer_agent",
            "FleetDeployerAgent",
            None,
        ),
        "agent_dao": ("src.infrastructure.swarm.orchestration.system.agent_dao", "AgentDAO", None),
        "weight_orchestrator": (
            "src.infrastructure.swarm.orchestration.system.weight_orchestrator",
            "WeightOrchestrator",
            None,
        ),
        "immune_orchestrator": (
            "src.logic.agents.security.immune_response_orchestrator",
            "ImmuneResponseOrchestrator",
            None,
        ),
        "quantum_shard": (
            "src.infrastructure.swarm.orchestration.system.quantum_shard_orchestrator",
            "QuantumShardOrchestrator",
            None,
        ),
        "ExpertMiner": (
            "src.logic.agents.specialized.expert_miner_agent",
            "ExpertMinerAgent",
            None,
        ),
        "HolographicContext": (
            "src.logic.agents.cognitive.holographic_context_agent",
            "HolographicContextAgent",
            None,
        ),
    }

    return {k: _overlay.get_agent_config(k, v) for k, v in defaults.items()}


BOOTSTRAP_AGENTS = get_bootstrap_agents()

BOOTSTRAP_ORCHESTRATORS = {
    "self_healing": (
        "src.infrastructure.swarm.orchestration.healing.self_healing_orchestrator",
        "SelfHealingOrchestrator",
    ),
    "telemetry": ("src.observability.stats.metrics_engine", "ObservabilityEngine"),
    "self_improvement": (
        "src.infrastructure.swarm.orchestration.intel.self_improvement_orchestrator",
        "SelfImprovementOrchestrator",
    ),
    "holographic_state": (
        "src.infrastructure.swarm.orchestration.state.holographic_state_orchestrator",
        "HolographicStateOrchestrator",
    ),
    "structured_orchestrator": (
        "src.infrastructure.swarm.orchestration.intel.phase_orchestrator",
        "PhaseOrchestrator",
    ),
    "registry": ("src.infrastructure.swarm.orchestration.system.tool_registry", "ToolRegistry"),
    "signals": ("src.infrastructure.swarm.orchestration.signals.signal_registry", "SignalRegistry"),
    "recorder": (
        "src.infrastructure.compute.backend.local_context_recorder",
        "LocalContextRecorder",
    ),
    "sql_metadata": (
        "src.infrastructure.compute.backend.sql_metadata_handler",
        "SqlMetadataHandler",
    ),
    "global_context": (
        "src.logic.agents.cognitive.context.engines.global_context_engine",
        "GlobalContextEngine",
    ),
    "market": ("src.infrastructure.swarm.fleet.agent_economy", "AgentEconomy"),
    "resources": ("src.observability.stats.monitoring", "ResourceMonitor"),
    "gossip": (
        "src.infrastructure.swarm.orchestration.consensus.gossip_protocol_orchestrator",
        "GossipProtocolOrchestrator",
    ),
    "sharding": ("src.infrastructure.swarm.fleet.shard_manager", "ShardManager"),
    "load_balancer": ("src.infrastructure.services.api.fleet_load_balancer", "FleetLoadBalancer"),
    "fallback_engine": (
        "src.observability.stats.analysis",
        "ModelFallbackEngine",
    ),
    "core": ("src.infrastructure.swarm.fleet.fleet_core", "FleetCore"),
    "speciation": (
        "src.infrastructure.swarm.orchestration.swarm.speciation_orchestrator",
        "SpeciationOrchestrator",
    ),
    "sovereignty_orchestrator": (
        "src.infrastructure.swarm.orchestration.swarm.sovereignty_orchestrator",
        "SovereigntyOrchestrator",
    ),
    "fractal_orchestrator": (
        "src.infrastructure.swarm.orchestration.swarm.fractal_orchestrator",
        "FractalOrchestrator",
    ),
    "sub_swarm_spawner": (
        "src.infrastructure.swarm.orchestration.swarm.sub_swarm_spawner",
        "SubSwarmSpawner",
    ),
    "discovery": (
        "src.infrastructure.swarm.orchestration.swarm.discovery_orchestrator",
        "DiscoveryOrchestrator",
    ),
    "scaling": ("src.infrastructure.swarm.fleet.scaling_manager", "ScalingManager"),
    "blackboard": (
        "src.infrastructure.swarm.orchestration.state.blackboard_manager",
        "BlackboardManager",
    ),
    "experiment_orchestrator": (
        "src.infrastructure.swarm.orchestration.system.experiment_orchestrator",
        "ExperimentOrchestrator",
    ),
    "evolution": ("src.infrastructure.swarm.fleet.evolution_engine", "EvolutionEngine"),
    "emotional_regulation": (
        "src.infrastructure.swarm.orchestration.intel.emotional_regulation_orchestrator",
        "EmotionalRegulationOrchestrator",
    ),
    "resource_predictor": (
        "src.infrastructure.swarm.orchestration.swarm.resource_predictor_orchestrator",
        "ResourcePredictorOrchestrator",
    ),
    "fleet_telemetry": (
        "src.infrastructure.swarm.orchestration.swarm.fleet_telemetry_visualizer",
        "FleetTelemetryVisualizer",
    ),
    "consciousness": (
        "src.infrastructure.swarm.fleet.consciousness_registry",
        "ConsciousnessRegistry",
    ),
}
