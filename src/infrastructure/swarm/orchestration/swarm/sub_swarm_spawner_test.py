# Auto-synced test for infrastructure/swarm/orchestration/swarm/sub_swarm_spawner.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "sub_swarm_spawner.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "SubSwarm"), "SubSwarm missing"
    assert hasattr(mod, "SubSwarmSpawner"), "SubSwarmSpawner missing"

