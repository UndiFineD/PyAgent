# Auto-synced test for core/base/common/base_interfaces.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "base_interfaces.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "AgentInterface"), "AgentInterface missing"
    assert hasattr(mod, "OrchestratorInterface"), "OrchestratorInterface missing"
    assert hasattr(mod, "CoreInterface"), "CoreInterface missing"
    assert hasattr(mod, "ContextRecorderInterface"), "ContextRecorderInterface missing"
    assert hasattr(mod, "Loadable"), "Loadable missing"
    assert hasattr(mod, "Saveable"), "Saveable missing"
    assert hasattr(mod, "Component"), "Component missing"

