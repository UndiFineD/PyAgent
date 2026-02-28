# Auto-synced test for infrastructure/storage/serialization/fast_serializer.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "fast_serializer.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "SerializationFormat"), "SerializationFormat missing"
    assert hasattr(mod, "SerializerStats"), "SerializerStats missing"
    assert hasattr(mod, "Serializer"), "Serializer missing"
    assert hasattr(mod, "JSONSerializer"), "JSONSerializer missing"
    assert hasattr(mod, "PickleSerializer"), "PickleSerializer missing"
    assert hasattr(mod, "MsgPackSerializer"), "MsgPackSerializer missing"
    assert hasattr(mod, "CBORSerializer"), "CBORSerializer missing"
    assert hasattr(mod, "BinarySerializer"), "BinarySerializer missing"
    assert hasattr(mod, "SerializerRegistry"), "SerializerRegistry missing"
    assert hasattr(mod, "get_serializer_registry"), "get_serializer_registry missing"
    assert hasattr(mod, "fast_serialize"), "fast_serialize missing"
    assert hasattr(mod, "fast_deserialize"), "fast_deserialize missing"
    assert hasattr(mod, "to_json"), "to_json missing"
    assert hasattr(mod, "from_json"), "from_json missing"
    assert hasattr(mod, "to_msgpack"), "to_msgpack missing"
    assert hasattr(mod, "from_msgpack"), "from_msgpack missing"

