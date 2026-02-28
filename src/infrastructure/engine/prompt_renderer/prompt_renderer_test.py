# Auto-synced test for infrastructure/engine/prompt_renderer/prompt_renderer.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "prompt_renderer.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "CacheSaltGenerator"), "CacheSaltGenerator missing"
    assert hasattr(mod, "ChatRenderer"), "ChatRenderer missing"
    assert hasattr(mod, "CompletionRenderer"), "CompletionRenderer missing"
    assert hasattr(mod, "EmbeddingInput"), "EmbeddingInput missing"
    assert hasattr(mod, "EmbeddingLoader"), "EmbeddingLoader missing"
    assert hasattr(mod, "InputType"), "InputType missing"
    assert hasattr(mod, "MultimodalInput"), "MultimodalInput missing"
    assert hasattr(mod, "PromptConfig"), "PromptConfig missing"
    assert hasattr(mod, "PromptRenderer"), "PromptRenderer missing"
    assert hasattr(mod, "RenderMode"), "RenderMode missing"
    assert hasattr(mod, "RenderResult"), "RenderResult missing"
    assert hasattr(mod, "TruncationManager"), "TruncationManager missing"
    assert hasattr(mod, "TruncationResult"), "TruncationResult missing"
    assert hasattr(mod, "TruncationStrategy"), "TruncationStrategy missing"
    assert hasattr(mod, "apply_chat_template"), "apply_chat_template missing"
    assert hasattr(mod, "generate_cache_salt"), "generate_cache_salt missing"
    assert hasattr(mod, "render_prompt"), "render_prompt missing"
    assert hasattr(mod, "truncate_prompt"), "truncate_prompt missing"

