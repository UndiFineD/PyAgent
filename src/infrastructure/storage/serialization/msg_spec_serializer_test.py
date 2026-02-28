# Auto-synced test for infrastructure/storage/serialization/msg_spec_serializer.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "msg_spec_serializer.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "is_msgspec_available"), "is_msgspec_available missing"
    assert hasattr(mod, "require_msgspec"), "require_msgspec missing"
    assert hasattr(mod, "JSONEncoder"), "JSONEncoder missing"
    assert hasattr(mod, "MsgPackEncoder"), "MsgPackEncoder missing"
    assert hasattr(mod, "TypedSerializer"), "TypedSerializer missing"
    assert hasattr(mod, "encode_chat_request"), "encode_chat_request missing"
    assert hasattr(mod, "decode_chat_response"), "decode_chat_response missing"
    assert hasattr(mod, "decode_stream_chunk"), "decode_stream_chunk missing"
    assert hasattr(mod, "BenchmarkResult"), "BenchmarkResult missing"
    assert hasattr(mod, "benchmark_serialization"), "benchmark_serialization missing"
    assert hasattr(mod, "MSGSPEC_AVAILABLE"), "MSGSPEC_AVAILABLE missing"

