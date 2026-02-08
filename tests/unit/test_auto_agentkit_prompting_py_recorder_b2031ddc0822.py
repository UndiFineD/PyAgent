
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agentkit_prompting_py_recorder_b2031ddc0822.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'Recorder'), 'missing Recorder'
assert hasattr(mod, 'StatsRecorder'), 'missing StatsRecorder'
assert hasattr(mod, 'VideoRecorder'), 'missing VideoRecorder'
assert hasattr(mod, 'EpisodeRecorder'), 'missing EpisodeRecorder'
assert hasattr(mod, 'EpisodeName'), 'missing EpisodeName'
