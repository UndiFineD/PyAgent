import importlib


def test_import_src_infrastructure_engine_scheduling_priority___init__():
    mod = importlib.import_module("src.infrastructure.engine.scheduling.priority.__init__")
    # Basic smoke tests
    assert mod is not None
