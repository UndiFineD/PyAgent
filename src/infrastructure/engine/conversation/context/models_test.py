# Auto-synced test for infrastructure/engine/conversation/context/models.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "models.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "ContextState"), "ContextState missing"
    assert hasattr(mod, "TurnType"), "TurnType missing"
    assert hasattr(mod, "ToolExecutionPolicy"), "ToolExecutionPolicy missing"
    assert hasattr(mod, "TokenMetrics"), "TokenMetrics missing"
    assert hasattr(mod, "ConversationTurn"), "ConversationTurn missing"
    assert hasattr(mod, "ToolExecution"), "ToolExecution missing"
    assert hasattr(mod, "ContextConfig"), "ContextConfig missing"
    assert hasattr(mod, "ContextSnapshot"), "ContextSnapshot missing"

