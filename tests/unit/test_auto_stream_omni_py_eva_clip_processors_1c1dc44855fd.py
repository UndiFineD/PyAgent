
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\stream_omni_py_eva_clip_processors_1c1dc44855fd.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'BaseProcessor'), 'missing BaseProcessor'
assert hasattr(mod, 'EvaClipImageBaseProcessor'), 'missing EvaClipImageBaseProcessor'
assert hasattr(mod, 'EvaClipImageTrainProcessor'), 'missing EvaClipImageTrainProcessor'
