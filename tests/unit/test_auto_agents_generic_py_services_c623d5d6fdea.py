
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agents_generic_py_services_c623d5d6fdea.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'LLM'), 'missing LLM'
assert hasattr(mod, 'STT'), 'missing STT'
assert hasattr(mod, '_get_api_key'), 'missing _get_api_key'
