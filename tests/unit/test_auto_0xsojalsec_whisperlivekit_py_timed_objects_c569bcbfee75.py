
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_whisperlivekit_py_timed_objects_c569bcbfee75.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'TimedText'), 'missing TimedText'
assert hasattr(mod, 'ASRToken'), 'missing ASRToken'
assert hasattr(mod, 'Sentence'), 'missing Sentence'
assert hasattr(mod, 'Transcript'), 'missing Transcript'
assert hasattr(mod, 'SpeakerSegment'), 'missing SpeakerSegment'
assert hasattr(mod, 'Silence'), 'missing Silence'
