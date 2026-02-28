# Auto-synced test for logic/agents/specialists/classification_agent.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "classification_agent.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "ClassificationType"), "ClassificationType missing"
    assert hasattr(mod, "ClassificationResult"), "ClassificationResult missing"
    assert hasattr(mod, "Taxonomy"), "Taxonomy missing"
    assert hasattr(mod, "ClassificationAgent"), "ClassificationAgent missing"

