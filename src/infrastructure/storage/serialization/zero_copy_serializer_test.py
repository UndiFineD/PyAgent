# Auto-synced test for infrastructure/storage/serialization/zero_copy_serializer.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "zero_copy_serializer.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "ZeroCopyEncoder"), "ZeroCopyEncoder missing"
    assert hasattr(mod, "ZeroCopyDecoder"), "ZeroCopyDecoder missing"
    assert hasattr(mod, "encode_with_buffers"), "encode_with_buffers missing"
    assert hasattr(mod, "decode_with_buffers"), "decode_with_buffers missing"
    assert hasattr(mod, "MSGSPEC_AVAILABLE"), "MSGSPEC_AVAILABLE missing"

