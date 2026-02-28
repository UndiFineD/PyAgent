# Auto-synced test for infrastructure/compute/backend/vllm_advanced/streaming_engine.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "streaming_engine.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "StreamCallback"), "StreamCallback missing"
    assert hasattr(mod, "StreamingConfig"), "StreamingConfig missing"
    assert hasattr(mod, "StreamToken"), "StreamToken missing"
    assert hasattr(mod, "TokenStreamIterator"), "TokenStreamIterator missing"
    assert hasattr(mod, "StreamingVllmEngine"), "StreamingVllmEngine missing"

