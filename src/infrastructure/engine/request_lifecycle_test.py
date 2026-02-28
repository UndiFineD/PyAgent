# Auto-synced test for infrastructure/engine/request_lifecycle.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "request_lifecycle.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "FinishReason"), "FinishReason missing"
    assert hasattr(mod, "RequestStatus"), "RequestStatus missing"
    assert hasattr(mod, "RequestEventType"), "RequestEventType missing"
    assert hasattr(mod, "is_valid_transition"), "is_valid_transition missing"
    assert hasattr(mod, "FINISH_REASON_STRINGS"), "FINISH_REASON_STRINGS missing"
    assert hasattr(mod, "RequestEvent"), "RequestEvent missing"
    assert hasattr(mod, "Request"), "Request missing"
    assert hasattr(mod, "RequestQueue"), "RequestQueue missing"
    assert hasattr(mod, "RequestTracker"), "RequestTracker missing"

