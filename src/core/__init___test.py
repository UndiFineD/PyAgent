import importlib


def test_import_src_core___init__():
    mod = importlib.import_module("src.core.__init__")
    # Basic smoke tests
    assert mod is not None
