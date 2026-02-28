# Auto-synced test for infrastructure/engine/structured/logit_processor.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "logit_processor.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "LogitBias"), "LogitBias missing"
    assert hasattr(mod, "ProcessorStats"), "ProcessorStats missing"
    assert hasattr(mod, "LogitProcessor"), "LogitProcessor missing"
    assert hasattr(mod, "ConstrainedLogitProcessor"), "ConstrainedLogitProcessor missing"
    assert hasattr(mod, "BitmaskLogitProcessor"), "BitmaskLogitProcessor missing"
    assert hasattr(mod, "BiasLogitProcessor"), "BiasLogitProcessor missing"
    assert hasattr(mod, "CompositeLogitProcessor"), "CompositeLogitProcessor missing"
    assert hasattr(mod, "TemperatureProcessor"), "TemperatureProcessor missing"
    assert hasattr(mod, "TopKProcessor"), "TopKProcessor missing"
    assert hasattr(mod, "TopPProcessor"), "TopPProcessor missing"
    assert hasattr(mod, "RepetitionPenaltyProcessor"), "RepetitionPenaltyProcessor missing"
    assert hasattr(mod, "create_standard_processor_chain"), "create_standard_processor_chain missing"
    assert hasattr(mod, "apply_constraints_to_logits"), "apply_constraints_to_logits missing"

