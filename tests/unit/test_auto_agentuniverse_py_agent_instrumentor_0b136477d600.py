
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agentuniverse_py_agent_instrumentor_0b136477d600.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, '_fallback'), 'missing _fallback'
assert hasattr(mod, 'safe_json_dumps'), 'missing safe_json_dumps'
assert hasattr(mod, 'QueueWrapper'), 'missing QueueWrapper'
assert hasattr(mod, 'AsyncQueueWrapper'), 'missing AsyncQueueWrapper'
assert hasattr(mod, 'AgentSpanManager'), 'missing AgentSpanManager'
assert hasattr(mod, 'AgentMetricsRecorder'), 'missing AgentMetricsRecorder'
assert hasattr(mod, 'AgentSpanAttributesSetter'), 'missing AgentSpanAttributesSetter'
assert hasattr(mod, 'AgentInstrumentor'), 'missing AgentInstrumentor'
