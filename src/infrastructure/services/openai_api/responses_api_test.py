# Auto-synced test for infrastructure/services/openai_api/responses_api.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "responses_api.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "AudioContent"), "AudioContent missing"
    assert hasattr(mod, "ContentPart"), "ContentPart missing"
    assert hasattr(mod, "ContentPartType"), "ContentPartType missing"
    assert hasattr(mod, "ConversationBuilder"), "ConversationBuilder missing"
    assert hasattr(mod, "ImageContent"), "ImageContent missing"
    assert hasattr(mod, "InMemoryResponseStore"), "InMemoryResponseStore missing"
    assert hasattr(mod, "Message"), "Message missing"
    assert hasattr(mod, "RefusalContent"), "RefusalContent missing"
    assert hasattr(mod, "Response"), "Response missing"
    assert hasattr(mod, "ResponseConfig"), "ResponseConfig missing"
    assert hasattr(mod, "ResponseOutput"), "ResponseOutput missing"
    assert hasattr(mod, "ResponsesAPIServer"), "ResponsesAPIServer missing"
    assert hasattr(mod, "ResponseStatus"), "ResponseStatus missing"
    assert hasattr(mod, "ResponseStore"), "ResponseStore missing"
    assert hasattr(mod, "ResponseType"), "ResponseType missing"
    assert hasattr(mod, "ResponseUsage"), "ResponseUsage missing"
    assert hasattr(mod, "RoleType"), "RoleType missing"
    assert hasattr(mod, "SSEEvent"), "SSEEvent missing"
    assert hasattr(mod, "SSEStream"), "SSEStream missing"
    assert hasattr(mod, "StreamingHandler"), "StreamingHandler missing"
    assert hasattr(mod, "TextContent"), "TextContent missing"
    assert hasattr(mod, "ToolCallContent"), "ToolCallContent missing"
    assert hasattr(mod, "ToolDefinition"), "ToolDefinition missing"
    assert hasattr(mod, "ToolType"), "ToolType missing"
    assert hasattr(mod, "parse_response_request"), "parse_response_request missing"

