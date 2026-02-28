# Auto-synced test for infrastructure/services/execution/cuda_graph_manager.py
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
    assert hasattr(mod, "CUDAGraphRegistry"), "CUDAGraphRegistry missing"
    assert hasattr(mod, "compute_graph_key"), "compute_graph_key missing"
    assert hasattr(mod, "generate_warmup_sizes"), "generate_warmup_sizes missing"
    assert hasattr(mod, "CUDAGraphManager"), "CUDAGraphManager missing"

