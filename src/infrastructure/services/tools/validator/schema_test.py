# Auto-synced test for infrastructure/services/tools/validator/schema.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "schema.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "validate_tool_call"), "validate_tool_call missing"
    assert hasattr(mod, "validate_tool_schema"), "validate_tool_schema missing"
    assert hasattr(mod, "validate_argument_type"), "validate_argument_type missing"

