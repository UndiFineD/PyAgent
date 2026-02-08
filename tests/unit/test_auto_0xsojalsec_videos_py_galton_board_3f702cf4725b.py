
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_galton_board_3f702cf4725b.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'GaltonBoard'), 'missing GaltonBoard'
assert hasattr(mod, 'EmphasizeMultipleSums'), 'missing EmphasizeMultipleSums'
assert hasattr(mod, 'GaltonTrickle'), 'missing GaltonTrickle'
assert hasattr(mod, 'BiggerGaltonBoard'), 'missing BiggerGaltonBoard'
assert hasattr(mod, 'SingleDropBigGaltonBoard'), 'missing SingleDropBigGaltonBoard'
assert hasattr(mod, 'NotIdenticallyDistributed'), 'missing NotIdenticallyDistributed'
