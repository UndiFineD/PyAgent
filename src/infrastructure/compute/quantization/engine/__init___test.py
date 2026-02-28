import importlib


def test_import_src_infrastructure_compute_quantization_engine___init__():
    mod = importlib.import_module("src.infrastructure.compute.quantization.engine.__init__")
    # Basic smoke tests
    assert mod is not None
