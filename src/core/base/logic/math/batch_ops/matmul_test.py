# Auto-synced test for core/base/logic/math/batch_ops/matmul.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "matmul.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "mm_batch_invariant"), "mm_batch_invariant missing"
    assert hasattr(mod, "bmm_batch_invariant"), "bmm_batch_invariant missing"

