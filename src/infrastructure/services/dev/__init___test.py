import importlib


def test_import_src_infrastructure_services_dev___init__():
    mod = importlib.import_module("src.infrastructure.services.dev.__init__")
    # Basic smoke tests
    assert mod is not None
