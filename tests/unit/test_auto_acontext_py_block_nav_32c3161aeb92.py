
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\acontext_py_block_nav_32c3161aeb92.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, '_normalize_path_block_title'), 'missing _normalize_path_block_title'
assert hasattr(mod, 'path_to_parts'), 'missing path_to_parts'
assert hasattr(mod, 'assert_block_type'), 'missing assert_block_type'
assert hasattr(mod, 'fetch_path_children_by_id'), 'missing fetch_path_children_by_id'
assert hasattr(mod, 'list_paths_under_block'), 'missing list_paths_under_block'
assert hasattr(mod, 'find_block_by_path'), 'missing find_block_by_path'
assert hasattr(mod, 'recover_path_by_id'), 'missing recover_path_by_id'
assert hasattr(mod, 'get_path_info_by_id'), 'missing get_path_info_by_id'
assert hasattr(mod, 'read_blocks_from_par_id'), 'missing read_blocks_from_par_id'
assert hasattr(mod, 'get_block_by_sort'), 'missing get_block_by_sort'
