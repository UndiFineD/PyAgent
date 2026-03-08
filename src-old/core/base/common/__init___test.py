import importlib


def test_import_src_core_base_common___init__():
    mod = importlib.import_module("src.core.base.common.__init__")
    # Basic smoke tests
    assert mod is not None
