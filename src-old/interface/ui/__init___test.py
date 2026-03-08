import importlib


def test_import_src_interface_ui___init__():
    mod = importlib.import_module("src.interface.ui.__init__")
    # Basic smoke tests
    assert mod is not None
