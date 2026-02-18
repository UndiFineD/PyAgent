#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
Hardcoded bootstrap configurations for essential system components.
These must remain static to ensure the system can boot up before dynamic discovery.
"""


from __future__ import annotations


try:
    from .core.base.lifecycle.version import VERSION
except ImportError:
    from src.core.base.lifecycle.version import VERSION

try:
    from .infrastructure.swarm.fleet.registry_overlay import RegistryOverlay
except ImportError:
    from src.infrastructure.swarm.fleet.registry_overlay import RegistryOverlay


__version__ = VERSION

_overlay = RegistryOverlay()


def get_bootstrap_agents() -> dict[str, tuple[str, str, str | None]]:
    """
    Returns the bootstrap agents with dynamic overrides applied.
    """
    defaults = {
        "Orchestrator": ("src.logic.agents.swarm.pattern_orchestrator", "PatternOrchestrator", None),
        "Sandbox": ("src.logic.agents.system.sandbox_agent", "SandboxAgent", None),
        "Linguist": ("src.logic.agents.cognitive.linguistic_agent", "LinguisticAgent", None),
        "Audit": ("src.logic.agents.security.eternal_audit_agent", "EternalAuditAgent", None),
        "LegalAudit": ("src.logic.agents.security.legal_audit_agent", "LegalAuditAgent", None),
        "Logging": ("src.logic.agents.system.logging_agent", "LoggingAgent", None),
        "Telemetry": ("src.logic.agents.system.telemetry_agent", "TelemetryAgent", None),
        "FleetDeployer": ("src.logic.agents.swarm.fleet_deployer_agent", "FleetDeployerAgent", None),
        "agent_dao": ("src.infrastructure.swarm.orchestration.system.agent_dao", "AgentDAO", None),
        "weight_orchestrator": ("src.infrastructure.swarm.orchestration.system.weight_orchestrator", "WeightOrchestrator", None),
        "immune_orchestrator": ("src.logic.agents.security.immune_response_orchestrator", "ImmuneResponseOrchestrator", None),
        "quantum_shard": ("src.infrastructure.swarm.orchestration.system.quantum_shard_orchestrator", "QuantumShardOrchestrator", None),
        "ExpertMiner": ("src.logic.agents.specialized.expert_miner_agent", "ExpertMinerAgent", None),
        "HolographicContext": ("src.logic.agents.cognitive.holographic_context_agent", "HolographicContextAgent", None),
    }

    return {k: _overlay.get_agent_config(k, v) for k, v in defaults.items()}


BOOTSTRAP_AGENTS = get_bootstrap_agents()

BOOTSTRAP_ORCHESTRATORS = {
    "self_healing": ("src.infrastructure.swarm.orchestration.healing.self_healing_orchestrator", "SelfHealingOrchestrator", None),
    "telemetry": ("src.observability.stats.metrics_engine", "ObservabilityEngine", None),
    "self_improvement": ("src.infrastructure.swarm.orchestration.intel.self_improvement_orchestrator", "SelfImprovementOrchestrator", None),
    "holographic_state": ("src.infrastructure.swarm.orchestration.state.holographic_state_orchestrator", "HolographicStateOrchestrator", None),
    "structured_orchestrator": ("src.infrastructure.swarm.orchestration.intel.phase_orchestrator", "PhaseOrchestrator", None),
    "registry": ("src.infrastructure.swarm.orchestration.system.tool_registry", "ToolRegistry", None),
    "signals": ("src.infrastructure.swarm.orchestration.signals.signal_registry", "SignalRegistry", None),
    "recorder": ("src.infrastructure.compute.backend.local_context_recorder", "LocalContextRecorder", None),
    "sql_metadata": ("src.infrastructure.compute.backend.sql_metadata_handler", "SqlMetadataHandler", None),
    "global_context": ("src.logic.agents.cognitive.context.engines.global_context_engine", "GlobalContextEngine", None),
    "market": ("src.infrastructure.swarm.fleet.agent_economy", "AgentEconomy", None),
    "resources": ("src.observability.stats.monitoring", "ResourceMonitor", None),
    "gossip": ("src.infrastructure.swarm.orchestration.consensus.gossip_protocol_orchestrator", "GossipProtocolOrchestrator", None),
    "sharding": ("src.infrastructure.swarm.fleet.shard_manager", "ShardManager", None),
    "load_balancer": ("src.infrastructure.services.api.fleet_load_balancer", "FleetLoadBalancer", None),
    "fallback_engine": ("src.observability.stats.analysis", "ModelFallbackEngine", None),
    "core": ("src.infrastructure.swarm.fleet.fleet_core", "FleetCore", None),
    "speciation": ("src.infrastructure.swarm.orchestration.swarm.speciation_orchestrator", "SpeciationOrchestrator", None),
    "sovereignty_orchestrator": ("src.infrastructure.swarm.orchestration.swarm.sovereignty_orchestrator", "SovereigntyOrchestrator", None),
    "fractal_orchestrator": ("src.infrastructure.swarm.orchestration.swarm.fractal_orchestrator", "FractalOrchestrator", None),
    "sub_swarm_spawner": ("src.infrastructure.swarm.orchestration.swarm.sub_swarm_spawner", "SubSwarmSpawner", None),
    "discovery": ("src.infrastructure.swarm.orchestration.swarm.discovery_orchestrator", "DiscoveryOrchestrator", None),
    "scaling": ("src.infrastructure.swarm.fleet.scaling_manager", "ScalingManager", None),
    "blackboard": ("src.infrastructure.swarm.orchestration.state.blackboard_manager", "BlackboardManager", None),
    "experiment_orchestrator": ("src.infrastructure.swarm.orchestration.system.experiment_orchestrator", "ExperimentOrchestrator", None),
    "evolution": ("src.infrastructure.swarm.fleet.evolution_engine", "EvolutionEngine", None),
    "emotional_regulation": ("src.infrastructure.swarm.orchestration.intel.emotional_regulation_orchestrator", "EmotionalRegulationOrchestrator", None),
    "resource_predictor": ("src.infrastructure.swarm.orchestration.swarm.resource_predictor_orchestrator", "ResourcePredictorOrchestrator", None),
    "fleet_telemetry": ("src.infrastructure.swarm.orchestration.swarm.fleet_telemetry_visualizer", "FleetTelemetryVisualizer", None),
    "consciousness": ("src.infrastructure.swarm.fleet.consciousness_registry", "ConsciousnessRegistry", None),
}
