
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_evermemos_py_text_utils_a180ff2cf270.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'TokenType'), 'missing TokenType'
assert hasattr(mod, 'Token'), 'missing Token'
assert hasattr(mod, 'TokenConfig'), 'missing TokenConfig'
assert hasattr(mod, 'SmartTextParser'), 'missing SmartTextParser'
assert hasattr(mod, 'smart_truncate_text'), 'missing smart_truncate_text'
assert hasattr(mod, 'clean_whitespace'), 'missing clean_whitespace'
