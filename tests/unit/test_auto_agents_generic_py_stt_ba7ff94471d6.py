
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agents_generic_py_stt_ba7ff94471d6.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'STTOptions'), 'missing STTOptions'
assert hasattr(mod, 'STT'), 'missing STT'
assert hasattr(mod, 'SpeechStream'), 'missing SpeechStream'
assert hasattr(mod, 'live_transcription_to_speech_data'), 'missing live_transcription_to_speech_data'
assert hasattr(mod, 'prerecorded_transcription_to_speech_event'), 'missing prerecorded_transcription_to_speech_event'
assert hasattr(mod, '_validate_model'), 'missing _validate_model'
assert hasattr(mod, '_validate_tags'), 'missing _validate_tags'
assert hasattr(mod, '_validate_keyterms'), 'missing _validate_keyterms'
