# Auto-synced test for core/base/common/base_exceptions.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "base_exceptions.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "PyAgentException"), "PyAgentException missing"
    assert hasattr(mod, "InfrastructureError"), "InfrastructureError missing"
    assert hasattr(mod, "LogicError"), "LogicError missing"
    assert hasattr(mod, "SecurityError"), "SecurityError missing"
    assert hasattr(mod, "ModelError"), "ModelError missing"
    assert hasattr(mod, "ConfigurationError"), "ConfigurationError missing"
    assert hasattr(mod, "CycleInterrupt"), "CycleInterrupt missing"

