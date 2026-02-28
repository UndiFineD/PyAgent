# Auto-synced test for infrastructure/compute/cuda/u_batch_processor.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "u_batch_processor.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "UBatchState"), "UBatchState missing"
    assert hasattr(mod, "UBatchSlice"), "UBatchSlice missing"
    assert hasattr(mod, "UBatchContext"), "UBatchContext missing"
    assert hasattr(mod, "UbatchMetadata"), "UbatchMetadata missing"
    assert hasattr(mod, "UBatchConfig"), "UBatchConfig missing"
    assert hasattr(mod, "UBatchBarrier"), "UBatchBarrier missing"
    assert hasattr(mod, "UBatchWrapper"), "UBatchWrapper missing"
    assert hasattr(mod, "DynamicUBatchWrapper"), "DynamicUBatchWrapper missing"
    assert hasattr(mod, "make_ubatch_contexts"), "make_ubatch_contexts missing"

