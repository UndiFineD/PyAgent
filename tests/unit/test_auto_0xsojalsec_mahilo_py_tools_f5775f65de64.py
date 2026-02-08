
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_mahilo_py_tools_f5775f65de64.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'search_properties'), 'missing search_properties'
assert hasattr(mod, 'check_calendar'), 'missing check_calendar'
assert hasattr(mod, 'get_available_dates'), 'missing get_available_dates'
