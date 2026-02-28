# Auto-synced test for core/base/logic/structures/cpu_gpu_buffer.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "cpu_gpu_buffer.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "CpuGpuBuffer"), "CpuGpuBuffer missing"
    assert hasattr(mod, "is_pin_memory_available"), "is_pin_memory_available missing"
    assert hasattr(mod, "get_device"), "get_device missing"
    assert hasattr(mod, "CpuGpuBufferPool"), "CpuGpuBufferPool missing"

