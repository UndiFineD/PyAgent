
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xSojalSec_h2o_llmstudio_exceptions.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'LLMDataException'), 'missing LLMDataException'
assert hasattr(mod, 'LLMModelException'), 'missing LLMModelException'
assert hasattr(mod, 'LLMAugmentationsException'), 'missing LLMAugmentationsException'
assert hasattr(mod, 'LLMMetricException'), 'missing LLMMetricException'
assert hasattr(mod, 'LLMTrainingException'), 'missing LLMTrainingException'
assert hasattr(mod, 'LLMResourceException'), 'missing LLMResourceException'
