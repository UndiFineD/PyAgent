
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pi3mos_slam_py_correlation_c412a724da1e.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'CorrLayer'), 'missing CorrLayer'
assert hasattr(mod, 'PatchLayer'), 'missing PatchLayer'
assert hasattr(mod, 'patchify'), 'missing patchify'
assert hasattr(mod, 'corr'), 'missing corr'
