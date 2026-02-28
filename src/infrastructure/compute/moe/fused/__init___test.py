import importlib


def test_import_src_infrastructure_compute_moe_fused___init__():
    mod = importlib.import_module("src.infrastructure.compute.moe.fused.__init__")
    # Basic smoke tests
    assert mod is not None
