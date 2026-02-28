# Auto-synced test for infrastructure/services/tools/parser/base.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "base.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "ToolParserType"), "ToolParserType missing"
    assert hasattr(mod, "ToolCallStatus"), "ToolCallStatus missing"
    assert hasattr(mod, "ToolParameter"), "ToolParameter missing"
    assert hasattr(mod, "ToolCall"), "ToolCall missing"
    assert hasattr(mod, "ToolParseResult"), "ToolParseResult missing"
    assert hasattr(mod, "StreamingToolState"), "StreamingToolState missing"
    assert hasattr(mod, "ToolParser"), "ToolParser missing"
    assert hasattr(mod, "extract_json_from_text"), "extract_json_from_text missing"

