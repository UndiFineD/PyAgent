# Auto-synced test for infrastructure/engine/prompt_renderer/models.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "models.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "TruncationStrategy"), "TruncationStrategy missing"
    assert hasattr(mod, "InputType"), "InputType missing"
    assert hasattr(mod, "RenderMode"), "RenderMode missing"
    assert hasattr(mod, "PromptConfig"), "PromptConfig missing"
    assert hasattr(mod, "TruncationResult"), "TruncationResult missing"
    assert hasattr(mod, "RenderResult"), "RenderResult missing"
    assert hasattr(mod, "EmbeddingInput"), "EmbeddingInput missing"
    assert hasattr(mod, "MultimodalInput"), "MultimodalInput missing"

