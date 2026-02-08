
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agentuniverse_py_tool_instrumentor_f0d13d7b0f09.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, '_fallback'), 'missing _fallback'
assert hasattr(mod, 'safe_json_dumps'), 'missing safe_json_dumps'
assert hasattr(mod, 'ToolSpanManager'), 'missing ToolSpanManager'
assert hasattr(mod, 'ToolMetricsRecorder'), 'missing ToolMetricsRecorder'
assert hasattr(mod, 'ToolSpanAttributesSetter'), 'missing ToolSpanAttributesSetter'
assert hasattr(mod, 'ToolInstrumentor'), 'missing ToolInstrumentor'
