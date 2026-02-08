
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_evermemos_py_base_memcell_extractor_e8e22f134117.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'MemCellExtractRequest'), 'missing MemCellExtractRequest'
assert hasattr(mod, 'StatusResult'), 'missing StatusResult'
assert hasattr(mod, 'MemCellExtractor'), 'missing MemCellExtractor'
