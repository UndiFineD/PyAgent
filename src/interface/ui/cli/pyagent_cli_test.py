# Auto-synced test for interface/ui/cli/pyagent_cli.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "pyagent_cli.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "check_server"), "check_server missing"
    assert hasattr(mod, "list_agents"), "list_agents missing"
    assert hasattr(mod, "run_task"), "run_task missing"
    assert hasattr(mod, "main"), "main missing"

