from __future__ import annotations

# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

import logging
# LocalContextRecorder lives under the classes backend package
from src.classes.backend.LocalContextRecorder import LocalContextRecorder
# SqlMetadataHandler not present in infrastructure; orchestration layer already provides it via orchestrators
# so we don't need to import it here
# MetricsEngine imported previously but not used in this mixin
from typing import Any, TYPE_CHECKING

# ToolRegistry is only needed for type hints in some properties; defer import to TYPE_CHECKING to
# avoid circular import with FleetManager.
# from src.infrastructure.orchestration.ToolRegistry import ToolRegistry
# The following imports were used for type hints only but caused import errors or circular
# dependencies. The associated properties are annotated as Any instead.
# from src.infrastructure.orchestration.signals.SignalRegistry import SignalRegistry
# from src.infrastructure.orchestration.healing.SelfHealingOrchestrator import (
#     SelfHealingOrchestrator,
# )
# from src.infrastructure.orchestration.intel.SelfImprovementOrchestrator import (
#     SelfImprovementOrchestrator,
# )
# from src.logic.agents.cognitive.context.engines.GlobalContextEngine import (
#     GlobalContextEngine,
# )

if TYPE_CHECKING:
    from src.infrastructure.fleet.FleetManager import FleetManager
    # These are used only as return types for properties
    from src.observability.stats import ObservabilityEngine
    from src.core.base.models import ModelFallbackEngine
    from src.infrastructure.orchestration.ToolRegistry import ToolRegistry
    # Type hints for other orchestrator components
    # from src.infrastructure.orchestration.SignalRegistry import SignalRegistry
    # from src.infrastructure.orchestration.SelfHealingOrchestrator import SelfHealingOrchestrator
    # from src.infrastructure.orchestration.SelfImprovementOrchestrator import SelfImprovementOrchestrator
    # from src.logic.agents.cognitive.context.utils.GlobalContextEngine import GlobalContextEngine


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
        hints = self.__dict__.get("_capability_hints", {})
        if effective_name in hints:
            target = hints[effective_name]
            # Avoid infinite recursion if target resolves back to name or effective_name
            if target != effective_name and target != name:
                try:
                    return getattr(self, target)
                except AttributeError:
                    pass
        elif name != effective_name and name in hints:
            target = hints[name]
            # Avoid recursion if target resolves back to name or effective_name
            if target != name and target != effective_name:
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
            except Exception as e:
                logging.debug(f"Fleet: Lazy-load error for orchestrator '{name}': {e}")

        # 3. Try Agents
        if "agents" in current_dict:
            agents = current_dict["agents"]
            try:
                # LazyAgentMap implements __getitem__ with fallback logic
                return agents[effective_name]
            except (KeyError, Exception):
                if effective_name != name:
                    try:
                        return agents[name]
                    except (KeyError, Exception):
                        pass

        raise AttributeError(f"'FleetManager' object has no attribute '{name}'")

    @property
    def telemetry(self: FleetManager) -> Any:
        return self.orchestrators.telemetry

    @property
    # return type annotated as Any to avoid import cycles
    def registry(self: FleetManager) -> Any:
        return self.orchestrators.registry

    @property
    def signals(self: FleetManager) -> Any:
        return self.orchestrators.signals

    @property
    def recorder(self: FleetManager) -> LocalContextRecorder:
        return self.orchestrators.recorder

    @property
    # SqlMetadataHandler type isn't available here; use Any to avoid import issues
    def sql_metadata(self: FleetManager) -> Any:
        return self.orchestrators.sql_metadata

    @property
    def self_healing(self: FleetManager) -> Any:
        return self.orchestrators.self_healing

    @property
    def self_improvement(self: FleetManager) -> Any:
        return self.orchestrators.self_improvement

    @property
    def global_context(self: FleetManager) -> Any:
        return self.orchestrators.global_context

    @property
    def fallback(self: FleetManager) -> ModelFallbackEngine:
        return self.orchestrators.fallback_engine

    @property
    def core(self: FleetManager) -> Any:
        return self.orchestrators.core

    @property
    def rl_selector(self: FleetManager) -> Any:
        return getattr(self.orchestrators, "r_l_selector", None) or getattr(
            self.orchestrators, "rl_selector", None
        )
