# Auto-synced test for core/base/state/agent_state_manager.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "agent_state_manager.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "EmergencyEventLog"), "EmergencyEventLog missing"
    assert hasattr(mod, "AgentCircuitBreaker"), "AgentCircuitBreaker missing"
    assert hasattr(mod, "AgentCheckpointManager"), "AgentCheckpointManager missing"
    assert hasattr(mod, "StateDriftDetector"), "StateDriftDetector missing"
    assert hasattr(mod, "StructuredErrorValidator"), "StructuredErrorValidator missing"
    assert hasattr(mod, "StateTransaction"), "StateTransaction missing"
    assert hasattr(mod, "AgentStateManager"), "AgentStateManager missing"

