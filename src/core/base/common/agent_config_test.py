# Auto-synced test for core/base/common/agent_config.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "agent_config.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    # register the module so dataclasses and other introspection tools
    # can look it up by name. Spec.loader.exec_module does not add it
    # automatically, which caused a failure when dataclass tried to
    # inspect cls.__module__.
    import sys
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "AgentConfig"), "AgentConfig missing"
