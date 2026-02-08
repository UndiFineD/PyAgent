
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_volweb_py_serializers_b64a39fbc51c.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'UserSerializer'), 'missing UserSerializer'
assert hasattr(mod, 'CaseSerializer'), 'missing CaseSerializer'
assert hasattr(mod, 'send_case_created'), 'missing send_case_created'
assert hasattr(mod, 'send_case_deleted'), 'missing send_case_deleted'
