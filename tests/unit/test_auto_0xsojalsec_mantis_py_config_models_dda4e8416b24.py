
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_mantis_py_config_models_dda4e8416b24.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'DBConfig'), 'missing DBConfig'
assert hasattr(mod, 'ReportOutputConfig'), 'missing ReportOutputConfig'
assert hasattr(mod, 'Module'), 'missing Module'
assert hasattr(mod, 'Workflow'), 'missing Workflow'
assert hasattr(mod, 'Notify'), 'missing Notify'
assert hasattr(mod, 'AWSConfig'), 'missing AWSConfig'
assert hasattr(mod, 'NucleiTemplate'), 'missing NucleiTemplate'
assert hasattr(mod, 'AppConfig'), 'missing AppConfig'
