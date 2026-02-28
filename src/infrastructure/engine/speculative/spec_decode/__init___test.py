import importlib


def test_import_src_infrastructure_engine_speculative_spec_decode___init__():
    mod = importlib.import_module("src.infrastructure.engine.speculative.spec_decode.__init__")
    # Basic smoke tests
    assert mod is not None
