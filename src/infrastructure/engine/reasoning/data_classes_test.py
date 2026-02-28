# Auto-synced test for infrastructure/engine/reasoning/data_classes.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "data_classes.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "ReasoningToken"), "ReasoningToken missing"
    assert hasattr(mod, "ThinkingBlock"), "ThinkingBlock missing"
    assert hasattr(mod, "ToolCall"), "ToolCall missing"
    assert hasattr(mod, "ToolCallResult"), "ToolCallResult missing"
    assert hasattr(mod, "ParseResult"), "ParseResult missing"

