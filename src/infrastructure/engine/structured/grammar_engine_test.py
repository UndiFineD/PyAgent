# Auto-synced test for infrastructure/engine/structured/grammar_engine.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "grammar_engine.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "FSMState"), "FSMState missing"
    assert hasattr(mod, "FSMTransitionTable"), "FSMTransitionTable missing"
    assert hasattr(mod, "TokenMask"), "TokenMask missing"
    assert hasattr(mod, "GrammarEngine"), "GrammarEngine missing"
    assert hasattr(mod, "RegexGrammar"), "RegexGrammar missing"
    assert hasattr(mod, "JsonSchemaGrammar"), "JsonSchemaGrammar missing"
    assert hasattr(mod, "ChoiceGrammar"), "ChoiceGrammar missing"
    assert hasattr(mod, "EBNFGrammar"), "EBNFGrammar missing"

