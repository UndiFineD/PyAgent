
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pi0_lerobot_py_rerun_log_utils_94841bd935b9.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'create_blueprint'), 'missing create_blueprint'
assert hasattr(mod, 'log_mano_batch'), 'missing log_mano_batch'
