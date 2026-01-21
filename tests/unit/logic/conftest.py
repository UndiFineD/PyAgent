"""Pytest fixtures for test_agent tests."""

import os
from pathlib import Path
from typing import Any

import pytest

from tests.utils.agent_test_utils import agent_dir_on_path, load_agent_module


def ensure_git_on_path() -> None:
    """Ensure git is in PATH for tests on Windows."""
    for possible_git in [
        r"C:\Program Files\Git\cmd",
        r"C:\Program Files (x86)\Git\cmd",
        os.path.join(os.environ.get("LOCALAPPDATA", ""), "Programs", "Git", "cmd")
    ]:
        if os.path.exists(possible_git) and possible_git not in os.environ["PATH"]:
            os.environ["PATH"] = possible_git + os.pathsep + os.environ["PATH"]


# Call it early
ensure_git_on_path()


@pytest.fixture
def agent_module() -> Any:
    """Load and return the agent module with legacy state injections."""
    with agent_dir_on_path():
        mod = load_agent_module("src/core/base/lifecycle/base_agent.py")

        # Configuration for legacy injections
        injections = [
            (
                "src.core.base.common.models.core_enums",
                [
                    "AgentExecutionState",
                    "AgentPriority",
                    "ConfigFormat",
                    "DiffOutputFormat",
                    "HealthStatus",
                    "LockType",
                    "RateLimitStrategy"
                ]
            ),
            (
                "src.core.base.common.utils.agent_priority_queue",
                ["AgentPriorityQueue"]
            ),
            (
                "src.core.base.common.utils.validation_rule_manager",
                ["ValidationRuleManager"]
            ),
            (
                "src.core.base.common.utils.telemetry_collector",
                ["TelemetryCollector"]
            ),
            (
                "src.core.base.common.utils.conditional_executor",
                ["ConditionalExecutor"]
            ),
            (
                "src.core.base.common.utils.template_manager",
                ["TemplateManager"]
            ),
            (
                "src.core.base.common.utils.result_cache",
                ["ResultCache"]
            ),
            (
                "src.core.base.common.utils.execution_scheduler",
                ["ExecutionScheduler"]
            ),
            (
                "src.core.base.common.utils.file_lock_manager",
                ["FileLockManager"]
            ),
            (
                "src.core.base.common.utils.rate_limiter",
                ["RateLimiter"]
            ),
            (
                "src.core.base.common.utils.diff_generator",
                ["DiffGenerator"]
            ),
            (
                "src.core.base.common.utils.file_lock",
                ["FileLock"]
            ),
            (
                "src.core.base.logic.dependency_graph",
                ["DependencyGraph"]
            ),
            (
                "src.core.base.common.config_loader",
                ["ConfigLoader"]
            ),
            (
                "src.core.base.lifecycle.graceful_shutdown",
                ["GracefulShutdown"]
            ),
            (
                "src.core.base.logic.incremental_processor",
                ["IncrementalProcessor"]
            ),
            (
                "src.core.base.logic.managers.system_managers",
                ["ProfileManager", "HealthChecker"]
            ),
            (
                "src.logic.agents.development.git_branch_processor",
                ["GitBranchProcessor"]
            ),
            (
                "src.logic.orchestration.agent_chain",
                ["AgentChain"]
            ),
            (
                "src.core.base.common.models.fleet_models",
                ["IncrementalState", "RateLimitConfig", "ShutdownState"]
            ),
            (
                "src.core.base.common.models.agent_models",
                ["AgentPluginConfig", "AgentHealthCheck"]
            ),
            (
                "src.core.base.common.models.base_models",
                ["ExecutionCondition", "DiffResult"]
            ),
        ]

        for module_path, attr_names in injections:
            _inject_from_module(mod, module_path, attr_names)

        _inject_special_shims(mod)
        _inject_legacy_agent_wrapper(mod)
        return mod


def _inject_from_module(target_mod: Any, module_path: str, attr_names: list[str]) -> None:
    """Safely imports attributes from a module and injects them into the target."""
    try:
        # pylint: disable=import-outside-toplevel
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
        # pylint: disable=import-outside-toplevel
        from src.core.base.logic.agent_plugin_base import AgentPluginBase
        if hasattr(AgentPluginBase, "shutdown"):
            AgentPluginBase.shutdown = lambda self: None
        mod.AgentPluginBase = AgentPluginBase
    except ImportError:
        pass

    try:
        # pylint: disable=import-outside-toplevel
        from src.core.base.common.models.base_models import ValidationRule as RealValidationRule
        mod.ValidationRule = _create_legacy_validation_rule_shim(RealValidationRule)
    except ImportError:
        pass

    try:
        # pylint: disable=import-outside-toplevel
        from src.core.base.logic.circuit_breaker import CircuitBreaker as RealCircuitBreaker
        mod.CircuitBreaker = _create_legacy_circuit_breaker_shim(RealCircuitBreaker)
    except ImportError:
        pass


def _create_legacy_validation_rule_shim(_real_cls: Any) -> Any:
    """Creates a shim for ValidationRule that supports legacy arguments."""
    class TestValidationRule:
        """Legacy shim for ValidationRule."""
        def __init__(
            self, name, pattern="", message="Validation failed", severity="error", **kwargs
        ):
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
        """Legacy shim for CircuitBreaker."""
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            if not hasattr(self.resilience_core, "update_state"):
                self.resilience_core.update_state = lambda *a, **k: ("CLOSED", 0, 0)
    return TestCircuitBreaker


def _inject_legacy_agent_wrapper(mod: Any) -> None:
    """Injects the LegacyAgentWrapper into the module if BaseAgent is present."""
    if hasattr(mod, "BaseAgent"):
        # pylint: disable=import-outside-toplevel
        from tests.utils.legacy_support import create_legacy_agent_wrapper
        # Create wrapper that inherits from the current BaseAgent
        LegacyAgent = create_legacy_agent_wrapper(mod.BaseAgent)
        mod.Agent = LegacyAgent
        # Also alias BaseAgent to the wrapper for legacy tests that use mod.BaseAgent
        mod.BaseAgent = LegacyAgent


@pytest.fixture
def agent(mod: Any, tmp_path: Path) -> Any:
    """Create an Agent instance for testing."""
    agent_cls = mod.Agent
    test_file = tmp_path / "test_agent.py"
    test_file.write_text("print('hello')\n")
    return agent_cls([str(test_file)])
