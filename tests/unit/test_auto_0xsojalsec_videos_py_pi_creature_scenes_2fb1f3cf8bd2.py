
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_pi_creature_scenes_2fb1f3cf8bd2.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'IveHeardOfThis'), 'missing IveHeardOfThis'
assert hasattr(mod, 'InFouriersShoes'), 'missing InFouriersShoes'
assert hasattr(mod, 'SineCurveIsUnrealistic'), 'missing SineCurveIsUnrealistic'
assert hasattr(mod, 'IfOnly'), 'missing IfOnly'
assert hasattr(mod, 'SoWeGotNowhere'), 'missing SoWeGotNowhere'
