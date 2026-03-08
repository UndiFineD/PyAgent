import importlib


def test_import_src_core_base_configuration___init__():
    mod = importlib.import_module("src.core.base.configuration.__init__")
    # Basic smoke tests
    assert mod is not None
