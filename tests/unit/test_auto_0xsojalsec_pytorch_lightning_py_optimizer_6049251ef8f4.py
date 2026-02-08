
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pytorch_lightning_py_optimizer_6049251ef8f4.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'do_nothing_closure'), 'missing do_nothing_closure'
assert hasattr(mod, 'LightningOptimizer'), 'missing LightningOptimizer'
assert hasattr(mod, '_init_optimizers_and_lr_schedulers'), 'missing _init_optimizers_and_lr_schedulers'
assert hasattr(mod, '_configure_optimizers'), 'missing _configure_optimizers'
assert hasattr(mod, '_configure_schedulers_automatic_opt'), 'missing _configure_schedulers_automatic_opt'
assert hasattr(mod, '_configure_schedulers_manual_opt'), 'missing _configure_schedulers_manual_opt'
assert hasattr(mod, '_validate_scheduler_api'), 'missing _validate_scheduler_api'
assert hasattr(mod, '_validate_multiple_optimizers_support'), 'missing _validate_multiple_optimizers_support'
assert hasattr(mod, '_validate_optimizers_attached'), 'missing _validate_optimizers_attached'
assert hasattr(mod, '_validate_optim_conf'), 'missing _validate_optim_conf'
assert hasattr(mod, '_MockOptimizer'), 'missing _MockOptimizer'
