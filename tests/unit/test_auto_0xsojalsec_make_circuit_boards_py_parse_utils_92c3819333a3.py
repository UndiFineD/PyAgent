
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_make_circuit_boards_py_parse_utils_92c3819333a3.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'get_src_info_from_token'), 'missing get_src_info_from_token'
assert hasattr(mod, 'get_src_info_from_ctx'), 'missing get_src_info_from_ctx'
