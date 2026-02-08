
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_proxyhub_py_judge_c285ac7ab7e9.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'Judge'), 'missing Judge'
assert hasattr(mod, 'get_judges'), 'missing get_judges'
