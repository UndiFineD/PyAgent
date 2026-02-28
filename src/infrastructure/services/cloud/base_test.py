# Auto-synced test for infrastructure/services/cloud/base.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "base.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "InferenceRequest"), "InferenceRequest missing"
    assert hasattr(mod, "InferenceResponse"), "InferenceResponse missing"
    assert hasattr(mod, "CloudProviderBase"), "CloudProviderBase missing"
    assert hasattr(mod, "CloudProviderError"), "CloudProviderError missing"
    assert hasattr(mod, "RateLimitError"), "RateLimitError missing"
    assert hasattr(mod, "AuthenticationError"), "AuthenticationError missing"

