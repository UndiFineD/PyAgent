# Auto-synced test for core/base/logic/structures/memory_arena.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "memory_arena.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "ArenaStats"), "ArenaStats missing"
    assert hasattr(mod, "MemoryArena"), "MemoryArena missing"
    assert hasattr(mod, "TypedArena"), "TypedArena missing"
    assert hasattr(mod, "StackArena"), "StackArena missing"
    assert hasattr(mod, "SlabAllocator"), "SlabAllocator missing"
    assert hasattr(mod, "get_thread_arena"), "get_thread_arena missing"
    assert hasattr(mod, "temp_arena"), "temp_arena missing"
    assert hasattr(mod, "thread_temp_alloc"), "thread_temp_alloc missing"

