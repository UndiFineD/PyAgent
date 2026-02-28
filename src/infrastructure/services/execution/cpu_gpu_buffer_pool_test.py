# Auto-synced test for infrastructure/services/execution/cpu_gpu_buffer_pool.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "cpu_gpu_buffer_pool.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "MemoryPlacement"), "MemoryPlacement missing"
    assert hasattr(mod, "CpuGpuBuffer"), "CpuGpuBuffer missing"
    assert hasattr(mod, "UvaBufferPool"), "UvaBufferPool missing"
    assert hasattr(mod, "PinnedMemoryManager"), "PinnedMemoryManager missing"
    assert hasattr(mod, "copy_with_indices"), "copy_with_indices missing"
    assert hasattr(mod, "scatter_with_indices"), "scatter_with_indices missing"
    assert hasattr(mod, "pad_to_multiple"), "pad_to_multiple missing"
    assert hasattr(mod, "compute_cumsum_offsets"), "compute_cumsum_offsets missing"
    assert hasattr(mod, "flatten_with_offsets"), "flatten_with_offsets missing"
    assert hasattr(mod, "split_by_offsets"), "split_by_offsets missing"

