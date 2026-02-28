import importlib


def test_import_src_infrastructure_engine_sampling_ngram___init__():
    mod = importlib.import_module("src.infrastructure.engine.sampling.ngram.__init__")
    # Basic smoke tests
    assert mod is not None
