
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_ovo_py_param_validation_2588e03a6fea.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'validate_params'), 'missing validate_params'
assert hasattr(mod, 'coerce_types'), 'missing coerce_types'
assert hasattr(mod, 'flatten_schema'), 'missing flatten_schema'
