# Auto-synced test for core/base/logic/structures/cuda_stream_pool.py
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
    assert hasattr(mod, "CudaStreamPool"), "CudaStreamPool missing"

