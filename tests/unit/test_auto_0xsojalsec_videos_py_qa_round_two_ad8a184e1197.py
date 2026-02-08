
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_qa_round_two_ad8a184e1197.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'Test'), 'missing Test'
assert hasattr(mod, 'Announcements'), 'missing Announcements'
assert hasattr(mod, 'PowersOfTwo'), 'missing PowersOfTwo'
assert hasattr(mod, 'PiHoldingScreen'), 'missing PiHoldingScreen'
assert hasattr(mod, 'QuestionsLink'), 'missing QuestionsLink'
assert hasattr(mod, 'Thumbnail'), 'missing Thumbnail'
