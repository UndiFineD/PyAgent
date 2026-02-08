
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pytorch_lightning_py_test_sync_batchnorm_parity_d9935ab9881e.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'SyncBNModule'), 'missing SyncBNModule'
assert hasattr(mod, 'test_sync_batchnorm_parity'), 'missing test_sync_batchnorm_parity'
assert hasattr(mod, '_train_single_process_sync_batchnorm'), 'missing _train_single_process_sync_batchnorm'
