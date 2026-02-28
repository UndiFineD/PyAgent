# Auto-synced test for infrastructure/compute/backend/vllm_advanced/guided_decoder.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "guided_decoder.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "ChoiceConstraint"), "ChoiceConstraint missing"
    assert hasattr(mod, "generate_choice"), "generate_choice missing"
    assert hasattr(mod, "generate_json"), "generate_json missing"
    assert hasattr(mod, "GuidedConfig"), "GuidedConfig missing"
    assert hasattr(mod, "GuidedDecoder"), "GuidedDecoder missing"
    assert hasattr(mod, "GuidedMode"), "GuidedMode missing"
    assert hasattr(mod, "JsonSchema"), "JsonSchema missing"
    assert hasattr(mod, "RegexPattern"), "RegexPattern missing"

