
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_eigenlecture_3c7394b9d865.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'get_intensity_colors'), 'missing get_intensity_colors'
assert hasattr(mod, 'TexScratchPad'), 'missing TexScratchPad'
assert hasattr(mod, 'get_vector_field_and_stream_lines'), 'missing get_vector_field_and_stream_lines'
assert hasattr(mod, 'VectorFieldSolution'), 'missing VectorFieldSolution'
assert hasattr(mod, 'Transformation'), 'missing Transformation'
