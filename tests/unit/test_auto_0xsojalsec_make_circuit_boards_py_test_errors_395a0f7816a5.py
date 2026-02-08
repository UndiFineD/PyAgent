
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_make_circuit_boards_py_test_errors_395a0f7816a5.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'test_error_accumulator'), 'missing test_error_accumulator'
assert hasattr(mod, 'test_iter_through_errors'), 'missing test_iter_through_errors'
