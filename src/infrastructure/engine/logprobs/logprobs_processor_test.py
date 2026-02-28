# Auto-synced test for infrastructure/engine/logprobs/logprobs_processor.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "logprobs_processor.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "LogprobFormat"), "LogprobFormat missing"
    assert hasattr(mod, "TopLogprob"), "TopLogprob missing"
    assert hasattr(mod, "LogprobEntry"), "LogprobEntry missing"
    assert hasattr(mod, "PromptLogprobs"), "PromptLogprobs missing"
    assert hasattr(mod, "SampleLogprobs"), "SampleLogprobs missing"
    assert hasattr(mod, "LogprobsResult"), "LogprobsResult missing"
    assert hasattr(mod, "compute_perplexity"), "compute_perplexity missing"
    assert hasattr(mod, "compute_entropy"), "compute_entropy missing"
    assert hasattr(mod, "normalize_logprobs"), "normalize_logprobs missing"
    assert hasattr(mod, "FlatLogprobs"), "FlatLogprobs missing"
    assert hasattr(mod, "LogprobsProcessor"), "LogprobsProcessor missing"
    assert hasattr(mod, "StreamingLogprobs"), "StreamingLogprobs missing"
    assert hasattr(mod, "LogprobsAnalyzer"), "LogprobsAnalyzer missing"

