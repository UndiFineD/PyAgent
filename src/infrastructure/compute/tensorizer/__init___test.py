import importlib


def test_import_src_infrastructure_compute_tensorizer___init__():
    mod = importlib.import_module("src.infrastructure.compute.tensorizer.__init__")
    # Basic smoke tests
    assert mod is not None
