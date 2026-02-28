# Auto-synced test for infrastructure/engine/attention/attention_backend_registry.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "attention_backend_registry.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "AttentionBackend"), "AttentionBackend missing"
    assert hasattr(mod, "AttentionBackendEnum"), "AttentionBackendEnum missing"
    assert hasattr(mod, "AttentionBackendRegistry"), "AttentionBackendRegistry missing"
    assert hasattr(mod, "AttentionCapabilities"), "AttentionCapabilities missing"
    assert hasattr(mod, "AttentionMetadata"), "AttentionMetadata missing"
    assert hasattr(mod, "AttentionType"), "AttentionType missing"
    assert hasattr(mod, "FlashAttentionBackend"), "FlashAttentionBackend missing"
    assert hasattr(mod, "FlashInferBackend"), "FlashInferBackend missing"
    assert hasattr(mod, "NaiveAttentionBackend"), "NaiveAttentionBackend missing"
    assert hasattr(mod, "PackKVAttentionBackend"), "PackKVAttentionBackend missing"
    assert hasattr(mod, "TorchSDPABackend"), "TorchSDPABackend missing"
    assert hasattr(mod, "get_attention_registry"), "get_attention_registry missing"

