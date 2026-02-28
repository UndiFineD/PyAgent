# Auto-synced test for infrastructure/engine/structured/structured_output_params.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "structured_output_params.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "StructuredOutputType"), "StructuredOutputType missing"
    assert hasattr(mod, "ConstraintType"), "ConstraintType missing"
    assert hasattr(mod, "SchemaFormat"), "SchemaFormat missing"
    assert hasattr(mod, "GuidedDecodingBackend"), "GuidedDecodingBackend missing"
    assert hasattr(mod, "WhitespacePattern"), "WhitespacePattern missing"
    assert hasattr(mod, "OutputConstraint"), "OutputConstraint missing"
    assert hasattr(mod, "JsonSchemaConstraint"), "JsonSchemaConstraint missing"
    assert hasattr(mod, "RegexConstraint"), "RegexConstraint missing"
    assert hasattr(mod, "ChoiceConstraint"), "ChoiceConstraint missing"
    assert hasattr(mod, "GrammarConstraint"), "GrammarConstraint missing"
    assert hasattr(mod, "TypeConstraint"), "TypeConstraint missing"
    assert hasattr(mod, "StructuredOutputConfig"), "StructuredOutputConfig missing"
    assert hasattr(mod, "ValidationResult"), "ValidationResult missing"
    assert hasattr(mod, "ConstraintBuilder"), "ConstraintBuilder missing"
    assert hasattr(mod, "StructuredOutputValidator"), "StructuredOutputValidator missing"
    assert hasattr(mod, "create_json_constraint"), "create_json_constraint missing"
    assert hasattr(mod, "create_regex_constraint"), "create_regex_constraint missing"
    assert hasattr(mod, "create_choice_constraint"), "create_choice_constraint missing"
    assert hasattr(mod, "combine_constraints"), "combine_constraints missing"

