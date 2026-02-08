
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_volweb_py_serializers_c9de706cb180.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'SymbolSerializer'), 'missing SymbolSerializer'
assert hasattr(mod, 'send_symbol_created'), 'missing send_symbol_created'
assert hasattr(mod, 'send_symbol_created'), 'missing send_symbol_created'
