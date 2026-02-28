# Auto-synced test for infrastructure/engine/structured/bad_words_processor_v2.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "bad_words_processor_v2.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "BadWordsPenaltyMode"), "BadWordsPenaltyMode missing"
    assert hasattr(mod, "TrieNode"), "TrieNode missing"
    assert hasattr(mod, "BadWordsProcessorV2"), "BadWordsProcessorV2 missing"
    assert hasattr(mod, "apply_bad_words"), "apply_bad_words missing"
    assert hasattr(mod, "apply_bad_words_with_drafts"), "apply_bad_words_with_drafts missing"
    assert hasattr(mod, "BadPhrasesProcessor"), "BadPhrasesProcessor missing"

