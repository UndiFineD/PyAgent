# Auto-synced test for observability/stats/formula_engine.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "formula_engine.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "FormulaValidation"), "FormulaValidation missing"
    assert hasattr(mod, "FormulaEngineCore"), "FormulaEngineCore missing"
    assert hasattr(mod, "FormulaEngine"), "FormulaEngine missing"

