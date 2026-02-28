# Auto-synced test for infrastructure/compute/moe/fused_mo_e_layer.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "fused_mo_e_layer.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "FusedMoEConfig"), "FusedMoEConfig missing"
    assert hasattr(mod, "FusedMoEParallelConfig"), "FusedMoEParallelConfig missing"
    assert hasattr(mod, "FusedMoEQuantConfig"), "FusedMoEQuantConfig missing"
    assert hasattr(mod, "ExpertPlacementStrategy"), "ExpertPlacementStrategy missing"
    assert hasattr(mod, "FusedMoEMethodBase"), "FusedMoEMethodBase missing"
    assert hasattr(mod, "UnquantizedFusedMoEMethod"), "UnquantizedFusedMoEMethod missing"
    assert hasattr(mod, "SparseDispatcher"), "SparseDispatcher missing"
    assert hasattr(mod, "DenseDispatcher"), "DenseDispatcher missing"
    assert hasattr(mod, "determine_expert_map"), "determine_expert_map missing"
    assert hasattr(mod, "FusedMoELayer"), "FusedMoELayer missing"
    assert hasattr(mod, "AdaptiveMoELayer"), "AdaptiveMoELayer missing"
    assert hasattr(mod, "HierarchicalMoELayer"), "HierarchicalMoELayer missing"

