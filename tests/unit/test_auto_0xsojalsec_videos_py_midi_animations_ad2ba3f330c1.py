
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_midi_animations_ad2ba3f330c1.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'AnimatedMidi'), 'missing AnimatedMidi'
assert hasattr(mod, 'AnimatedMidiTrapped5m'), 'missing AnimatedMidiTrapped5m'
assert hasattr(mod, 'STFTAlgorithmOnTrapped'), 'missing STFTAlgorithmOnTrapped'
assert hasattr(mod, 'HelpLongOnlineConverter'), 'missing HelpLongOnlineConverter'
