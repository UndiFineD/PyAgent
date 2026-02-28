# Auto-synced test for core/base/logic/math/batch_invariant_ops.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "batch_invariant_ops.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "matmul_persistent"), "matmul_persistent missing"
    assert hasattr(mod, "softmax_batch_invariant"), "softmax_batch_invariant missing"
    assert hasattr(mod, "log_softmax_batch_invariant"), "log_softmax_batch_invariant missing"
    assert hasattr(mod, "mean_batch_invariant"), "mean_batch_invariant missing"
    assert hasattr(mod, "mm_batch_invariant"), "mm_batch_invariant missing"
    assert hasattr(mod, "bmm_batch_invariant"), "bmm_batch_invariant missing"
    assert hasattr(mod, "addmm_batch_invariant"), "addmm_batch_invariant missing"
    assert hasattr(mod, "gelu_batch_invariant"), "gelu_batch_invariant missing"
    assert hasattr(mod, "layer_norm_batch_invariant"), "layer_norm_batch_invariant missing"
    assert hasattr(mod, "rms_norm_batch_invariant"), "rms_norm_batch_invariant missing"
    assert hasattr(mod, "attention_score_batch_invariant"), "attention_score_batch_invariant missing"
    assert hasattr(mod, "attention_output_batch_invariant"), "attention_output_batch_invariant missing"
    assert hasattr(mod, "BatchInvariantOps"), "BatchInvariantOps missing"

