# Auto-synced test for infrastructure/engine/reasoning/engine.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "engine.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "ReasoningEngine"), "ReasoningEngine missing"
    assert hasattr(mod, "create_reasoning_engine"), "create_reasoning_engine missing"
    assert hasattr(mod, "create_tool_parser"), "create_tool_parser missing"

