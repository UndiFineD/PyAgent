# Auto-synced test for infrastructure/engine/structured/params/constraints.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "constraints.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "OutputConstraint"), "OutputConstraint missing"
    assert hasattr(mod, "JsonSchemaConstraint"), "JsonSchemaConstraint missing"
    assert hasattr(mod, "RegexConstraint"), "RegexConstraint missing"
    assert hasattr(mod, "ChoiceConstraint"), "ChoiceConstraint missing"
    assert hasattr(mod, "GrammarConstraint"), "GrammarConstraint missing"
    assert hasattr(mod, "TypeConstraint"), "TypeConstraint missing"

