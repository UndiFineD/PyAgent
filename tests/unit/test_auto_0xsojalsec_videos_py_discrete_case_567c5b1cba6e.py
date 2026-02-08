
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_discrete_case_567c5b1cba6e.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'ShowNewRuleAtDiscreteBoundary'), 'missing ShowNewRuleAtDiscreteBoundary'
assert hasattr(mod, 'DiscreteEvolutionPoint25'), 'missing DiscreteEvolutionPoint25'
assert hasattr(mod, 'DiscreteEvolutionPoint1'), 'missing DiscreteEvolutionPoint1'
assert hasattr(mod, 'FlatEdgesForDiscreteEvolution'), 'missing FlatEdgesForDiscreteEvolution'
assert hasattr(mod, 'FlatEdgesForDiscreteEvolutionTinySteps'), 'missing FlatEdgesForDiscreteEvolutionTinySteps'
