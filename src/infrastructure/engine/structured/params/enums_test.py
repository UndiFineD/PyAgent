# Auto-synced test for infrastructure/engine/structured/params/enums.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "enums.py"
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

