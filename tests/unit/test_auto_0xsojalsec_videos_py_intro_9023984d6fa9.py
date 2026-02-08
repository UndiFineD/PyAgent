
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_intro_9023984d6fa9.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'Chapter1OpeningQuote'), 'missing Chapter1OpeningQuote'
assert hasattr(mod, 'Introduction'), 'missing Introduction'
