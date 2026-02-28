# Auto-synced test for infrastructure/engine/scheduling/chunked_prefill/types.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "types.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "ChunkState"), "ChunkState missing"
    assert hasattr(mod, "ChunkPriority"), "ChunkPriority missing"
    assert hasattr(mod, "ChunkMetrics"), "ChunkMetrics missing"
    assert hasattr(mod, "PrefillChunk"), "PrefillChunk missing"
    assert hasattr(mod, "ChunkedRequest"), "ChunkedRequest missing"
    assert hasattr(mod, "ChunkedPrefillConfig"), "ChunkedPrefillConfig missing"

