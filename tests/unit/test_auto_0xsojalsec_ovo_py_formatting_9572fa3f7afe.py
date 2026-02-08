
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_ovo_py_formatting_9572fa3f7afe.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'format_duration'), 'missing format_duration'
assert hasattr(mod, 'generate_id'), 'missing generate_id'
assert hasattr(mod, 'get_hash_of_bytes'), 'missing get_hash_of_bytes'
assert hasattr(mod, 'get_hashed_path_for_bytes'), 'missing get_hashed_path_for_bytes'
assert hasattr(mod, 'safe_filename'), 'missing safe_filename'
assert hasattr(mod, 'parse_args'), 'missing parse_args'
assert hasattr(mod, 'get_alphanumeric_sort_key'), 'missing get_alphanumeric_sort_key'
assert hasattr(mod, 'sorted_alphanumeric'), 'missing sorted_alphanumeric'
assert hasattr(mod, 'truncated_list'), 'missing truncated_list'
