#!/usr/bin/env python3

"""
Hardcoded bootstrap configurations for essential system components.
These must remain static to ensure the system can boot up before dynamic discovery.
"""

from __future__ import annotations
from typing import Dict, Tuple, Optional
from src.infrastructure.fleet.RegistryOverlay import RegistryOverlay

_overlay = RegistryOverlay()

def get_bootstrap_agents() -> Dict[str, Tuple[str, str, Optional[str]]]:
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
        "src.observability.stats.ObservabilityEngine",
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
        "src.observability.stats.ResourceMonitor",
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
    )
}
