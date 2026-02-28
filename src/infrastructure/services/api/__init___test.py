import importlib


def test_import_src_infrastructure_services_api___init__():
    mod = importlib.import_module("src.infrastructure.services.api.__init__")
    # Basic smoke tests
    assert mod is not None
