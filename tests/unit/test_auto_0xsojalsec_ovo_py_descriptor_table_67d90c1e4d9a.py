
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_ovo_py_descriptor_table_67d90c1e4d9a.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'get_descriptor_column_config'), 'missing get_descriptor_column_config'
assert hasattr(mod, 'get_residue_number_column_config'), 'missing get_residue_number_column_config'
assert hasattr(mod, 'make_bg_color_func'), 'missing make_bg_color_func'
assert hasattr(mod, 'descriptor_table'), 'missing descriptor_table'
assert hasattr(mod, 'residue_number_descriptor_detail_table'), 'missing residue_number_descriptor_detail_table'
