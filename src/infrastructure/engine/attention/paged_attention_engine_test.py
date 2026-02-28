# Auto-synced test for infrastructure/engine/attention/paged_attention_engine.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "paged_attention_engine.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "AttentionConfig"), "AttentionConfig missing"
    assert hasattr(mod, "AttentionMetadata"), "AttentionMetadata missing"
    assert hasattr(mod, "AttentionType"), "AttentionType missing"
    assert hasattr(mod, "BlockTable"), "BlockTable missing"
    assert hasattr(mod, "KVCacheDtype"), "KVCacheDtype missing"
    assert hasattr(mod, "PagedAttentionEngine"), "PagedAttentionEngine missing"
    assert hasattr(mod, "PagedAttentionOps"), "PagedAttentionOps missing"
    assert hasattr(mod, "PagedKVCache"), "PagedKVCache missing"
    assert hasattr(mod, "SlotMapping"), "SlotMapping missing"
    assert hasattr(mod, "create_attention_engine"), "create_attention_engine missing"

