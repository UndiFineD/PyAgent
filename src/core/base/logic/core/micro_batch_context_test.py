# Auto-synced test for core/base/logic/core/micro_batch_context.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "micro_batch_context.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "StreamType"), "StreamType missing"
    assert hasattr(mod, "MicroBatchState"), "MicroBatchState missing"
    assert hasattr(mod, "StreamHandle"), "StreamHandle missing"
    assert hasattr(mod, "MicroBatchInfo"), "MicroBatchInfo missing"
    assert hasattr(mod, "StreamManager"), "StreamManager missing"
    assert hasattr(mod, "MicroBatchContext"), "MicroBatchContext missing"
    assert hasattr(mod, "AdaptiveMicroBatchContext"), "AdaptiveMicroBatchContext missing"
    assert hasattr(mod, "create_micro_batch_context"), "create_micro_batch_context missing"
    assert hasattr(mod, "micro_batch_scope"), "micro_batch_scope missing"

