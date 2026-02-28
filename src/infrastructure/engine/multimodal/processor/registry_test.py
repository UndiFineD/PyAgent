# Auto-synced test for infrastructure/engine/multimodal/processor/registry.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "registry.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "MultiModalRegistry"), "MultiModalRegistry missing"
    assert hasattr(mod, "process_multimodal_inputs"), "process_multimodal_inputs missing"
    assert hasattr(mod, "get_placeholder_tokens"), "get_placeholder_tokens missing"

