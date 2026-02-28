# Auto-synced test for infrastructure/compute/lora/manager/adapter.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "adapter.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "LoRAAdapter"), "LoRAAdapter missing"
    assert hasattr(mod, "load_lora_adapter"), "load_lora_adapter missing"
    assert hasattr(mod, "get_lora_info"), "get_lora_info missing"

