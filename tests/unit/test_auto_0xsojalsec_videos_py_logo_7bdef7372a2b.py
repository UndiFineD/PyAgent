
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_logo_7bdef7372a2b.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'Logo'), 'missing Logo'
assert hasattr(mod, 'LogoGenerationTemplate'), 'missing LogoGenerationTemplate'
assert hasattr(mod, 'LogoGeneration'), 'missing LogoGeneration'
assert hasattr(mod, 'SortingLogoGeneration'), 'missing SortingLogoGeneration'
assert hasattr(mod, 'LogoTest'), 'missing LogoTest'
assert hasattr(mod, 'LogoGenerationFlurry'), 'missing LogoGenerationFlurry'
assert hasattr(mod, 'WrittenLogo'), 'missing WrittenLogo'
assert hasattr(mod, 'LogoGenerationFivefold'), 'missing LogoGenerationFivefold'
assert hasattr(mod, 'Vertical3B1B'), 'missing Vertical3B1B'
