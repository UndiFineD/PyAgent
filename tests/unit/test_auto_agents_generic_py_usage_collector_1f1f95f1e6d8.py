
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agents_generic_py_usage_collector_1f1f95f1e6d8.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'UsageSummary'), 'missing UsageSummary'
assert hasattr(mod, 'UsageCollector'), 'missing UsageCollector'
