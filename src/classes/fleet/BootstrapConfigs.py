#!/usr/bin/env python3

"""
Hardcoded bootstrap configurations for essential system components.
These must remain static to ensure the system can boot up before dynamic discovery.
"""

BOOTSTRAP_AGENTS = {
    # System Agents that might not follow standard naming or search patterns
    "Orchestrator": (
        "src.classes.specialized.StructuredOrchestrator", 
        "StructuredOrchestrator", 
        None
    ),
    "Sandbox": (
        "src.classes.coder.SandboxAgent", 
        "SandboxAgent", 
        None
    ),
    "Linguist": (
        "src.classes.specialized.LinguisticAgent",
        "LinguisticAgent",
        None
    ),
    "Audit": (
        "src.classes.specialized.EternalAuditAgent",
        "EternalAuditAgent",
        None
    )
}

BOOTSTRAP_ORCHESTRATORS = {
    "self_healing": (
        "src.classes.orchestration.SelfHealingOrchestrator",
        "SelfHealingOrchestrator"
    ),
    "telemetry": (
        "src.classes.stats.ObservabilityEngine",
        "ObservabilityEngine"
    ),
    "self_improvement": (
        "src.classes.orchestration.SelfImprovementOrchestrator",
        "SelfImprovementOrchestrator"
    )
}
