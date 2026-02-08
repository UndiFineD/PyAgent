
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_factorio_learning_environment_py_position_utils_e21248aa0124.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'format_position'), 'missing format_position'
assert hasattr(mod, 'format_position_from_dict'), 'missing format_position_from_dict'
assert hasattr(mod, 'convert_coordinate_format_in_text'), 'missing convert_coordinate_format_in_text'
assert hasattr(mod, 'extract_position_from_text'), 'missing extract_position_from_text'
assert hasattr(mod, 'normalize_position_references_in_qa'), 'missing normalize_position_references_in_qa'
