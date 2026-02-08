
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pytorch_lightning_py_parameter_tying_674ecd0199a4.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'find_shared_parameters'), 'missing find_shared_parameters'
assert hasattr(mod, '_find_shared_parameters'), 'missing _find_shared_parameters'
assert hasattr(mod, 'set_shared_parameters'), 'missing set_shared_parameters'
assert hasattr(mod, '_get_module_by_path'), 'missing _get_module_by_path'
assert hasattr(mod, '_set_module_by_path'), 'missing _set_module_by_path'
