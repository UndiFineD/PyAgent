
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pytorch_lightning_py_configuration_validator_cbe30623c120.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, '_verify_loop_configurations'), 'missing _verify_loop_configurations'
assert hasattr(mod, '__verify_train_val_loop_configuration'), 'missing __verify_train_val_loop_configuration'
assert hasattr(mod, '__verify_eval_loop_configuration'), 'missing __verify_eval_loop_configuration'
assert hasattr(mod, '__verify_manual_optimization_support'), 'missing __verify_manual_optimization_support'
assert hasattr(mod, '__warn_dataloader_iter_limitations'), 'missing __warn_dataloader_iter_limitations'
assert hasattr(mod, '__verify_configure_model_configuration'), 'missing __verify_configure_model_configuration'
