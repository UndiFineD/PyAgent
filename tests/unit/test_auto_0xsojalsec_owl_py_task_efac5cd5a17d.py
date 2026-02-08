
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_owl_py_task_efac5cd5a17d.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'parse_response'), 'missing parse_response'
assert hasattr(mod, 'TaskState'), 'missing TaskState'
assert hasattr(mod, 'Task'), 'missing Task'
assert hasattr(mod, 'TaskManager'), 'missing TaskManager'
