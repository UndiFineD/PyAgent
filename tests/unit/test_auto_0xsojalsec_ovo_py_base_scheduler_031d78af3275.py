
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_ovo_py_base_scheduler_031d78af3275.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'SchedulerTypes'), 'missing SchedulerTypes'
assert hasattr(mod, 'JobNotFound'), 'missing JobNotFound'
assert hasattr(mod, 'Scheduler'), 'missing Scheduler'
