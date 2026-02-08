
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agents_generic_py_participant_3b2722f6a463.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'wait_for_participant'), 'missing wait_for_participant'
assert hasattr(mod, 'wait_for_track_publication'), 'missing wait_for_track_publication'
