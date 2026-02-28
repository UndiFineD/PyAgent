# Auto-synced test for infrastructure/engine/logprobs/processor/config.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "config.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "LogprobFormat"), "LogprobFormat missing"
    assert hasattr(mod, "TopLogprob"), "TopLogprob missing"
    assert hasattr(mod, "LogprobEntry"), "LogprobEntry missing"
    assert hasattr(mod, "compute_perplexity"), "compute_perplexity missing"
    assert hasattr(mod, "PromptLogprobs"), "PromptLogprobs missing"
    assert hasattr(mod, "SampleLogprobs"), "SampleLogprobs missing"
    assert hasattr(mod, "LogprobsResult"), "LogprobsResult missing"

