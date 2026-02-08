
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_temperature_scenes_c5f3e94fc02e.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'StepFunctionExample'), 'missing StepFunctionExample'
assert hasattr(mod, 'BreakDownStepFunction'), 'missing BreakDownStepFunction'
