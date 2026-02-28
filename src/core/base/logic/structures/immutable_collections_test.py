# Auto-synced test for core/base/logic/structures/immutable_collections.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "immutable_collections.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "ConstantList"), "ConstantList missing"
    assert hasattr(mod, "ConstantDict"), "ConstantDict missing"
    assert hasattr(mod, "FrozenDict"), "FrozenDict missing"
    assert hasattr(mod, "as_constant"), "as_constant missing"

