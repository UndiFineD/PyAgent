# Auto-synced test for infrastructure/engine/conversation/context/manager.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "manager.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "ContextManager"), "ContextManager missing"
    assert hasattr(mod, "get_context_manager"), "get_context_manager missing"
    assert hasattr(mod, "create_context"), "create_context missing"
    assert hasattr(mod, "merge_contexts"), "merge_contexts missing"
    assert hasattr(mod, "restore_context"), "restore_context missing"

