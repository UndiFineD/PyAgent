# Auto-synced test for observability/stats/compilation_counter.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "compilation_counter.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "CompileEventType"), "CompileEventType missing"
    assert hasattr(mod, "CompileEvent"), "CompileEvent missing"
    assert hasattr(mod, "FunctionStats"), "FunctionStats missing"
    assert hasattr(mod, "CompilationCounter"), "CompilationCounter missing"
    assert hasattr(mod, "RecompileTracker"), "RecompileTracker missing"
    assert hasattr(mod, "TrendAnalyzer"), "TrendAnalyzer missing"
    assert hasattr(mod, "get_global_counter"), "get_global_counter missing"
    assert hasattr(mod, "reset_global_counter"), "reset_global_counter missing"

