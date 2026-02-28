# Auto-synced test for logic/agents/development/core/linter_core.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "linter_core.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "LintIssue"), "LintIssue missing"
    assert hasattr(mod, "LintResult"), "LintResult missing"
    assert hasattr(mod, "LinterCore"), "LinterCore missing"

