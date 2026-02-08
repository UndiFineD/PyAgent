
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\ace_plus_py_ace_plus_ldm_6ea9ad292032.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'LatentDiffusionACEPlus'), 'missing LatentDiffusionACEPlus'
