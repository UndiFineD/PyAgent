import importlib


def test_import_src___init__():
    mod = importlib.import_module("src.__init__")
    # Basic smoke tests
    assert mod is not None
