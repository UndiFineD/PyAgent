
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_circuits_f345c4fb6067.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'Resistor'), 'missing Resistor'
assert hasattr(mod, 'LongResistor'), 'missing LongResistor'
assert hasattr(mod, 'Source'), 'missing Source'
assert hasattr(mod, 'CircuitReduction'), 'missing CircuitReduction'
