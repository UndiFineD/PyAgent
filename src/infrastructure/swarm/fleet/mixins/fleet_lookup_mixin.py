
"""
Fleet lookup mixin.py module.
"""
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from src.infrastructure.compute.backend.local_context_recorder import \
        LocalContextRecorder
    from src.infrastructure.compute.backend.sql_metadata_handler import \
        SqlMetadataHandler
    from src.infrastructure.swarm.fleet.fleet_manager import FleetManager
    from src.infrastructure.swarm.orchestration.healing.self_healing_orchestrator import \
        SelfHealingOrchestrator
    from src.infrastructure.swarm.orchestration.intel.self_improvement_orchestrator import \
        SelfImprovementOrchestrator
    from src.infrastructure.swarm.orchestration.signals.signal_registry import \
        SignalRegistry
    from src.infrastructure.swarm.orchestration.system.tool_registry import \
        ToolRegistry
    from src.logic.agents.cognitive.context.engines.global_context_engine import \
        GlobalContextEngine
    from src.observability.stats.metrics_engine import (ModelFallbackEngine,
                                                        ObservabilityEngine)


class FleetLookupMixin:
    """Mixin for lazy loading lookups and property accessors in FleetManager."""

    def __getattr__(self: FleetManager, name: str) -> Any:
        """Delegate to orchestrators and agents for lazy loading support."""
        if name.startswith("__"):
            raise AttributeError(f"'FleetManager' object has no attribute '{name}'")

        # Optimization: Avoid recursion if we are already looking for an internal attribute
        current_dict = self.__dict__

        # Phase 130: Handle Backend -> System rename for legacy support
        effective_name = name
        if "backend" in name:
            effective_name = name.replace("backend", "system")

        # 1. Capability Hints Fallback (Phase 125: Check explicit mappings first)
        hints = self.__dict__.get("capability_hints", {})
        if effective_name in hints:
            target = hints[effective_name]
            # Avoid infinite recursion if target resolves back to name or effective_name
            if target not in (effective_name, name):
                try:
                    return getattr(self, target)
                except AttributeError:
                    pass
        elif name != effective_name and name in hints:
            target = hints[name]
            # Avoid recursion if target resolves back to name or effective_name
            if target not in (name, effective_name):
                try:
                    return getattr(self, target)
                except AttributeError:
                    pass

        # 2. Try Orchestrators
        if "orchestrators" in current_dict:
            orchestrators = current_dict["orchestrators"]
            try:
                # LazyOrchestratorMap implements __getattr__
                return getattr(orchestrators, effective_name)
            except AttributeError:
                if effective_name != name:
                    try:
                        return getattr(orchestrators, name)
                    except AttributeError:
                        pass
            except (TypeError, KeyError, RuntimeError) as exc:
                logging.debug(f"Fleet: Lazy-load error for orchestrator '{name}': {exc}")

        # 3. Try Agents
        if "agents" in current_dict:
            agents = current_dict["agents"]
            try:
                # LazyAgentMap implements __getitem__ with fallback logic
                return agents[effective_name]
            except (KeyError, TypeError, AttributeError):
                if effective_name != name:
                    try:
                        return agents[name]
                    except (KeyError, TypeError, AttributeError):
                        pass

        raise AttributeError(f"'FleetManager' object has no attribute '{name}'")

    @property
    def telemetry(self: FleetManager) -> ObservabilityEngine:
        """Returns the observability engine for the fleet."""
        return self.orchestrators.telemetry

    @property
    def registry(self: FleetManager) -> ToolRegistry:
        """Returns the tool and agent registry."""
        return self.orchestrators.registry

    @property
    def signals(self: FleetManager) -> SignalRegistry:
        """Returns the signal bus for the fleet."""
        return self.orchestrators.signals

    @property
    def recorder(self: FleetManager) -> LocalContextRecorder:
        """Returns the local context recorder."""
        return self.orchestrators.recorder

    @property
    def sql_metadata(self: FleetManager) -> SqlMetadataHandler:
        """Returns the SQL metadata handler."""
        return self.orchestrators.sql_metadata

    @property
    def self_healing(self: FleetManager) -> SelfHealingOrchestrator:
        """Returns the self-healing orchestrator."""
        return self.orchestrators.self_healing

    @property
    def self_improvement(self: FleetManager) -> SelfImprovementOrchestrator:
        """Returns the self-improvement orchestrator."""
        return self.orchestrators.self_improvement

    @property
    def global_context(self: FleetManager) -> GlobalContextEngine:
        """Returns the global context engine."""
        return self.orchestrators.global_context

    @property
    def fallback(self: FleetManager) -> ModelFallbackEngine:
        """Returns the model fallback engine."""
        return self.orchestrators.fallback_engine

    @property
    def core(self: FleetManager) -> Any:
        """Returns the routing core."""
        return self.orchestrators.core

    @property
    def rl_selector(self: FleetManager) -> Any:
        """Returns the reinforcement learning selector."""
        return getattr(self.orchestrators, "r_l_selector", None) or getattr(self.orchestrators, "rl_selector", None)
