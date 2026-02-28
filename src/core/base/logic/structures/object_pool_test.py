# Auto-synced test for core/base/logic/structures/object_pool.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "object_pool.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "Resettable"), "Resettable missing"
    assert hasattr(mod, "PoolStats"), "PoolStats missing"
    assert hasattr(mod, "ObjectPool"), "ObjectPool missing"
    assert hasattr(mod, "TypedObjectPool"), "TypedObjectPool missing"
    assert hasattr(mod, "BufferPool"), "BufferPool missing"
    assert hasattr(mod, "TieredBufferPool"), "TieredBufferPool missing"
    assert hasattr(mod, "PooledContextManager"), "PooledContextManager missing"
    assert hasattr(mod, "get_list_pool"), "get_list_pool missing"
    assert hasattr(mod, "get_dict_pool"), "get_dict_pool missing"
    assert hasattr(mod, "get_set_pool"), "get_set_pool missing"
    assert hasattr(mod, "pooled_list"), "pooled_list missing"
    assert hasattr(mod, "pooled_dict"), "pooled_dict missing"
    assert hasattr(mod, "pooled_set"), "pooled_set missing"

