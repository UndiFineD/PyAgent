# Auto-synced test for infrastructure/engine/decoding/grammar/registry.py
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
    assert hasattr(mod, "GrammarCompiler"), "GrammarCompiler missing"
    assert hasattr(mod, "StructuredOutputManager"), "StructuredOutputManager missing"
    assert hasattr(mod, "compile_grammar"), "compile_grammar missing"
    assert hasattr(mod, "validate_structured_output_params"), "validate_structured_output_params missing"

