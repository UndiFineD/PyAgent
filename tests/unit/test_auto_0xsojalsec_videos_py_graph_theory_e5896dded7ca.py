
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_graph_theory_e5896dded7ca.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'Graph'), 'missing Graph'
assert hasattr(mod, 'CubeGraph'), 'missing CubeGraph'
assert hasattr(mod, 'SampleGraph'), 'missing SampleGraph'
assert hasattr(mod, 'OctohedronGraph'), 'missing OctohedronGraph'
assert hasattr(mod, 'CompleteGraph'), 'missing CompleteGraph'
assert hasattr(mod, 'DiscreteGraphScene'), 'missing DiscreteGraphScene'
