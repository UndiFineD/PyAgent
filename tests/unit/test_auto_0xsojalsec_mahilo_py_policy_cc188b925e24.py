
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_mahilo_py_policy_cc188b925e24.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'PolicyType'), 'missing PolicyType'
assert hasattr(mod, 'PolicyViolation'), 'missing PolicyViolation'
assert hasattr(mod, 'Policy'), 'missing Policy'
assert hasattr(mod, 'PolicyManager'), 'missing PolicyManager'
assert hasattr(mod, 'MessageValidator'), 'missing MessageValidator'
assert hasattr(mod, 'create_default_policies'), 'missing create_default_policies'
