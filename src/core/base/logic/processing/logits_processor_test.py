# Auto-synced test for core/base/logic/processing/logits_processor.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "logits_processor.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "LogitsProcessor"), "LogitsProcessor missing"
    assert hasattr(mod, "LogitsProcessorList"), "LogitsProcessorList missing"
    assert hasattr(mod, "TemperatureProcessor"), "TemperatureProcessor missing"
    assert hasattr(mod, "TopKProcessor"), "TopKProcessor missing"
    assert hasattr(mod, "TopPProcessor"), "TopPProcessor missing"
    assert hasattr(mod, "RepetitionPenaltyProcessor"), "RepetitionPenaltyProcessor missing"
    assert hasattr(mod, "NoBadWordsProcessor"), "NoBadWordsProcessor missing"
    assert hasattr(mod, "MinLengthProcessor"), "MinLengthProcessor missing"
    assert hasattr(mod, "apply_processors"), "apply_processors missing"
    assert hasattr(mod, "MaxLengthProcessor"), "MaxLengthProcessor missing"
    assert hasattr(mod, "PresencePenaltyProcessor"), "PresencePenaltyProcessor missing"
    assert hasattr(mod, "FrequencyPenaltyProcessor"), "FrequencyPenaltyProcessor missing"
    assert hasattr(mod, "create_processor_chain"), "create_processor_chain missing"

