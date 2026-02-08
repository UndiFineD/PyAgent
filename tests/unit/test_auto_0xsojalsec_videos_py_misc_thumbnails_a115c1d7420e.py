
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_misc_thumbnails_a115c1d7420e.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'LinalgThumbnail'), 'missing LinalgThumbnail'
assert hasattr(mod, 'CSThumbnail'), 'missing CSThumbnail'
assert hasattr(mod, 'GroupThumbnail'), 'missing GroupThumbnail'
assert hasattr(mod, 'BaselThumbnail'), 'missing BaselThumbnail'
assert hasattr(mod, 'Eola1Thumbnail'), 'missing Eola1Thumbnail'
assert hasattr(mod, 'pendulum_vector_field_func'), 'missing pendulum_vector_field_func'
assert hasattr(mod, 'ODEThumbnail'), 'missing ODEThumbnail'
assert hasattr(mod, 'PrimeSpirals'), 'missing PrimeSpirals'
assert hasattr(mod, 'EGraph'), 'missing EGraph'
