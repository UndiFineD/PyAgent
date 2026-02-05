
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\Chain_of_Recursive_Thoughts_tic_tac.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'print_board'), 'missing print_board'
assert hasattr(mod, 'check_winner'), 'missing check_winner'
assert hasattr(mod, 'is_board_full'), 'missing is_board_full'
assert hasattr(mod, 'tic_tac_toe'), 'missing tic_tac_toe'
