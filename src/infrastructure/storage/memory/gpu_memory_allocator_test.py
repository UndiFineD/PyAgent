# Auto-synced test for infrastructure/storage/memory/gpu_memory_allocator.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "gpu_memory_allocator.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "MemoryState"), "MemoryState missing"
    assert hasattr(mod, "AllocationStrategy"), "AllocationStrategy missing"
    assert hasattr(mod, "MemoryRegion"), "MemoryRegion missing"
    assert hasattr(mod, "MemorySnapshot"), "MemorySnapshot missing"
    assert hasattr(mod, "MemoryPoolConfig"), "MemoryPoolConfig missing"
    assert hasattr(mod, "MemoryPressureEvent"), "MemoryPressureEvent missing"
    assert hasattr(mod, "CuMemAllocator"), "CuMemAllocator missing"
    assert hasattr(mod, "MultiGPUMemoryBalancer"), "MultiGPUMemoryBalancer missing"

