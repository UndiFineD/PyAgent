
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_make_circuit_boards_py_test_datatypes_b286eb692e9d.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'test_ref_from_one'), 'missing test_ref_from_one'
assert hasattr(mod, 'test_ref_add_name'), 'missing test_ref_add_name'
assert hasattr(mod, 'test_keyoptitem_from_kv'), 'missing test_keyoptitem_from_kv'
assert hasattr(mod, 'test_keyoptmap_from_item'), 'missing test_keyoptmap_from_item'
assert hasattr(mod, 'test_keyoptmap_from_kv'), 'missing test_keyoptmap_from_kv'
assert hasattr(mod, 'test_keyoptitem_ref'), 'missing test_keyoptitem_ref'
assert hasattr(mod, 'test_keyoptmap_get_named_items'), 'missing test_keyoptmap_get_named_items'
assert hasattr(mod, 'test_filter_items_by_type'), 'missing test_filter_items_by_type'
assert hasattr(mod, 'test_keyoptmap_get_items_by_type'), 'missing test_keyoptmap_get_items_by_type'
assert hasattr(mod, 'test_keyoptmap_get_unnamed_items'), 'missing test_keyoptmap_get_unnamed_items'
assert hasattr(mod, 'test_keyoptmap_keys'), 'missing test_keyoptmap_keys'
assert hasattr(mod, 'test_keyoptmap_values'), 'missing test_keyoptmap_values'
assert hasattr(mod, 'test_strainer'), 'missing test_strainer'
assert hasattr(mod, 'test_stack_list'), 'missing test_stack_list'
assert hasattr(mod, 'test_DotDict'), 'missing test_DotDict'
