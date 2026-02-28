# Auto-synced test for infrastructure/engine/output_processor.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "output_processor.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "EventType"), "EventType missing"
    assert hasattr(mod, "RequestEvent"), "RequestEvent missing"
    assert hasattr(mod, "LoRARequest"), "LoRARequest missing"
    assert hasattr(mod, "ParentRequest"), "ParentRequest missing"
    assert hasattr(mod, "SamplingParams"), "SamplingParams missing"
    assert hasattr(mod, "EngineCoreRequest"), "EngineCoreRequest missing"
    assert hasattr(mod, "EngineCoreOutput"), "EngineCoreOutput missing"
    assert hasattr(mod, "EngineCoreOutputs"), "EngineCoreOutputs missing"
    assert hasattr(mod, "RequestOutput"), "RequestOutput missing"
    assert hasattr(mod, "OutputProcessorOutput"), "OutputProcessorOutput missing"
    assert hasattr(mod, "RequestOutputCollector"), "RequestOutputCollector missing"
    assert hasattr(mod, "RequestState"), "RequestState missing"
    assert hasattr(mod, "LoRARequestStates"), "LoRARequestStates missing"
    assert hasattr(mod, "OutputProcessor"), "OutputProcessor missing"
    assert hasattr(mod, "IterationStats"), "IterationStats missing"

