
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\ad_miner_py_generic_formating_df2ac9272098.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'get_label_icon_dictionary'), 'missing get_label_icon_dictionary'
assert hasattr(mod, 'formatGridValues2Columns'), 'missing formatGridValues2Columns'
assert hasattr(mod, 'formatGridValues1Columns'), 'missing formatGridValues1Columns'
assert hasattr(mod, 'formatGridValues3Columns'), 'missing formatGridValues3Columns'
assert hasattr(mod, 'formatFor3Col'), 'missing formatFor3Col'
