
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_evermemos_py_annotations_bc87a4a945f4.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'ClassAnnotationKey'), 'missing ClassAnnotationKey'
assert hasattr(mod, 'Toggle'), 'missing Toggle'
