
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_prettymapp_py_conftest_dbba959c2478.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'pytest_addoption'), 'missing pytest_addoption'
assert hasattr(mod, 'pytest_collection_modifyitems'), 'missing pytest_collection_modifyitems'
