
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xSojalSec_ldapper_exceptions.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'LdapperError'), 'missing LdapperError'
assert hasattr(mod, 'AddDNFailed'), 'missing AddDNFailed'
assert hasattr(mod, 'ArgumentError'), 'missing ArgumentError'
assert hasattr(mod, 'DuplicateValue'), 'missing DuplicateValue'
assert hasattr(mod, 'NoSuchAttrValue'), 'missing NoSuchAttrValue'
assert hasattr(mod, 'NoSuchDN'), 'missing NoSuchDN'
assert hasattr(mod, 'InvalidDN'), 'missing InvalidDN'
