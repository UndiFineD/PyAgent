
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_for_site_9199d9475eed.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'WhyPi'), 'missing WhyPi'
assert hasattr(mod, 'GeneralExpositionIcon'), 'missing GeneralExpositionIcon'
assert hasattr(mod, 'GeometryIcon'), 'missing GeometryIcon'
assert hasattr(mod, 'PhysicsIcon'), 'missing PhysicsIcon'
assert hasattr(mod, 'SupportIcon'), 'missing SupportIcon'
assert hasattr(mod, 'SupportPitch1'), 'missing SupportPitch1'
assert hasattr(mod, 'SupportPitch2'), 'missing SupportPitch2'
assert hasattr(mod, 'SupportPitch3'), 'missing SupportPitch3'
assert hasattr(mod, 'SupportPitch4'), 'missing SupportPitch4'
assert hasattr(mod, 'RantPage'), 'missing RantPage'
assert hasattr(mod, 'ClipsLogo'), 'missing ClipsLogo'
