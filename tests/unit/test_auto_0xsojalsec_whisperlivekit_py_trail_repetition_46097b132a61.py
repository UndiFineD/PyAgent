
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_whisperlivekit_py_trail_repetition_46097b132a61.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, '_detect_tail_repetition'), 'missing _detect_tail_repetition'
assert hasattr(mod, 'trim_tail_repetition'), 'missing trim_tail_repetition'
