# Auto-synced test for infrastructure/engine/parallel_sampling.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "parallel_sampling.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "SamplingStrategy"), "SamplingStrategy missing"
    assert hasattr(mod, "OutputKind"), "OutputKind missing"
    assert hasattr(mod, "SamplingParams"), "SamplingParams missing"
    assert hasattr(mod, "CompletionOutput"), "CompletionOutput missing"
    assert hasattr(mod, "ParentRequest"), "ParentRequest missing"
    assert hasattr(mod, "ParallelSamplingManager"), "ParallelSamplingManager missing"
    assert hasattr(mod, "BeamState"), "BeamState missing"
    assert hasattr(mod, "BeamSearchManager"), "BeamSearchManager missing"
    assert hasattr(mod, "DiverseSamplingManager"), "DiverseSamplingManager missing"
    assert hasattr(mod, "BestOfNFilter"), "BestOfNFilter missing"
    assert hasattr(mod, "IterationStats"), "IterationStats missing"

