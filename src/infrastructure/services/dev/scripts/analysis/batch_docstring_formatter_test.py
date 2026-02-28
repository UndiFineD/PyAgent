# Auto-synced test for infrastructure/services/dev/scripts/analysis/batch_docstring_formatter.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "batch_docstring_formatter.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "DocstringStandards"), "DocstringStandards missing"
    assert hasattr(mod, "DocstringAnalyzer"), "DocstringAnalyzer missing"
    assert hasattr(mod, "DocstringFixer"), "DocstringFixer missing"
    assert hasattr(mod, "main"), "main missing"

