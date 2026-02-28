# Auto-synced test for infrastructure/compute/backend/vllm_advanced/lora_manager.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "lora_manager.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "AdapterState"), "AdapterState missing"
    assert hasattr(mod, "LoraConfig"), "LoraConfig missing"
    assert hasattr(mod, "LoraAdapter"), "LoraAdapter missing"
    assert hasattr(mod, "HAS_LORA"), "HAS_LORA missing"
    assert hasattr(mod, "LoraRegistry"), "LoraRegistry missing"
    assert hasattr(mod, "LoraManager"), "LoraManager missing"
    assert hasattr(mod, "create_lora_request"), "create_lora_request missing"
    assert hasattr(mod, "discover_adapters"), "discover_adapters missing"

