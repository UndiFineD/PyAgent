# Auto-synced test for infrastructure/engine/structured/params/factory.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "factory.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "create_json_constraint"), "create_json_constraint missing"
    assert hasattr(mod, "create_regex_constraint"), "create_regex_constraint missing"
    assert hasattr(mod, "create_choice_constraint"), "create_choice_constraint missing"
    assert hasattr(mod, "combine_constraints"), "combine_constraints missing"

