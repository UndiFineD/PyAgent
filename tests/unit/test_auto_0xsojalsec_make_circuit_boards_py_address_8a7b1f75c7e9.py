
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_make_circuit_boards_py_address_8a7b1f75c7e9.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'AddrStr'), 'missing AddrStr'
assert hasattr(mod, 'AddressError'), 'missing AddressError'
assert hasattr(mod, '_handle_windows'), 'missing _handle_windows'
assert hasattr(mod, 'get_file'), 'missing get_file'
assert hasattr(mod, 'get_relative_addr_str'), 'missing get_relative_addr_str'
assert hasattr(mod, 'get_entry'), 'missing get_entry'
assert hasattr(mod, 'get_entry_section'), 'missing get_entry_section'
assert hasattr(mod, 'get_instance_section'), 'missing get_instance_section'
assert hasattr(mod, 'get_name'), 'missing get_name'
assert hasattr(mod, 'add_instance'), 'missing add_instance'
assert hasattr(mod, 'add_instances'), 'missing add_instances'
assert hasattr(mod, 'add_entry'), 'missing add_entry'
assert hasattr(mod, 'add_entries'), 'missing add_entries'
assert hasattr(mod, 'from_parts'), 'missing from_parts'
assert hasattr(mod, 'get_parent_instance_addr'), 'missing get_parent_instance_addr'
assert hasattr(mod, 'get_instance_names'), 'missing get_instance_names'
