# Auto-synced test for infrastructure/compute/moe/expert_router.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "expert_router.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "RoutingMethod"), "RoutingMethod missing"
    assert hasattr(mod, "RouterConfig"), "RouterConfig missing"
    assert hasattr(mod, "RouterOutput"), "RouterOutput missing"
    assert hasattr(mod, "RouterBase"), "RouterBase missing"
    assert hasattr(mod, "TopKRouter"), "TopKRouter missing"
    assert hasattr(mod, "GroupedTopKRouter"), "GroupedTopKRouter missing"
    assert hasattr(mod, "ExpertChoiceRouter"), "ExpertChoiceRouter missing"
    assert hasattr(mod, "SoftMoERouter"), "SoftMoERouter missing"
    assert hasattr(mod, "AdaptiveRouter"), "AdaptiveRouter missing"
    assert hasattr(mod, "RoutingSimulator"), "RoutingSimulator missing"

