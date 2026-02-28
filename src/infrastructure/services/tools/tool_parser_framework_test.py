# Auto-synced test for infrastructure/services/tools/tool_parser_framework.py
import importlib.util
import pathlib


def _load_module():
    """Load the module under test from the same directory as this test file.
    """
    p = pathlib.Path(__file__).parent / "tool_parser_framework.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    if spec is None:
        raise RuntimeError(f"Failed to load module spec from {p}")
    mod = importlib.util.module_from_spec(spec)
    if spec.loader is None:
        raise RuntimeError(f"Failed to load module loader from {p}")
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    """Basic smoke test to ensure the module and expected symbols can be imported.
    """
    mod = _load_module()
    assert hasattr(mod, "ToolCall"), "ToolCall missing"
    assert hasattr(mod, "ToolParseResult"), "ToolParseResult missing"
    assert hasattr(mod, "JsonToolParser"), "JsonToolParser missing"
    assert hasattr(mod, "HermesToolParser"), "HermesToolParser missing"
    assert hasattr(mod, "Llama3ToolParser"), "Llama3ToolParser missing"
    assert hasattr(mod, "ToolParserRegistry"), "ToolParserRegistry missing"
    assert hasattr(mod, "StreamingToolParser"), "StreamingToolParser missing"
    assert hasattr(mod, "parse_tool_call"), "parse_tool_call missing"
    assert hasattr(mod, "extract_json_from_text"), "extract_json_from_text missing"
    assert hasattr(mod, "validate_tool_call"), "validate_tool_call missing"
    assert hasattr(mod, "validate_tool_schema"), "validate_tool_schema missing"
    assert hasattr(mod, "validate_argument_type"), "validate_argument_type missing"
