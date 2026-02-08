
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_ovo_py_descriptor_tiles_8f78fd45df55.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'descriptor_overview_tiles'), 'missing descriptor_overview_tiles'
assert hasattr(mod, 'get_residue_presence_df'), 'missing get_residue_presence_df'
assert hasattr(mod, 'show_flag_counts'), 'missing show_flag_counts'
assert hasattr(mod, 'descriptor_tiles'), 'missing descriptor_tiles'
