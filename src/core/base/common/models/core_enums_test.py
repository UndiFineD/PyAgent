# Auto-synced test for core/base/common/models/core_enums.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "core_enums.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "AgentState"), "AgentState missing"
    assert hasattr(mod, "ResponseQuality"), "ResponseQuality missing"
    assert hasattr(mod, "FailureClassification"), "FailureClassification missing"
    assert hasattr(mod, "EventType"), "EventType missing"
    assert hasattr(mod, "AuthMethod"), "AuthMethod missing"
    assert hasattr(mod, "SerializationFormat"), "SerializationFormat missing"
    assert hasattr(mod, "FilePriority"), "FilePriority missing"
    assert hasattr(mod, "InputType"), "InputType missing"
    assert hasattr(mod, "AgentType"), "AgentType missing"
    assert hasattr(mod, "MessageRole"), "MessageRole missing"
    assert hasattr(mod, "AgentEvent"), "AgentEvent missing"
    assert hasattr(mod, "AgentExecutionState"), "AgentExecutionState missing"
    assert hasattr(mod, "AgentPriority"), "AgentPriority missing"
    assert hasattr(mod, "ConfigFormat"), "ConfigFormat missing"
    assert hasattr(mod, "DiffOutputFormat"), "DiffOutputFormat missing"
    assert hasattr(mod, "HealthStatus"), "HealthStatus missing"
    assert hasattr(mod, "LockType"), "LockType missing"
    assert hasattr(mod, "RateLimitStrategy"), "RateLimitStrategy missing"

