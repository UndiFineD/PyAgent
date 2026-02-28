# Auto-synced test for infrastructure/engine/structured/logits_processor_v2.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "logits_processor_v2.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "MoveDirectionality"), "MoveDirectionality missing"
    assert hasattr(mod, "SamplingParams"), "SamplingParams missing"
    assert hasattr(mod, "BatchUpdate"), "BatchUpdate missing"
    assert hasattr(mod, "BatchUpdateBuilder"), "BatchUpdateBuilder missing"
    assert hasattr(mod, "LogitsProcessor"), "LogitsProcessor missing"
    assert hasattr(mod, "MinPLogitsProcessor"), "MinPLogitsProcessor missing"
    assert hasattr(mod, "LogitBiasLogitsProcessor"), "LogitBiasLogitsProcessor missing"
    assert hasattr(mod, "CompositeLogitsProcessor"), "CompositeLogitsProcessor missing"
    assert hasattr(mod, "LogitsProcessorRegistry"), "LogitsProcessorRegistry missing"

