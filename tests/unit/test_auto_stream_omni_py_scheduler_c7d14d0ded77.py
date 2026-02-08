
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\stream_omni_py_scheduler_c7d14d0ded77.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'WarmupLR'), 'missing WarmupLR'
assert hasattr(mod, 'WarmupPolicy'), 'missing WarmupPolicy'
assert hasattr(mod, 'SquareRootConstantPolicy'), 'missing SquareRootConstantPolicy'
assert hasattr(mod, 'WarmupHoldPolicy'), 'missing WarmupHoldPolicy'
assert hasattr(mod, 'WarmupAnnealHoldPolicy'), 'missing WarmupAnnealHoldPolicy'
assert hasattr(mod, '_squareroot_annealing'), 'missing _squareroot_annealing'
assert hasattr(mod, '_square_annealing'), 'missing _square_annealing'
assert hasattr(mod, '_cosine_annealing'), 'missing _cosine_annealing'
assert hasattr(mod, '_linear_warmup_with_cosine_annealing'), 'missing _linear_warmup_with_cosine_annealing'
assert hasattr(mod, '_poly_decay'), 'missing _poly_decay'
assert hasattr(mod, '_noam_hold_annealing'), 'missing _noam_hold_annealing'
assert hasattr(mod, 'SquareAnnealing'), 'missing SquareAnnealing'
assert hasattr(mod, 'SquareRootAnnealing'), 'missing SquareRootAnnealing'
assert hasattr(mod, 'CosineAnnealing'), 'missing CosineAnnealing'
assert hasattr(mod, 'NoamAnnealing'), 'missing NoamAnnealing'
assert hasattr(mod, 'NoamHoldAnnealing'), 'missing NoamHoldAnnealing'
assert hasattr(mod, 'ConstantLR'), 'missing ConstantLR'
