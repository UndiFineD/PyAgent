
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pytorch_lightning_py_setup_188d6e6b6934.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, '_init_debugging_flags'), 'missing _init_debugging_flags'
assert hasattr(mod, '_determine_batch_limits'), 'missing _determine_batch_limits'
assert hasattr(mod, '_init_profiler'), 'missing _init_profiler'
assert hasattr(mod, '_log_device_info'), 'missing _log_device_info'
assert hasattr(mod, '_parse_time_interval_seconds'), 'missing _parse_time_interval_seconds'
