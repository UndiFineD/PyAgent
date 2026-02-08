
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_whisper_flow_py_streaming_9bd3d1292835.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'get_all'), 'missing get_all'
assert hasattr(mod, 'transcribe'), 'missing transcribe'
assert hasattr(mod, 'should_close_segment'), 'missing should_close_segment'
assert hasattr(mod, 'TranscribeSession'), 'missing TranscribeSession'
