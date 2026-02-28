# Auto-synced test for infrastructure/services/dev/agent_tests/testing_utils.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "testing_utils.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "VisualRegressionTester"), "VisualRegressionTester missing"
    assert hasattr(mod, "ContractTestRunner"), "ContractTestRunner missing"
    assert hasattr(mod, "ResultAggregator"), "ResultAggregator missing"
    assert hasattr(mod, "TestMetricsCollector"), "TestMetricsCollector missing"

