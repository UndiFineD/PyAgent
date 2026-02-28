import importlib


def test_import_src_core_knowledge___init__():
    mod = importlib.import_module("src.core.knowledge.__init__")
    # Basic smoke tests
    assert mod is not None
