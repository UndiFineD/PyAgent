
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_mantis_py_tool_logs_model_5d864de02f28.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'AssetLogs'), 'missing AssetLogs'
assert hasattr(mod, 'ModuleLogs'), 'missing ModuleLogs'
assert hasattr(mod, 'ScanLogs'), 'missing ScanLogs'
