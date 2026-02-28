# Auto-synced test for infrastructure/compute/backend/llm_backends/lm_studio_backend.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "lm_studio_backend.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "LMStudioConfig"), "LMStudioConfig missing"
    assert hasattr(mod, "CachedModel"), "CachedModel missing"
    assert hasattr(mod, "ModelCache"), "ModelCache missing"
    assert hasattr(mod, "LMStudioBackend"), "LMStudioBackend missing"
    assert hasattr(mod, "lmstudio_chat"), "lmstudio_chat missing"
    assert hasattr(mod, "lmstudio_stream"), "lmstudio_stream missing"
    assert hasattr(mod, "lmstudio_chat_async"), "lmstudio_chat_async missing"

