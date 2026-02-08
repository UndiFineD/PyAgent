
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pytorch_lightning_py_parsing_c44ab98265e2.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'is_picklable'), 'missing is_picklable'
assert hasattr(mod, 'clean_namespace'), 'missing clean_namespace'
assert hasattr(mod, 'parse_class_init_keys'), 'missing parse_class_init_keys'
assert hasattr(mod, 'get_init_args'), 'missing get_init_args'
assert hasattr(mod, '_get_init_args'), 'missing _get_init_args'
assert hasattr(mod, 'collect_init_args'), 'missing collect_init_args'
assert hasattr(mod, 'save_hyperparameters'), 'missing save_hyperparameters'
assert hasattr(mod, 'AttributeDict'), 'missing AttributeDict'
assert hasattr(mod, '_lightning_get_all_attr_holders'), 'missing _lightning_get_all_attr_holders'
assert hasattr(mod, '_lightning_get_first_attr_holder'), 'missing _lightning_get_first_attr_holder'
assert hasattr(mod, 'lightning_hasattr'), 'missing lightning_hasattr'
assert hasattr(mod, 'lightning_getattr'), 'missing lightning_getattr'
assert hasattr(mod, 'lightning_setattr'), 'missing lightning_setattr'
