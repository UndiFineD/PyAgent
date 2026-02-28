import importlib


def test_import_src_infrastructure_compute_cuda___init__():
    mod = importlib.import_module("src.infrastructure.compute.cuda.__init__")
    # Basic smoke tests
    assert mod is not None
