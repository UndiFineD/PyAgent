# Auto-synced test for infrastructure/engine/reasoning/implementations.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "implementations.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "DeepSeekReasoningParser"), "DeepSeekReasoningParser missing"
    assert hasattr(mod, "QwenReasoningParser"), "QwenReasoningParser missing"
    assert hasattr(mod, "GenericReasoningParser"), "GenericReasoningParser missing"
    assert hasattr(mod, "OpenAIToolParser"), "OpenAIToolParser missing"
    assert hasattr(mod, "HermesToolParser"), "HermesToolParser missing"

