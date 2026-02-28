# Auto-synced test for core/base/common/models/base_models.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "base_models.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "CacheEntry"), "CacheEntry missing"
    assert hasattr(mod, "AuthConfig"), "AuthConfig missing"
    assert hasattr(mod, "ConfigProfile"), "ConfigProfile missing"
    assert hasattr(mod, "SerializationConfig"), "SerializationConfig missing"
    assert hasattr(mod, "FilePriorityConfig"), "FilePriorityConfig missing"
    assert hasattr(mod, "ValidationRule"), "ValidationRule missing"
    assert hasattr(mod, "ExecutionCondition"), "ExecutionCondition missing"
    assert hasattr(mod, "DiffResult"), "DiffResult missing"
    assert hasattr(mod, "ModelConfig"), "ModelConfig missing"
    assert hasattr(mod, "EventHook"), "EventHook missing"

