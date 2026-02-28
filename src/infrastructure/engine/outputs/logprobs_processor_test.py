# Auto-synced test for infrastructure/engine/outputs/logprobs_processor.py
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
    assert hasattr(mod, "TokenLogprob"), "TokenLogprob missing"
    assert hasattr(mod, "TopLogprobs"), "TopLogprobs missing"
    assert hasattr(mod, "LogprobsLists"), "LogprobsLists missing"
    assert hasattr(mod, "LogprobsTensors"), "LogprobsTensors missing"
    assert hasattr(mod, "AsyncCPUTransfer"), "AsyncCPUTransfer missing"
    assert hasattr(mod, "SamplerOutput"), "SamplerOutput missing"
    assert hasattr(mod, "ModelRunnerOutput"), "ModelRunnerOutput missing"
    assert hasattr(mod, "StreamingLogprobsCollector"), "StreamingLogprobsCollector missing"
    assert hasattr(mod, "extract_top_k_logprobs_rust"), "extract_top_k_logprobs_rust missing"
    assert hasattr(mod, "batch_logprobs_to_cpu_rust"), "batch_logprobs_to_cpu_rust missing"

