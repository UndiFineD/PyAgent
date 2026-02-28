# Auto-synced test for infrastructure/compute/backend/execution_engine.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "execution_engine.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "clear_response_cache"), "clear_response_cache missing"
    assert hasattr(mod, "get_metrics"), "get_metrics missing"
    assert hasattr(mod, "reset_metrics"), "reset_metrics missing"
    assert hasattr(mod, "validate_response_content"), "validate_response_content missing"
    assert hasattr(mod, "estimate_tokens"), "estimate_tokens missing"
    assert hasattr(mod, "estimate_cost"), "estimate_cost missing"
    assert hasattr(mod, "configure_timeout_per_backend"), "configure_timeout_per_backend missing"
    assert hasattr(mod, "llm_chat_via_github_models"), "llm_chat_via_github_models missing"
    assert hasattr(mod, "llm_chat_via_ollama"), "llm_chat_via_ollama missing"
    assert hasattr(mod, "llm_chat_via_copilot_cli"), "llm_chat_via_copilot_cli missing"
    assert hasattr(mod, "run_subagent"), "run_subagent missing"
    assert hasattr(mod, "get_backend_status"), "get_backend_status missing"
    assert hasattr(mod, "describe_backends"), "describe_backends missing"

