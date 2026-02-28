# Auto-synced test for core/base/logic/structures/uva_buffer_pool.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "uva_buffer_pool.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "BufferState"), "BufferState missing"
    assert hasattr(mod, "AllocationStrategy"), "AllocationStrategy missing"
    assert hasattr(mod, "BufferStats"), "BufferStats missing"
    assert hasattr(mod, "UvaBuffer"), "UvaBuffer missing"
    assert hasattr(mod, "UvaBufferPool"), "UvaBufferPool missing"
    assert hasattr(mod, "UvaBackedTensor"), "UvaBackedTensor missing"
    assert hasattr(mod, "create_uva_buffer"), "create_uva_buffer missing"
    assert hasattr(mod, "create_uva_pool"), "create_uva_pool missing"

