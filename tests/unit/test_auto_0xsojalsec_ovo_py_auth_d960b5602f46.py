
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_ovo_py_auth_d960b5602f46.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'is_running_in_streamlit'), 'missing is_running_in_streamlit'
assert hasattr(mod, 'get_posit_user_info'), 'missing get_posit_user_info'
assert hasattr(mod, 'get_username'), 'missing get_username'
