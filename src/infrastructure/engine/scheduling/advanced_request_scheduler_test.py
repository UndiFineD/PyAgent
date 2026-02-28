# Auto-synced test for infrastructure/engine/scheduling/advanced_request_scheduler.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "advanced_request_scheduler.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "RequestPriority"), "RequestPriority missing"
    assert hasattr(mod, "RequestState"), "RequestState missing"
    assert hasattr(mod, "PreemptionReason"), "PreemptionReason missing"
    assert hasattr(mod, "SchedulerConfig"), "SchedulerConfig missing"
    assert hasattr(mod, "ScheduledRequest"), "ScheduledRequest missing"
    assert hasattr(mod, "RequestMetrics"), "RequestMetrics missing"
    assert hasattr(mod, "PriorityRequestQueue"), "PriorityRequestQueue missing"
    assert hasattr(mod, "AdvancedRequestScheduler"), "AdvancedRequestScheduler missing"
    assert hasattr(mod, "create_scheduler"), "create_scheduler missing"
    assert hasattr(mod, "priority_from_string"), "priority_from_string missing"

