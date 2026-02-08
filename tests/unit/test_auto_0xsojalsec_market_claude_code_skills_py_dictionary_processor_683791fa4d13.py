
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_market_claude_code_skills_py_dictionary_processor_683791fa4d13.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'Change'), 'missing Change'
assert hasattr(mod, 'DictionaryProcessor'), 'missing DictionaryProcessor'
