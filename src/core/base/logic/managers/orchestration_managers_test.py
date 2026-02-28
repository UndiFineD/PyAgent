# Auto-synced test for core/base/logic/managers/orchestration_managers.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "orchestration_managers.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "AgentComposer"), "AgentComposer missing"
    assert hasattr(mod, "ModelSelector"), "ModelSelector missing"
    assert hasattr(mod, "ABTest"), "ABTest missing"
    assert hasattr(mod, "QualityScorer"), "QualityScorer missing"

