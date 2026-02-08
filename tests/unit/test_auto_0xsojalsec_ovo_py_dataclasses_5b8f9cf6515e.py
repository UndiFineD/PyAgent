
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_ovo_py_dataclasses_5b8f9cf6515e.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'ContigSegment'), 'missing ContigSegment'
assert hasattr(mod, 'EnhancedJSONEncoder'), 'missing EnhancedJSONEncoder'
assert hasattr(mod, 'ChainVisualization'), 'missing ChainVisualization'
assert hasattr(mod, 'StructureVisualization'), 'missing StructureVisualization'
