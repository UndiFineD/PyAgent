
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pdfalyzer_py_dict_helper_bf50355b1ca4.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'get_dict_key_by_value'), 'missing get_dict_key_by_value'
assert hasattr(mod, 'merge'), 'missing merge'
