
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_ovo_py_test_config_object_8cd9f31244b1.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'test_config_default'), 'missing test_config_default'
assert hasattr(mod, 'test_config_with_extra_args'), 'missing test_config_with_extra_args'
