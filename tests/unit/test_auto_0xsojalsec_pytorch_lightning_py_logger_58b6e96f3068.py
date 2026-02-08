
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pytorch_lightning_py_logger_58b6e96f3068.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'Logger'), 'missing Logger'
assert hasattr(mod, 'rank_zero_experiment'), 'missing rank_zero_experiment'
assert hasattr(mod, '_DummyExperiment'), 'missing _DummyExperiment'
