
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agent_wiz_tools.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'escalate_to_agent'), 'missing escalate_to_agent'
assert hasattr(mod, 'valid_to_change_flight'), 'missing valid_to_change_flight'
assert hasattr(mod, 'change_flight'), 'missing change_flight'
assert hasattr(mod, 'initiate_refund'), 'missing initiate_refund'
assert hasattr(mod, 'initiate_flight_credits'), 'missing initiate_flight_credits'
assert hasattr(mod, 'case_resolved'), 'missing case_resolved'
assert hasattr(mod, 'initiate_baggage_search'), 'missing initiate_baggage_search'
