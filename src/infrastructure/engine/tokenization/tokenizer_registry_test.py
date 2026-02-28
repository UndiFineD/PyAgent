# Auto-synced test for infrastructure/engine/tokenization/tokenizer_registry.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "tokenizer_registry.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "TokenizerBackend"), "TokenizerBackend missing"
    assert hasattr(mod, "SpecialTokenHandling"), "SpecialTokenHandling missing"
    assert hasattr(mod, "TruncationStrategy"), "TruncationStrategy missing"
    assert hasattr(mod, "PaddingStrategy"), "PaddingStrategy missing"
    assert hasattr(mod, "TokenizerConfig"), "TokenizerConfig missing"
    assert hasattr(mod, "TokenizerInfo"), "TokenizerInfo missing"
    assert hasattr(mod, "TokenizeResult"), "TokenizeResult missing"
    assert hasattr(mod, "BatchTokenizeResult"), "BatchTokenizeResult missing"
    assert hasattr(mod, "TokenizerProtocol"), "TokenizerProtocol missing"
    assert hasattr(mod, "BaseTokenizer"), "BaseTokenizer missing"
    assert hasattr(mod, "HuggingFaceTokenizer"), "HuggingFaceTokenizer missing"
    assert hasattr(mod, "TiktokenTokenizer"), "TiktokenTokenizer missing"
    assert hasattr(mod, "MistralTokenizer"), "MistralTokenizer missing"
    assert hasattr(mod, "TokenizerRegistry"), "TokenizerRegistry missing"
    assert hasattr(mod, "TokenizerPool"), "TokenizerPool missing"
    assert hasattr(mod, "get_tokenizer"), "get_tokenizer missing"
    assert hasattr(mod, "create_tokenizer"), "create_tokenizer missing"
    assert hasattr(mod, "estimate_token_count"), "estimate_token_count missing"
    assert hasattr(mod, "detect_tokenizer_backend"), "detect_tokenizer_backend missing"

