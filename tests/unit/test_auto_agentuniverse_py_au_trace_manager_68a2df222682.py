
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agentuniverse_py_au_trace_manager_68a2df222682.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'AuTraceManager'), 'missing AuTraceManager'
assert hasattr(mod, 'get_trace_dict'), 'missing get_trace_dict'
assert hasattr(mod, 'set_session_id'), 'missing set_session_id'
assert hasattr(mod, 'get_session_id'), 'missing get_session_id'
assert hasattr(mod, 'set_trace_id'), 'missing set_trace_id'
assert hasattr(mod, 'get_trace_id'), 'missing get_trace_id'
assert hasattr(mod, 'set_span_id'), 'missing set_span_id'
assert hasattr(mod, 'get_span_id'), 'missing get_span_id'
assert hasattr(mod, 'init_new_token_usage'), 'missing init_new_token_usage'
assert hasattr(mod, 'add_current_token_usage'), 'missing add_current_token_usage'
assert hasattr(mod, 'add_current_token_usage_to_parent'), 'missing add_current_token_usage_to_parent'
assert hasattr(mod, 'get_current_token_usage'), 'missing get_current_token_usage'
