import importlib


def test_import_src_infrastructure_services_cloud_providers___init__():
    mod = importlib.import_module("src.infrastructure.services.cloud.providers.__init__")
    # Basic smoke tests
    assert mod is not None
