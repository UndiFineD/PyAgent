
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_long_fourier_scenes_c08bad7fa387.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'FourierSeriesExampleWithRectForZoom'), 'missing FourierSeriesExampleWithRectForZoom'
assert hasattr(mod, 'ZoomedInFourierSeriesExample'), 'missing ZoomedInFourierSeriesExample'
assert hasattr(mod, 'ZoomedInFourierSeriesExample100x'), 'missing ZoomedInFourierSeriesExample100x'
assert hasattr(mod, 'TrebleClefFourierSeriesExampleWithRectForZoom'), 'missing TrebleClefFourierSeriesExampleWithRectForZoom'
assert hasattr(mod, 'TrebleClefZoomedInFourierSeriesExample'), 'missing TrebleClefZoomedInFourierSeriesExample'
assert hasattr(mod, 'NailAndGearFourierSeriesExampleWithRectForZoom'), 'missing NailAndGearFourierSeriesExampleWithRectForZoom'
assert hasattr(mod, 'NailAndGearZoomedInFourierSeriesExample'), 'missing NailAndGearZoomedInFourierSeriesExample'
assert hasattr(mod, 'SigmaFourierSeriesExampleWithRectForZoom'), 'missing SigmaFourierSeriesExampleWithRectForZoom'
assert hasattr(mod, 'SigmaZoomedInFourierSeriesExample'), 'missing SigmaZoomedInFourierSeriesExample'
assert hasattr(mod, 'FourierOfFourier'), 'missing FourierOfFourier'
assert hasattr(mod, 'FourierOfFourierZoomedIn'), 'missing FourierOfFourierZoomedIn'
assert hasattr(mod, 'FourierOfFourier100xZoom'), 'missing FourierOfFourier100xZoom'
assert hasattr(mod, 'FourierOfHilbert'), 'missing FourierOfHilbert'
assert hasattr(mod, 'FourierOfHilbertZoomedIn'), 'missing FourierOfHilbertZoomedIn'
assert hasattr(mod, 'FourierOfBritain'), 'missing FourierOfBritain'
assert hasattr(mod, 'FourierOfBritainZoomedIn'), 'missing FourierOfBritainZoomedIn'
assert hasattr(mod, 'FourierOfSeattle'), 'missing FourierOfSeattle'
assert hasattr(mod, 'FourierOfSeattleZoomedIn'), 'missing FourierOfSeattleZoomedIn'
assert hasattr(mod, 'VideoWrapper'), 'missing VideoWrapper'
