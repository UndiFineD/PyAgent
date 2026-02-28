# Auto-synced test for infrastructure/engine/position/rotary_embedding_engine.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "rotary_embedding_engine.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "RoPEConfig"), "RoPEConfig missing"
    assert hasattr(mod, "RoPEVariant"), "RoPEVariant missing"
    assert hasattr(mod, "RoPEScalingType"), "RoPEScalingType missing"
    assert hasattr(mod, "RotaryEmbeddingBase"), "RotaryEmbeddingBase missing"
    assert hasattr(mod, "NeoxRotaryEmbedding"), "NeoxRotaryEmbedding missing"
    assert hasattr(mod, "GptJRotaryEmbedding"), "GptJRotaryEmbedding missing"
    assert hasattr(mod, "MRotaryEmbedding"), "MRotaryEmbedding missing"
    assert hasattr(mod, "XDRotaryEmbedding"), "XDRotaryEmbedding missing"
    assert hasattr(mod, "RotaryEmbeddingEngine"), "RotaryEmbeddingEngine missing"
    assert hasattr(mod, "create_rope_embedding"), "create_rope_embedding missing"

