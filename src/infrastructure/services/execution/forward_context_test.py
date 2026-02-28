# Auto-synced test for infrastructure/services/execution/forward_context.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "forward_context.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "BatchDescriptor"), "BatchDescriptor missing"
    assert hasattr(mod, "DPMetadata"), "DPMetadata missing"
    assert hasattr(mod, "ForwardContext"), "ForwardContext missing"
    assert hasattr(mod, "get_forward_context"), "get_forward_context missing"
    assert hasattr(mod, "is_forward_context_available"), "is_forward_context_available missing"
    assert hasattr(mod, "create_forward_context"), "create_forward_context missing"
    assert hasattr(mod, "set_forward_context"), "set_forward_context missing"
    assert hasattr(mod, "ForwardTimingTracker"), "ForwardTimingTracker missing"
    assert hasattr(mod, "get_timing_tracker"), "get_timing_tracker missing"

