import importlib


def test_import_src_infrastructure_services_dev_generated___init__():
    mod = importlib.import_module("src.infrastructure.services.dev.generated.__init__")
    # Basic smoke tests
    assert mod is not None
