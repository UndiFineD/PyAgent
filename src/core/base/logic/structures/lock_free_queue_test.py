# Auto-synced test for core/base/logic/structures/lock_free_queue.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "lock_free_queue.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "QueueStats"), "QueueStats missing"
    assert hasattr(mod, "MPMCQueue"), "MPMCQueue missing"
    assert hasattr(mod, "SPSCQueue"), "SPSCQueue missing"
    assert hasattr(mod, "PriorityItem"), "PriorityItem missing"
    assert hasattr(mod, "PriorityQueue"), "PriorityQueue missing"
    assert hasattr(mod, "WorkStealingDeque"), "WorkStealingDeque missing"
    assert hasattr(mod, "BatchingQueue"), "BatchingQueue missing"

