
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agents_generic_py_log_queue_bbbdb36cc146.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'LogQueueListener'), 'missing LogQueueListener'
assert hasattr(mod, 'LogQueueHandler'), 'missing LogQueueHandler'
