# Auto-synced test for core/rl/action_space.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "action_space.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "ActionMetadata"), "ActionMetadata missing"
    assert hasattr(mod, "ActionSpace"), "ActionSpace missing"
    assert hasattr(mod, "DiscreteActionSpace"), "DiscreteActionSpace missing"
    assert hasattr(mod, "BoxActionSpace"), "BoxActionSpace missing"
    assert hasattr(mod, "MultiDiscreteActionSpace"), "MultiDiscreteActionSpace missing"
    assert hasattr(mod, "DictActionSpace"), "DictActionSpace missing"

