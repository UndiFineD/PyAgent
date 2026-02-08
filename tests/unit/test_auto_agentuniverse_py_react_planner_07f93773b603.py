
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agentuniverse_py_react_planner_07f93773b603.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'ReActPlanner'), 'missing ReActPlanner'
assert hasattr(mod, 'create_react_agent'), 'missing create_react_agent'
