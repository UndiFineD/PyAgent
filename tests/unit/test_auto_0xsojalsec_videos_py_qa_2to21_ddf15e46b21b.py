
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_qa_2to21_ddf15e46b21b.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'Questions'), 'missing Questions'
assert hasattr(mod, 'MathematicianPlusX'), 'missing MathematicianPlusX'
assert hasattr(mod, 'NoClearCutPath'), 'missing NoClearCutPath'
assert hasattr(mod, 'Cumulative'), 'missing Cumulative'
assert hasattr(mod, 'HolidayStorePromotionTime'), 'missing HolidayStorePromotionTime'
