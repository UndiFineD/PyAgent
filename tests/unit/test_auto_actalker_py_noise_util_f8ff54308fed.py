
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\actalker_py_noise_util_f8ff54308fed.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'random_noise'), 'missing random_noise'
assert hasattr(mod, 'video_fusion_noise'), 'missing video_fusion_noise'
