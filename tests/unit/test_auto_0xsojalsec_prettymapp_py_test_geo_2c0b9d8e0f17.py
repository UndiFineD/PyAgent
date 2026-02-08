
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_prettymapp_py_test_geo_2c0b9d8e0f17.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'test_validate_coordinates'), 'missing test_validate_coordinates'
assert hasattr(mod, 'test_get_aoi_from_user_input_address'), 'missing test_get_aoi_from_user_input_address'
assert hasattr(mod, 'test_get_aoi_from_user_input_coordinates'), 'missing test_get_aoi_from_user_input_coordinates'
assert hasattr(mod, 'test_get_aoi_from_user_input_rectangle'), 'missing test_get_aoi_from_user_input_rectangle'
assert hasattr(mod, 'test_get_aoi_from_user_input_address_live'), 'missing test_get_aoi_from_user_input_address_live'
assert hasattr(mod, 'test_get_aoi_from_user_input_coordinates_live'), 'missing test_get_aoi_from_user_input_coordinates_live'
assert hasattr(mod, 'test_get_aoi_invalid_address_raises'), 'missing test_get_aoi_invalid_address_raises'
assert hasattr(mod, 'test_explode_multigeoemtries'), 'missing test_explode_multigeoemtries'
