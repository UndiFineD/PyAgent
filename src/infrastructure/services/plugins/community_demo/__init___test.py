import importlib


def test_import_src_infrastructure_services_plugins_community_demo___init__():
    mod = importlib.import_module("src.infrastructure.services.plugins.community_demo.__init__")
    # Basic smoke tests
    assert mod is not None
