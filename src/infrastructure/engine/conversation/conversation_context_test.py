# Auto-synced test for infrastructure/engine/conversation/conversation_context.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "conversation_context.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "ContextConfig"), "ContextConfig missing"
    assert hasattr(mod, "ContextState"), "ContextState missing"
    assert hasattr(mod, "ContextSnapshot"), "ContextSnapshot missing"
    assert hasattr(mod, "TokenMetrics"), "TokenMetrics missing"
    assert hasattr(mod, "TurnType"), "TurnType missing"
    assert hasattr(mod, "ConversationTurn"), "ConversationTurn missing"
    assert hasattr(mod, "ToolExecution"), "ToolExecution missing"
    assert hasattr(mod, "ToolExecutionPolicy"), "ToolExecutionPolicy missing"
    assert hasattr(mod, "ConversationContext"), "ConversationContext missing"
    assert hasattr(mod, "AgenticContext"), "AgenticContext missing"
    assert hasattr(mod, "ContextManager"), "ContextManager missing"
    assert hasattr(mod, "get_context_manager"), "get_context_manager missing"
    assert hasattr(mod, "create_context"), "create_context missing"
    assert hasattr(mod, "merge_contexts"), "merge_contexts missing"
    assert hasattr(mod, "restore_context"), "restore_context missing"
    assert hasattr(mod, "TurnTracker"), "TurnTracker missing"
    assert hasattr(mod, "TokenTracker"), "TokenTracker missing"
    assert hasattr(mod, "ToolOrchestrator"), "ToolOrchestrator missing"
    assert hasattr(mod, "ContextOrchestrator"), "ContextOrchestrator missing"

