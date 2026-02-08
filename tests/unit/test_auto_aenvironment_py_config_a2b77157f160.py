
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\aenvironment_py_config_a2b77157f160.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'get_default_config_dir'), 'missing get_default_config_dir'
assert hasattr(mod, 'ensure_config_dir'), 'missing ensure_config_dir'
assert hasattr(mod, 'get_env_file_path'), 'missing get_env_file_path'
