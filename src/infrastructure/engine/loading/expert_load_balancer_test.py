# Auto-synced test for infrastructure/engine/loading/expert_load_balancer.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "expert_load_balancer.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "ExpertType"), "ExpertType missing"
    assert hasattr(mod, "EplbMetrics"), "EplbMetrics missing"
    assert hasattr(mod, "ExpertMapping"), "ExpertMapping missing"
    assert hasattr(mod, "AbstractEplbPolicy"), "AbstractEplbPolicy missing"
    assert hasattr(mod, "DefaultEplbPolicy"), "DefaultEplbPolicy missing"
    assert hasattr(mod, "LocalityAwarePolicy"), "LocalityAwarePolicy missing"
    assert hasattr(mod, "ExpertLoadBalancer"), "ExpertLoadBalancer missing"
    assert hasattr(mod, "AsyncExpertRebalancer"), "AsyncExpertRebalancer missing"
    assert hasattr(mod, "compute_balanced_packing_rust"), "compute_balanced_packing_rust missing"
    assert hasattr(mod, "compute_expert_replication_rust"), "compute_expert_replication_rust missing"
    assert hasattr(mod, "compute_load_imbalance_rust"), "compute_load_imbalance_rust missing"

