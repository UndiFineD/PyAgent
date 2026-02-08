
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pytorch_lightning_py_progress_e98c4e0cfa4e.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, '_BaseProgress'), 'missing _BaseProgress'
assert hasattr(mod, '_ReadyCompletedTracker'), 'missing _ReadyCompletedTracker'
assert hasattr(mod, '_StartedTracker'), 'missing _StartedTracker'
assert hasattr(mod, '_ProcessedTracker'), 'missing _ProcessedTracker'
assert hasattr(mod, '_Progress'), 'missing _Progress'
assert hasattr(mod, '_BatchProgress'), 'missing _BatchProgress'
assert hasattr(mod, '_SchedulerProgress'), 'missing _SchedulerProgress'
assert hasattr(mod, '_OptimizerProgress'), 'missing _OptimizerProgress'
assert hasattr(mod, '_OptimizationProgress'), 'missing _OptimizationProgress'
