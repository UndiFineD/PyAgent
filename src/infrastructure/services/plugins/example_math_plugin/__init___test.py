import importlib


def test_import_src_infrastructure_services_plugins_example_math_plugin___init__():
    mod = importlib.import_module("src.infrastructure.services.plugins.example_math_plugin.__init__")
    # Basic smoke tests
    assert mod is not None
