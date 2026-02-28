# Auto-synced test for infrastructure/services/dev/agent_tests/enums.py
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
    assert hasattr(mod, "TestPriority"), "TestPriority missing"
    assert hasattr(mod, "TestStatus"), "TestStatus missing"
    assert hasattr(mod, "CoverageType"), "CoverageType missing"
    assert hasattr(mod, "BrowserType"), "BrowserType missing"
    assert hasattr(mod, "TestSourceType"), "TestSourceType missing"
    assert hasattr(mod, "MutationOperator"), "MutationOperator missing"
    assert hasattr(mod, "ExecutionMode"), "ExecutionMode missing"

