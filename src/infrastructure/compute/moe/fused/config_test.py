# Auto-synced test for infrastructure/compute/moe/fused/config.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "config.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "ExpertPlacementStrategy"), "ExpertPlacementStrategy missing"
    assert hasattr(mod, "MoEQuantMethod"), "MoEQuantMethod missing"
    assert hasattr(mod, "FusedMoEConfig"), "FusedMoEConfig missing"
    assert hasattr(mod, "FusedMoEParallelConfig"), "FusedMoEParallelConfig missing"
    assert hasattr(mod, "FusedMoEQuantConfig"), "FusedMoEQuantConfig missing"

