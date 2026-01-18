"""Pytest fixtures for test_agent tests."""

import pytest
import os
from pathlib import Path
from typing import Any, Optional

# Ensure git is in PATH for tests on Windows
for possible_git in [
    r"C:\Program Files\Git\cmd",
    r"C:\Program Files (x86)\Git\cmd",
    os.path.join(os.environ.get("LOCALAPPDATA", ""), "Programs", "Git", "cmd")
]:
    if os.path.exists(possible_git) and possible_git not in os.environ["PATH"]:
        os.environ["PATH"] = possible_git + os.pathsep + os.environ["PATH"]

from tests.utils.agent_test_utils import agent_dir_on_path, load_agent_module


@pytest.fixture
def agent_module() -> Any:
    """Load and return the agent module with legacy state injections."""
    with agent_dir_on_path():
        mod = load_agent_module("core/base/BaseAgent.py")

        # Configuration for legacy injections
        injections = [
            ("src.core.base.models.CoreEnums", ["AgentExecutionState", "AgentPriority", "ConfigFormat", "DiffOutputFormat", "HealthStatus", "LockType", "RateLimitStrategy"]),
            ("src.core.base.utils.AgentPriorityQueue", ["AgentPriorityQueue"]),
            ("src.core.base.utils.ValidationRuleManager", ["ValidationRuleManager"]),
            ("src.core.base.utils.TelemetryCollector", ["TelemetryCollector"]),
            ("src.core.base.utils.ConditionalExecutor", ["ConditionalExecutor"]),
            ("src.core.base.utils.TemplateManager", ["TemplateManager"]),
            ("src.core.base.utils.ResultCache", ["ResultCache"]),
            ("src.core.base.utils.ExecutionScheduler", ["ExecutionScheduler"]),
            ("src.core.base.utils.FileLockManager", ["FileLockManager"]),
            ("src.core.base.utils.RateLimiter", ["RateLimiter"]),
            ("src.core.base.utils.DiffGenerator", ["DiffGenerator"]),
            ("src.core.base.utils.FileLock", ["FileLock"]),
            ("src.core.base.DependencyGraph", ["DependencyGraph"]),
            ("src.core.base.ConfigLoader", ["ConfigLoader"]),
            ("src.core.base.GracefulShutdown", ["GracefulShutdown"]),
            ("src.core.base.IncrementalProcessor", ["IncrementalProcessor"]),
            ("src.core.base.managers.SystemManagers", ["ProfileManager", "HealthChecker"]),
            ("src.logic.agents.development.GitBranchProcessor", ["GitBranchProcessor"]),
            ("src.logic.orchestration.AgentChain", ["AgentChain"]),
            ("src.core.base.models.FleetModels", ["IncrementalState", "RateLimitConfig", "ShutdownState"]),
            ("src.core.base.models.AgentModels", ["AgentPluginConfig", "AgentHealthCheck"]),
            ("src.core.base.models.BaseModels", ["ExecutionCondition", "DiffResult"]),
        ]

        for module_path, attr_names in injections:
            _inject_from_module(mod, module_path, attr_names)

        _inject_special_shims(mod)
        _inject_legacy_agent_wrapper(mod)
        return mod


def _inject_from_module(target_mod: Any, module_path: str, attr_names: list[str]) -> None:
    """Safely imports attributes from a module and injects them into the target."""
    try:
        from importlib import import_module
        source_mod = import_module(module_path)
        for attr in attr_names:
            if hasattr(source_mod, attr):
                setattr(target_mod, attr, getattr(source_mod, attr))
    except ImportError:
        pass


def _inject_special_shims(mod: Any) -> None:
    """Injects complex shims (classes/methods) that require customization."""
    try:
        from src.core.base.AgentPluginBase import AgentPluginBase
        if hasattr(AgentPluginBase, "shutdown"):
            AgentPluginBase.shutdown = lambda self: None
        mod.AgentPluginBase = AgentPluginBase
    except ImportError:
        pass

    try:
        from src.core.base.models.BaseModels import ValidationRule as RealValidationRule
        mod.ValidationRule = _create_legacy_validation_rule_shim(RealValidationRule)
    except ImportError:
        pass

    try:
        from src.core.base.CircuitBreaker import CircuitBreaker as RealCircuitBreaker
        mod.CircuitBreaker = _create_legacy_circuit_breaker_shim(RealCircuitBreaker)
    except ImportError:
        pass


def _create_legacy_validation_rule_shim(real_cls: Any) -> Any:
    """Creates a shim for ValidationRule that supports legacy arguments."""
    class TestValidationRule:
        def __init__(self, name, pattern="", message="Validation failed", severity="error", **kwargs):
            self.name = name
            self.file_pattern = pattern or kwargs.get("file_pattern", "")
            self.pattern = self.file_pattern
            self.message = message or kwargs.get("error_message", "Validation failed")
            self.error_message = self.message
            self.severity = severity
            self.validator = kwargs.get("validator")
            self.kwargs = kwargs
    return TestValidationRule


def _create_legacy_circuit_breaker_shim(real_cls: Any) -> Any:
    """Creates a shim for CircuitBreaker with mock fallback."""
    class TestCircuitBreaker(real_cls):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            if not hasattr(self.resilience_core, "update_state"):
                self.resilience_core.update_state = lambda *a, **k: ("CLOSED", 0, 0)
    return TestCircuitBreaker


def _inject_legacy_agent_wrapper(mod: Any) -> None:
    """Injects the LegacyAgentWrapper into the module if BaseAgent is present."""
    if hasattr(mod, "BaseAgent"):
        from tests.utils.LegacySupport import create_legacy_agent_wrapper
        # Create wrapper that inherits from the current BaseAgent
        LegacyAgent = create_legacy_agent_wrapper(mod.BaseAgent)
        mod.Agent = LegacyAgent
        # Also alias BaseAgent to the wrapper for legacy tests that use mod.BaseAgent
        mod.BaseAgent = LegacyAgent


@pytest.fixture
def agent(agent_module: Any, tmp_path: Path) -> Any:
    """Create an Agent instance for testing."""
    Agent = agent_module.Agent
    test_file = tmp_path / "test_agent.py"
    test_file.write_text("print('hello')\n")
    return Agent([str(test_file)])
