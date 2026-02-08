
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_evermemos_py_answer_stage_d476b0e94ef4.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'build_context'), 'missing build_context'
assert hasattr(mod, 'run_answer_stage'), 'missing run_answer_stage'
