# Auto-synced test for infrastructure/services/dev/agent_tests/test_management.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "test_management.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "BaselineComparisonResult"), "BaselineComparisonResult missing"
    assert hasattr(mod, "BaselineManager"), "BaselineManager missing"
    assert hasattr(mod, "DIContainer"), "DIContainer missing"
    assert hasattr(mod, "TestPrioritizer"), "TestPrioritizer missing"
    assert hasattr(mod, "FlakinessDetector"), "FlakinessDetector missing"
    assert hasattr(mod, "QuarantineManager"), "QuarantineManager missing"
    assert hasattr(mod, "ImpactAnalyzer"), "ImpactAnalyzer missing"
    assert hasattr(mod, "ContractValidator"), "ContractValidator missing"
    assert hasattr(mod, "TestDocGenerator"), "TestDocGenerator missing"

