# Auto-synced test for infrastructure/services/dev/agent_tests/models.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "models.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "TestCase"), "TestCase missing"
    assert hasattr(mod, "TestRun"), "TestRun missing"
    assert hasattr(mod, "CoverageGap"), "CoverageGap missing"
    assert hasattr(mod, "TestFactory"), "TestFactory missing"
    assert hasattr(mod, "VisualRegressionConfig"), "VisualRegressionConfig missing"
    assert hasattr(mod, "ContractTest"), "ContractTest missing"
    assert hasattr(mod, "TestEnvironment"), "TestEnvironment missing"
    assert hasattr(mod, "ExecutionTrace"), "ExecutionTrace missing"
    assert hasattr(mod, "TestDependency"), "TestDependency missing"
    assert hasattr(mod, "CrossBrowserConfig"), "CrossBrowserConfig missing"
    assert hasattr(mod, "AggregatedResult"), "AggregatedResult missing"
    assert hasattr(mod, "Mutation"), "Mutation missing"
    assert hasattr(mod, "GeneratedTest"), "GeneratedTest missing"
    assert hasattr(mod, "TestProfile"), "TestProfile missing"
    assert hasattr(mod, "ScheduleSlot"), "ScheduleSlot missing"
    assert hasattr(mod, "ProvisionedEnvironment"), "ProvisionedEnvironment missing"
    assert hasattr(mod, "ValidationResult"), "ValidationResult missing"
    assert hasattr(mod, "Recording"), "Recording missing"
    assert hasattr(mod, "ReplayResult"), "ReplayResult missing"

