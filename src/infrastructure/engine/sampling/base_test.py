# Auto-synced test for infrastructure/engine/sampling/base.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "base.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "Sampler"), "Sampler missing"
    assert hasattr(mod, "HAS_RUST"), "HAS_RUST missing"
    assert hasattr(mod, "top_k_mask_rust"), "top_k_mask_rust missing"
    assert hasattr(mod, "top_p_mask_rust"), "top_p_mask_rust missing"
    assert hasattr(mod, "gumbel_sample_rust"), "gumbel_sample_rust missing"
    assert hasattr(mod, "beam_score_rust"), "beam_score_rust missing"
    assert hasattr(mod, "compute_penalties_rust"), "compute_penalties_rust missing"

