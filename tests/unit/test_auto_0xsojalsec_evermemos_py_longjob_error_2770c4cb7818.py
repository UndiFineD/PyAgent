
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_evermemos_py_longjob_error_2770c4cb7818.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'FatalError'), 'missing FatalError'
assert hasattr(mod, 'BusinessLogicError'), 'missing BusinessLogicError'
assert hasattr(mod, 'LongJobError'), 'missing LongJobError'
assert hasattr(mod, 'JobNotFoundError'), 'missing JobNotFoundError'
assert hasattr(mod, 'JobAlreadyExistsError'), 'missing JobAlreadyExistsError'
assert hasattr(mod, 'JobStateError'), 'missing JobStateError'
assert hasattr(mod, 'ManagerShutdownError'), 'missing ManagerShutdownError'
assert hasattr(mod, 'MaxConcurrentJobsError'), 'missing MaxConcurrentJobsError'
