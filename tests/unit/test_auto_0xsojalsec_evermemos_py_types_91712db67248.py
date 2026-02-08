
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_evermemos_py_types_91712db67248.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'ProjectInfo'), 'missing ProjectInfo'
assert hasattr(mod, 'ImportanceEvidence'), 'missing ImportanceEvidence'
assert hasattr(mod, 'GroupImportanceEvidence'), 'missing GroupImportanceEvidence'
assert hasattr(mod, 'ProfileMemory'), 'missing ProfileMemory'
assert hasattr(mod, 'ProfileMemoryExtractRequest'), 'missing ProfileMemoryExtractRequest'
