
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_volweb_py_initadmin_74b7211687df.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'createSuperUser'), 'missing createSuperUser'
assert hasattr(mod, 'createSimpleUser'), 'missing createSimpleUser'
assert hasattr(mod, 'Command'), 'missing Command'
