
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_ovo_py_sidebar_fd5eda6489ba.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'create_project_dialog'), 'missing create_project_dialog'
assert hasattr(mod, 'get_query_arg_project'), 'missing get_query_arg_project'
assert hasattr(mod, 'project_sidebar_component'), 'missing project_sidebar_component'
