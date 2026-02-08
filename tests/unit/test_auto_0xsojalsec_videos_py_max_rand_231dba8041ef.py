
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_max_rand_231dba8041ef.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'Randomize'), 'missing Randomize'
assert hasattr(mod, 'TrackingDots'), 'missing TrackingDots'
assert hasattr(mod, 'get_random_var_label_group'), 'missing get_random_var_label_group'
assert hasattr(mod, 'MaxProcess'), 'missing MaxProcess'
assert hasattr(mod, 'SqrtProcess'), 'missing SqrtProcess'
assert hasattr(mod, 'SquareAndSquareRoot'), 'missing SquareAndSquareRoot'
assert hasattr(mod, 'GawkAtEquivalence'), 'missing GawkAtEquivalence'
assert hasattr(mod, 'VisualizeMaxOfPairCDF'), 'missing VisualizeMaxOfPairCDF'
assert hasattr(mod, 'MaxOfThreeTex'), 'missing MaxOfThreeTex'
assert hasattr(mod, 'Arrows'), 'missing Arrows'
