
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_starry_night_4cf258c416a9.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'stereo_project_point'), 'missing stereo_project_point'
assert hasattr(mod, 'StarryStarryNight'), 'missing StarryStarryNight'
