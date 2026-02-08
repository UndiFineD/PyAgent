
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_factorio_learning_environment_py_bounding_box_utils_6c6816bbd897.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'calculate_blueprint_bounding_box'), 'missing calculate_blueprint_bounding_box'
assert hasattr(mod, 'get_blueprint_center'), 'missing get_blueprint_center'
assert hasattr(mod, 'is_position_in_bounds'), 'missing is_position_in_bounds'
assert hasattr(mod, 'get_relative_position_description'), 'missing get_relative_position_description'
assert hasattr(mod, 'format_bounding_box_info'), 'missing format_bounding_box_info'
