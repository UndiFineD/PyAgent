
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_volweb_py_signals_037fbf2f0cf3.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'create_auth_token'), 'missing create_auth_token'
assert hasattr(mod, 'send_evidence_created'), 'missing send_evidence_created'
assert hasattr(mod, 'send_evidence_deleted'), 'missing send_evidence_deleted'
assert hasattr(mod, 'create_task_result_on_publish'), 'missing create_task_result_on_publish'
