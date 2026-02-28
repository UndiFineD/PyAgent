# Auto-synced test for observability/stats/subs_engine.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "subs_engine.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "AnnotationManager"), "AnnotationManager missing"
    assert hasattr(mod, "StatsAnnotationManager"), "StatsAnnotationManager missing"
    assert hasattr(mod, "SubscriptionManager"), "SubscriptionManager missing"
    assert hasattr(mod, "StatsSubscriptionManager"), "StatsSubscriptionManager missing"

