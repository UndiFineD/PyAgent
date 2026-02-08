
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_evermemos_py_scan_context_72f4ecbf9d19.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, '_PathTrieNode'), 'missing _PathTrieNode'
assert hasattr(mod, 'ScanContextRegistry'), 'missing ScanContextRegistry'
assert hasattr(mod, 'get_scan_context_registry'), 'missing get_scan_context_registry'
