
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\aenvironment_py_custom_env_169287412a28.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'get_weather'), 'missing get_weather'
assert hasattr(mod, 'get_weather_func'), 'missing get_weather_func'
assert hasattr(mod, 'is_good_weather'), 'missing is_good_weather'
