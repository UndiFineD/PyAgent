import importlib


def test_import_src_observability_stats_core___init__():
    mod = importlib.import_module("src.observability.stats.core.__init__")
    # Basic smoke tests
    assert mod is not None
