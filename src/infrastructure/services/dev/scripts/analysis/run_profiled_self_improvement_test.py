# Auto-synced test for infrastructure/services/dev/scripts/analysis/run_profiled_self_improvement.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "run_profiled_self_improvement.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "RustFunctionStats"), "RustFunctionStats missing"
    assert hasattr(mod, "RustProfiler"), "RustProfiler missing"
    assert hasattr(mod, "ComprehensiveProfileAnalyzer"), "ComprehensiveProfileAnalyzer missing"
    assert hasattr(mod, "save_profile_report"), "save_profile_report missing"

