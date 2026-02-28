# Auto-synced test for infrastructure/engine/chat_templates/registry/utils.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "utils.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "register_template"), "register_template missing"
    assert hasattr(mod, "get_template"), "get_template missing"
    assert hasattr(mod, "render_template"), "render_template missing"
    assert hasattr(mod, "detect_template_type"), "detect_template_type missing"

