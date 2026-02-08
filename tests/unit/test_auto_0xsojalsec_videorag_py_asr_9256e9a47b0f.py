
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videorag_py_asr_9256e9a47b0f.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'process_single_segment'), 'missing process_single_segment'
assert hasattr(mod, 'speech_to_text_online'), 'missing speech_to_text_online'
assert hasattr(mod, 'speech_to_text_async'), 'missing speech_to_text_async'
assert hasattr(mod, 'speech_to_text'), 'missing speech_to_text'
