
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_evermemos_py_doc_base_971b79cb2c07.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'DocBase'), 'missing DocBase'
assert hasattr(mod, 'AliasSupportDoc'), 'missing AliasSupportDoc'
assert hasattr(mod, 'AliasDoc'), 'missing AliasDoc'
