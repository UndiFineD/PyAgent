# Auto-synced test for infrastructure/services/metrics/lo_ra_stats_manager.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "lo_ra_stats_manager.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "LoRALoadState"), "LoRALoadState missing"
    assert hasattr(mod, "RequestStatus"), "RequestStatus missing"
    assert hasattr(mod, "LoRAAdapterInfo"), "LoRAAdapterInfo missing"
    assert hasattr(mod, "LoRARequestState"), "LoRARequestState missing"
    assert hasattr(mod, "LoRAStats"), "LoRAStats missing"
    assert hasattr(mod, "LoRAStatsManager"), "LoRAStatsManager missing"
    assert hasattr(mod, "RequestLifecycle"), "RequestLifecycle missing"
    assert hasattr(mod, "RequestLifecycleManager"), "RequestLifecycleManager missing"

