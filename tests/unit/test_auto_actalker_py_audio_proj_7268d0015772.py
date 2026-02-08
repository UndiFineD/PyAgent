
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\actalker_py_audio_proj_7268d0015772.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'AudioProjModel'), 'missing AudioProjModel'
assert hasattr(mod, 'VasaProjModel'), 'missing VasaProjModel'
assert hasattr(mod, 'IDProjModel'), 'missing IDProjModel'
assert hasattr(mod, 'ExpProjModel'), 'missing ExpProjModel'
assert hasattr(mod, 'MotionControlProjModel'), 'missing MotionControlProjModel'
