# Auto-synced test for infrastructure/compute/lora/lo_ra_manager.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "lo_ra_manager.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "LoRAMethod"), "LoRAMethod missing"
    assert hasattr(mod, "AdapterStatus"), "AdapterStatus missing"
    assert hasattr(mod, "TargetModule"), "TargetModule missing"
    assert hasattr(mod, "LoRAConfig"), "LoRAConfig missing"
    assert hasattr(mod, "LoRARequest"), "LoRARequest missing"
    assert hasattr(mod, "LoRAInfo"), "LoRAInfo missing"
    assert hasattr(mod, "AdapterSlot"), "AdapterSlot missing"
    assert hasattr(mod, "LoRAWeights"), "LoRAWeights missing"
    assert hasattr(mod, "merge_adapters"), "merge_adapters missing"
    assert hasattr(mod, "LoRAAdapter"), "LoRAAdapter missing"
    assert hasattr(mod, "load_lora_adapter"), "load_lora_adapter missing"
    assert hasattr(mod, "get_lora_info"), "get_lora_info missing"
    assert hasattr(mod, "LoRARegistry"), "LoRARegistry missing"
    assert hasattr(mod, "LoRASlotManager"), "LoRASlotManager missing"
    assert hasattr(mod, "LoRAManager"), "LoRAManager missing"

