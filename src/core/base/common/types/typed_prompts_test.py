# Auto-synced test for core/base/common/types/typed_prompts.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "typed_prompts.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "TextPrompt"), "TextPrompt missing"
    assert hasattr(mod, "TokensPrompt"), "TokensPrompt missing"
    assert hasattr(mod, "EmbedsPrompt"), "EmbedsPrompt missing"
    assert hasattr(mod, "DataPrompt"), "DataPrompt missing"
    assert hasattr(mod, "ExplicitEncoderDecoderPrompt"), "ExplicitEncoderDecoderPrompt missing"
    assert hasattr(mod, "is_text_prompt"), "is_text_prompt missing"
    assert hasattr(mod, "is_tokens_prompt"), "is_tokens_prompt missing"
    assert hasattr(mod, "is_embeds_prompt"), "is_embeds_prompt missing"
    assert hasattr(mod, "is_data_prompt"), "is_data_prompt missing"
    assert hasattr(mod, "is_string_prompt"), "is_string_prompt missing"
    assert hasattr(mod, "is_explicit_encoder_decoder_prompt"), "is_explicit_encoder_decoder_prompt missing"
    assert hasattr(mod, "parse_prompt"), "parse_prompt missing"
    assert hasattr(mod, "get_prompt_text"), "get_prompt_text missing"
    assert hasattr(mod, "get_prompt_token_ids"), "get_prompt_token_ids missing"
    assert hasattr(mod, "has_multi_modal_data"), "has_multi_modal_data missing"
    assert hasattr(mod, "make_text_prompt"), "make_text_prompt missing"
    assert hasattr(mod, "make_tokens_prompt"), "make_tokens_prompt missing"
    assert hasattr(mod, "make_embeds_prompt"), "make_embeds_prompt missing"
    assert hasattr(mod, "make_encoder_decoder_prompt"), "make_encoder_decoder_prompt missing"
    assert hasattr(mod, "validate_prompt"), "validate_prompt missing"

