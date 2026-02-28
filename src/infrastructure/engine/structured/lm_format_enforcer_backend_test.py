# Auto-synced test for infrastructure/engine/structured/lm_format_enforcer_backend.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "lm_format_enforcer_backend.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "DFAStateType"), "DFAStateType missing"
    assert hasattr(mod, "DFAState"), "DFAState missing"
    assert hasattr(mod, "DFATransition"), "DFATransition missing"
    assert hasattr(mod, "CompiledDFA"), "CompiledDFA missing"
    assert hasattr(mod, "TokenVocabulary"), "TokenVocabulary missing"
    assert hasattr(mod, "RegexMatchState"), "RegexMatchState missing"
    assert hasattr(mod, "CompiledEnforcer"), "CompiledEnforcer missing"
    assert hasattr(mod, "LMFormatEnforcerBackend"), "LMFormatEnforcerBackend missing"
    assert hasattr(mod, "AsyncLMFormatEnforcerBackend"), "AsyncLMFormatEnforcerBackend missing"
    assert hasattr(mod, "FormatEnforcerGrammar"), "FormatEnforcerGrammar missing"
    assert hasattr(mod, "CompositeEnforcer"), "CompositeEnforcer missing"

