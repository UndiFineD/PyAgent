# Auto-synced test for core/base/logic/structures/flat_logprobs.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "flat_logprobs.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "Logprob"), "Logprob missing"
    assert hasattr(mod, "FlatLogprobs"), "FlatLogprobs missing"
    assert hasattr(mod, "create_prompt_logprobs"), "create_prompt_logprobs missing"
    assert hasattr(mod, "create_sample_logprobs"), "create_sample_logprobs missing"
    assert hasattr(mod, "LogprobsAccumulator"), "LogprobsAccumulator missing"

