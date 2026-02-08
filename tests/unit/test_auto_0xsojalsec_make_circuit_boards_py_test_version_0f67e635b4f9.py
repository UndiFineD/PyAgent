
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_make_circuit_boards_py_test_version_0f67e635b4f9.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'version'), 'missing version'
assert hasattr(mod, 'test_match_equal'), 'missing test_match_equal'
assert hasattr(mod, 'test_match_greater_than'), 'missing test_match_greater_than'
assert hasattr(mod, 'test_match_less_than'), 'missing test_match_less_than'
assert hasattr(mod, 'test_match_greater_than_or_equal'), 'missing test_match_greater_than_or_equal'
assert hasattr(mod, 'test_match_less_than_or_equal'), 'missing test_match_less_than_or_equal'
assert hasattr(mod, 'test_match_caret'), 'missing test_match_caret'
assert hasattr(mod, 'test_match_dirty'), 'missing test_match_dirty'
assert hasattr(mod, 'test_match_tilde'), 'missing test_match_tilde'
assert hasattr(mod, 'test_match_multiple'), 'missing test_match_multiple'
assert hasattr(mod, 'test_match_union'), 'missing test_match_union'
assert hasattr(mod, 'test_match_negation'), 'missing test_match_negation'
assert hasattr(mod, 'test_syntax_error'), 'missing test_syntax_error'
assert hasattr(mod, 'test_parse_valid_version'), 'missing test_parse_valid_version'
assert hasattr(mod, 'test_parse_version_with_build_info'), 'missing test_parse_version_with_build_info'
assert hasattr(mod, 'test_parse_version_with_prerelease_and_build_info'), 'missing test_parse_version_with_prerelease_and_build_info'
assert hasattr(mod, 'test_parse_version_with_hatch_shenanigans'), 'missing test_parse_version_with_hatch_shenanigans'
assert hasattr(mod, 'test_parse_invalid_version'), 'missing test_parse_invalid_version'
assert hasattr(mod, 'test_v_prefix'), 'missing test_v_prefix'
assert hasattr(mod, 'test_stringify'), 'missing test_stringify'
