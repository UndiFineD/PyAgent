# Auto-synced test for infrastructure/services/dev/scripts/analysis/run_fleet_self_improvement.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "run_fleet_self_improvement.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "DirectiveParser"), "DirectiveParser missing"
    assert hasattr(mod, "IntelligenceHarvester"), "IntelligenceHarvester missing"
    assert hasattr(mod, "CycleOrchestrator"), "CycleOrchestrator missing"
    assert hasattr(mod, "run_cycle"), "run_cycle missing"
    assert hasattr(mod, "consult_external_models"), "consult_external_models missing"
    assert hasattr(mod, "main"), "main missing"

