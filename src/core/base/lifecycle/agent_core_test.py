# Auto-synced test for core/base/lifecycle/agent_core.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "agent_core.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "CodeQualityReport"), "CodeQualityReport missing"
    assert hasattr(mod, "LogicCore"), "LogicCore missing"
    assert hasattr(mod, "BaseCore"), "BaseCore missing"
    assert hasattr(mod, "AgentCore"), "AgentCore missing"

