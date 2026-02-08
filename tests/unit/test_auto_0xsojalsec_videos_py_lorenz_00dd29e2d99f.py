
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_lorenz_00dd29e2d99f.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'lorenz_system'), 'missing lorenz_system'
assert hasattr(mod, 'ode_solution_points'), 'missing ode_solution_points'
assert hasattr(mod, 'for_later'), 'missing for_later'
assert hasattr(mod, 'LorenzAttractor'), 'missing LorenzAttractor'
assert hasattr(mod, 'EndScreen'), 'missing EndScreen'
