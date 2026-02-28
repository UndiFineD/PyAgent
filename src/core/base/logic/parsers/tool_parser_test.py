# Auto-synced test for core/base/logic/parsers/tool_parser.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "tool_parser.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "ToolCall"), "ToolCall missing"
    assert hasattr(mod, "ExtractedToolCalls"), "ExtractedToolCalls missing"
    assert hasattr(mod, "StreamingToolCallDelta"), "StreamingToolCallDelta missing"
    assert hasattr(mod, "ToolParser"), "ToolParser missing"
    assert hasattr(mod, "JSONToolParser"), "JSONToolParser missing"
    assert hasattr(mod, "XMLToolParser"), "XMLToolParser missing"
    assert hasattr(mod, "ToolParserManager"), "ToolParserManager missing"
    assert hasattr(mod, "tool_parser"), "tool_parser missing"
    assert hasattr(mod, "extract_tool_calls"), "extract_tool_calls missing"

