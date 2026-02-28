# Auto-synced test for infrastructure/engine/adapters/lora/utils.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "utils.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "create_lora_weights"), "create_lora_weights missing"
    assert hasattr(mod, "create_lora_model"), "create_lora_model missing"
    assert hasattr(mod, "merge_lora_weights"), "merge_lora_weights missing"
    assert hasattr(mod, "compute_effective_rank"), "compute_effective_rank missing"

