# Auto-synced test for infrastructure/compute/cuda/cuda_graph_manager.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "cuda_graph_manager.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "CUDAGraphMode"), "CUDAGraphMode missing"
    assert hasattr(mod, "BatchDescriptor"), "BatchDescriptor missing"
    assert hasattr(mod, "CUDAGraphEntry"), "CUDAGraphEntry missing"
    assert hasattr(mod, "CUDAGraphOptions"), "CUDAGraphOptions missing"
    assert hasattr(mod, "CUDAGraphStats"), "CUDAGraphStats missing"
    assert hasattr(mod, "MockCUDAGraph"), "MockCUDAGraph missing"
    assert hasattr(mod, "CUDAGraphWrapper"), "CUDAGraphWrapper missing"
    assert hasattr(mod, "AdaptiveCUDAGraphWrapper"), "AdaptiveCUDAGraphWrapper missing"
    assert hasattr(mod, "cudagraph_context"), "cudagraph_context missing"
    assert hasattr(mod, "get_cudagraph_sizes"), "get_cudagraph_sizes missing"

