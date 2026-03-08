import importlib


def test_import_src_core_base_logic_managers___init__():
    mod = importlib.import_module("src.core.base.logic.managers.__init__")
    # Basic smoke tests
    assert mod is not None
