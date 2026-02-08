
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_multilayered_6ccd980af2bc.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'MultilayeredScene'), 'missing MultilayeredScene'
assert hasattr(mod, 'TwoToMany'), 'missing TwoToMany'
assert hasattr(mod, 'RaceLightInLayers'), 'missing RaceLightInLayers'
assert hasattr(mod, 'ShowDiscretePath'), 'missing ShowDiscretePath'
assert hasattr(mod, 'NLayers'), 'missing NLayers'
assert hasattr(mod, 'ShowLayerVariables'), 'missing ShowLayerVariables'
assert hasattr(mod, 'LimitingProcess'), 'missing LimitingProcess'
assert hasattr(mod, 'ShowLightAndSlidingObject'), 'missing ShowLightAndSlidingObject'
assert hasattr(mod, 'ContinuouslyObeyingSnellsLaw'), 'missing ContinuouslyObeyingSnellsLaw'
