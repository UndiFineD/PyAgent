# Auto-synced test for logic/agents/specialists/stream_agent.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "stream_agent.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "WebhookStatus"), "WebhookStatus missing"
    assert hasattr(mod, "WebhookConfig"), "WebhookConfig missing"
    assert hasattr(mod, "StreamEvent"), "StreamEvent missing"
    assert hasattr(mod, "StreamAgent"), "StreamAgent missing"

