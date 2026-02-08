
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agentuniverse_py_llm_instrumentor_9abc5a859e51.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, '_fallback'), 'missing _fallback'
assert hasattr(mod, 'safe_json_dumps'), 'missing safe_json_dumps'
assert hasattr(mod, 'LLMSpanManager'), 'missing LLMSpanManager'
assert hasattr(mod, 'LLMMetricsRecorder'), 'missing LLMMetricsRecorder'
assert hasattr(mod, 'LLMSpanAttributesSetter'), 'missing LLMSpanAttributesSetter'
assert hasattr(mod, 'StreamingResultProcessor'), 'missing StreamingResultProcessor'
assert hasattr(mod, 'LLMInstrumentor'), 'missing LLMInstrumentor'
