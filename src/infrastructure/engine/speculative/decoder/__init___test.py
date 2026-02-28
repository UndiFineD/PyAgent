import importlib


def test_import_src_infrastructure_engine_speculative_decoder___init__():
    mod = importlib.import_module("src.infrastructure.engine.speculative.decoder.__init__")
    # Basic smoke tests
    assert mod is not None
