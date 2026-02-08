
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agents_generic_py_output_dbf34f97fd46.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, '_ParticipantAudioOutput'), 'missing _ParticipantAudioOutput'
assert hasattr(mod, '_ParticipantLegacyTranscriptionOutput'), 'missing _ParticipantLegacyTranscriptionOutput'
assert hasattr(mod, '_ParticipantStreamTranscriptionOutput'), 'missing _ParticipantStreamTranscriptionOutput'
assert hasattr(mod, '_ParticipantTranscriptionOutput'), 'missing _ParticipantTranscriptionOutput'
