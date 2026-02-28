# Auto-synced test for core/base/logic/agent_verification.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "agent_verification.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "AgentVerifier"), "AgentVerifier missing"
    assert hasattr(mod, "CodeHealthAuditor"), "CodeHealthAuditor missing"
    assert hasattr(mod, "CodeIntegrityVerifier"), "CodeIntegrityVerifier missing"

