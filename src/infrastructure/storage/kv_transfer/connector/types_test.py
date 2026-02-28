# Auto-synced test for infrastructure/storage/kv_transfer/connector/types.py
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
    assert hasattr(mod, "KVConnectorRole"), "KVConnectorRole missing"
    assert hasattr(mod, "KVTransferMode"), "KVTransferMode missing"
    assert hasattr(mod, "KVTransferConfig"), "KVTransferConfig missing"
    assert hasattr(mod, "KVConnectorMetadata"), "KVConnectorMetadata missing"
    assert hasattr(mod, "KVCacheBlocks"), "KVCacheBlocks missing"
    assert hasattr(mod, "ForwardContext"), "ForwardContext missing"
    assert hasattr(mod, "Request"), "Request missing"

