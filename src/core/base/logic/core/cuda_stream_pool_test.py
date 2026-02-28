# Auto-synced test for core/base/logic/core/cuda_stream_pool.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "cuda_stream_pool.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "StreamPriority"), "StreamPriority missing"
    assert hasattr(mod, "StreamState"), "StreamState missing"
    assert hasattr(mod, "StreamStats"), "StreamStats missing"
    assert hasattr(mod, "PooledStream"), "PooledStream missing"
    assert hasattr(mod, "PooledEvent"), "PooledEvent missing"
    assert hasattr(mod, "EventPool"), "EventPool missing"
    assert hasattr(mod, "CudaStreamPool"), "CudaStreamPool missing"
    assert hasattr(mod, "get_global_stream_pool"), "get_global_stream_pool missing"
    assert hasattr(mod, "reset_global_pool"), "reset_global_pool missing"
    assert hasattr(mod, "compute_stream"), "compute_stream missing"
    assert hasattr(mod, "comm_stream"), "comm_stream missing"
    assert hasattr(mod, "high_priority_stream"), "high_priority_stream missing"

