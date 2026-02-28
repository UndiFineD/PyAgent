# Auto-synced test for infrastructure/engine/sampling/sampling_engine.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "sampling_engine.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "SamplingParams"), "SamplingParams missing"
    assert hasattr(mod, "SamplingState"), "SamplingState missing"
    assert hasattr(mod, "Sampler"), "Sampler missing"
    assert hasattr(mod, "HAS_RUST"), "HAS_RUST missing"
    assert hasattr(mod, "TemperatureSampler"), "TemperatureSampler missing"
    assert hasattr(mod, "TopKSampler"), "TopKSampler missing"
    assert hasattr(mod, "TopPSampler"), "TopPSampler missing"
    assert hasattr(mod, "TopKTopPSampler"), "TopKTopPSampler missing"
    assert hasattr(mod, "GumbelSampler"), "GumbelSampler missing"
    assert hasattr(mod, "RepetitionPenaltySampler"), "RepetitionPenaltySampler missing"
    assert hasattr(mod, "PenaltySampler"), "PenaltySampler missing"
    assert hasattr(mod, "BeamSearchConfig"), "BeamSearchConfig missing"
    assert hasattr(mod, "BeamHypothesis"), "BeamHypothesis missing"
    assert hasattr(mod, "BeamSearchSampler"), "BeamSearchSampler missing"
    assert hasattr(mod, "SamplingEngine"), "SamplingEngine missing"
    assert hasattr(mod, "SamplingPipeline"), "SamplingPipeline missing"
    assert hasattr(mod, "sample_logits"), "sample_logits missing"
    assert hasattr(mod, "create_sampling_engine"), "create_sampling_engine missing"

