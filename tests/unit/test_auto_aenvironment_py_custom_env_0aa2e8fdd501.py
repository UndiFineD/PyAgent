
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\aenvironment_py_custom_env_0aa2e8fdd501.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'my_custom_echo_env'), 'missing my_custom_echo_env'
assert hasattr(mod, 'my_custom_reward'), 'missing my_custom_reward'
