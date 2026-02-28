import importlib


def test_import_src_infrastructure_compute_backend___init__():
    mod = importlib.import_module("src.infrastructure.compute.backend.__init__")
    # Basic smoke tests
    assert mod is not None
