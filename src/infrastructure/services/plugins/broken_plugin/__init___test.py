import importlib


def test_import_src_infrastructure_services_plugins_broken_plugin___init__():
    mod = importlib.import_module("src.infrastructure.services.plugins.broken_plugin.__init__")
    # Basic smoke tests
    assert mod is not None
