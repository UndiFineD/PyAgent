# Auto-synced test for infrastructure/swarm/fleet/mixins/fleet_update_mixin.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "fleet_update_mixin.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "FleetUpdateMixin"), "FleetUpdateMixin missing"

