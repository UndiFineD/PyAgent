
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pytorch_lightning_py_progress_bar_f9cded3154c4.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'ProgressBar'), 'missing ProgressBar'
assert hasattr(mod, 'get_standard_metrics'), 'missing get_standard_metrics'
