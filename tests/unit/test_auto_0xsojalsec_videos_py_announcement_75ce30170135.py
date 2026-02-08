
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_announcement_75ce30170135.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'IntersectionAndUnion'), 'missing IntersectionAndUnion'
assert hasattr(mod, 'WinnerCategories'), 'missing WinnerCategories'
assert hasattr(mod, 'ComplainAboutGithub'), 'missing ComplainAboutGithub'
assert hasattr(mod, 'Triumverate'), 'missing Triumverate'
assert hasattr(mod, 'Winners'), 'missing Winners'
assert hasattr(mod, 'EndingAnimation'), 'missing EndingAnimation'
assert hasattr(mod, 'Thumbnail'), 'missing Thumbnail'
