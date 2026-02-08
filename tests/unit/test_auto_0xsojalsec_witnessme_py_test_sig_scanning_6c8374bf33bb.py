
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_witnessme_py_test_sig_scanning_6c8374bf33bb.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'sig_eng'), 'missing sig_eng'
assert hasattr(mod, 'sig_eng_l'), 'missing sig_eng_l'
assert hasattr(mod, 'test_sig_load'), 'missing test_sig_load'
assert hasattr(mod, 'test_get_sig_name'), 'missing test_get_sig_name'
assert hasattr(mod, 'test_signature_scanning'), 'missing test_signature_scanning'
