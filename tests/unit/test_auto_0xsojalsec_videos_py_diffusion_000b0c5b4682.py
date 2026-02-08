
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_diffusion_000b0c5b4682.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'Diffusion1D'), 'missing Diffusion1D'
assert hasattr(mod, 'Diffusion1DWith1Dot'), 'missing Diffusion1DWith1Dot'
assert hasattr(mod, 'Diffusion1DStepFunction'), 'missing Diffusion1DStepFunction'
assert hasattr(mod, 'Diffusion1DStepFunctionGraphed'), 'missing Diffusion1DStepFunctionGraphed'
assert hasattr(mod, 'DiffusionDeltaGraphed'), 'missing DiffusionDeltaGraphed'
assert hasattr(mod, 'DiffusionDeltaGraphedTripleStart'), 'missing DiffusionDeltaGraphedTripleStart'
assert hasattr(mod, 'DiffusionDeltaGraphedShowingMean'), 'missing DiffusionDeltaGraphedShowingMean'
assert hasattr(mod, 'Diffusion2D'), 'missing Diffusion2D'
assert hasattr(mod, 'Diffusion2D1Dot'), 'missing Diffusion2D1Dot'
assert hasattr(mod, 'Diffusion2D10KDots'), 'missing Diffusion2D10KDots'
