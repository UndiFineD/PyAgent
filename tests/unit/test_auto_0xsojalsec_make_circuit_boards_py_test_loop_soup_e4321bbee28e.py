
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_make_circuit_boards_py_test_loop_soup_e4321bbee28e.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'assert_loop_is_lonely'), 'missing assert_loop_is_lonely'
assert hasattr(mod, 'test_lonely_loop'), 'missing test_lonely_loop'
assert hasattr(mod, 'test_joining_two_loney_loops'), 'missing test_joining_two_loney_loops'
assert hasattr(mod, 'test_joining_lonely_with_many_loop'), 'missing test_joining_lonely_with_many_loop'
assert hasattr(mod, 'test_joining_many_with_many'), 'missing test_joining_many_with_many'
assert hasattr(mod, 'test_joining_loop_onto_itself'), 'missing test_joining_loop_onto_itself'
assert hasattr(mod, 'test_limit'), 'missing test_limit'
assert hasattr(mod, 'test_loop_soup'), 'missing test_loop_soup'
