# Auto-synced test for infrastructure/engine/adapters/lo_ra_manager.py
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
    assert hasattr(mod, "LoRATarget"), "LoRATarget missing"
    assert hasattr(mod, "LoRAConfig"), "LoRAConfig missing"
    assert hasattr(mod, "LoRAModelState"), "LoRAModelState missing"
    assert hasattr(mod, "LoRALayerWeights"), "LoRALayerWeights missing"
    assert hasattr(mod, "PackedLoRAWeights"), "PackedLoRAWeights missing"
    assert hasattr(mod, "LoRAModel"), "LoRAModel missing"
    assert hasattr(mod, "LoRAModelEntry"), "LoRAModelEntry missing"
    assert hasattr(mod, "LoRARegistry"), "LoRARegistry missing"
    assert hasattr(mod, "LoRAManager"), "LoRAManager missing"
    assert hasattr(mod, "create_lora_weights"), "create_lora_weights missing"
    assert hasattr(mod, "create_lora_model"), "create_lora_model missing"
    assert hasattr(mod, "merge_lora_weights"), "merge_lora_weights missing"
    assert hasattr(mod, "compute_effective_rank"), "compute_effective_rank missing"

