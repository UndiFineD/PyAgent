
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_evermemos_py_interfaces_0fd9bc879cf4.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'MessageBatch'), 'missing MessageBatch'
assert hasattr(mod, 'LongJobStatus'), 'missing LongJobStatus'
assert hasattr(mod, 'LongJobInterface'), 'missing LongJobInterface'
assert hasattr(mod, 'ErrorHandler'), 'missing ErrorHandler'
assert hasattr(mod, 'RetryConfig'), 'missing RetryConfig'
assert hasattr(mod, 'ConsumerConfig'), 'missing ConsumerConfig'
