import importlib


def test_import_src_infrastructure_services_mediaio___init__():
    mod = importlib.import_module("src.infrastructure.services.mediaio.__init__")
    # Basic smoke tests
    assert mod is not None
