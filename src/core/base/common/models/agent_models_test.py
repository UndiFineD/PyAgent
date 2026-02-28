# Auto-synced test for core/base/common/models/agent_models.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "agent_models.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "AgentConfig"), "AgentConfig missing"
    assert hasattr(mod, "ComposedAgent"), "ComposedAgent missing"
    assert hasattr(mod, "AgentHealthCheck"), "AgentHealthCheck missing"
    assert hasattr(mod, "AgentPluginConfig"), "AgentPluginConfig missing"
    assert hasattr(mod, "ExecutionProfile"), "ExecutionProfile missing"
    assert hasattr(mod, "AgentPipeline"), "AgentPipeline missing"
    assert hasattr(mod, "AgentParallel"), "AgentParallel missing"
    assert hasattr(mod, "AgentRouter"), "AgentRouter missing"

