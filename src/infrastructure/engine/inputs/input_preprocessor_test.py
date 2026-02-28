# Auto-synced test for infrastructure/engine/inputs/input_preprocessor.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "input_preprocessor.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "PromptType"), "PromptType missing"
    assert hasattr(mod, "InputFormat"), "InputFormat missing"
    assert hasattr(mod, "TextPrompt"), "TextPrompt missing"
    assert hasattr(mod, "TokensPrompt"), "TokensPrompt missing"
    assert hasattr(mod, "EmbedsPrompt"), "EmbedsPrompt missing"
    assert hasattr(mod, "EncoderDecoderPrompt"), "EncoderDecoderPrompt missing"
    assert hasattr(mod, "ChatMessage"), "ChatMessage missing"
    assert hasattr(mod, "ChatPrompt"), "ChatPrompt missing"
    assert hasattr(mod, "InputMetadata"), "InputMetadata missing"
    assert hasattr(mod, "ProcessedInput"), "ProcessedInput missing"
    assert hasattr(mod, "PromptTemplate"), "PromptTemplate missing"
    assert hasattr(mod, "PromptValidator"), "PromptValidator missing"
    assert hasattr(mod, "ConversationLinearizer"), "ConversationLinearizer missing"
    assert hasattr(mod, "InputPreprocessor"), "InputPreprocessor missing"
    assert hasattr(mod, "parse_prompt"), "parse_prompt missing"
    assert hasattr(mod, "estimate_tokens"), "estimate_tokens missing"

