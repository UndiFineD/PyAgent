# Auto-synced test for core/base/logic/parsers/reasoning_parser.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "reasoning_parser.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "ReasoningResult"), "ReasoningResult missing"
    assert hasattr(mod, "StreamingReasoningState"), "StreamingReasoningState missing"
    assert hasattr(mod, "ReasoningParser"), "ReasoningParser missing"
    assert hasattr(mod, "ReasoningParserManager"), "ReasoningParserManager missing"
    assert hasattr(mod, "reasoning_parser"), "reasoning_parser missing"
    assert hasattr(mod, "extract_reasoning"), "extract_reasoning missing"
    assert hasattr(mod, "create_streaming_parser"), "create_streaming_parser missing"
    assert hasattr(mod, "XMLReasoningParser"), "XMLReasoningParser missing"
    assert hasattr(mod, "JSONReasoningParser"), "JSONReasoningParser missing"
    assert hasattr(mod, "MarkdownReasoningParser"), "MarkdownReasoningParser missing"
    assert hasattr(mod, "IdentityReasoningParser"), "IdentityReasoningParser missing"

