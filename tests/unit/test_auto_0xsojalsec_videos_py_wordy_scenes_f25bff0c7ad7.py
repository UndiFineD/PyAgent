
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_wordy_scenes_f25bff0c7ad7.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'WriteHeatEquationTemplate'), 'missing WriteHeatEquationTemplate'
assert hasattr(mod, 'HeatEquationIntroTitle'), 'missing HeatEquationIntroTitle'
assert hasattr(mod, 'BringTogether'), 'missing BringTogether'
assert hasattr(mod, 'FourierSeriesIntro'), 'missing FourierSeriesIntro'
assert hasattr(mod, 'CompareODEToPDE'), 'missing CompareODEToPDE'
assert hasattr(mod, 'TodaysTargetWrapper'), 'missing TodaysTargetWrapper'
assert hasattr(mod, 'TwoGraphTypeTitles'), 'missing TwoGraphTypeTitles'
assert hasattr(mod, 'ShowPartialDerivativeSymbols'), 'missing ShowPartialDerivativeSymbols'
assert hasattr(mod, 'WriteHeatEquation'), 'missing WriteHeatEquation'
assert hasattr(mod, 'Show3DEquation'), 'missing Show3DEquation'
assert hasattr(mod, 'Show1DAnd3DEquations'), 'missing Show1DAnd3DEquations'
assert hasattr(mod, 'D1EquationNoInputs'), 'missing D1EquationNoInputs'
assert hasattr(mod, 'AltHeatRHS'), 'missing AltHeatRHS'
assert hasattr(mod, 'CompareInputsOfGeneralCaseTo1D'), 'missing CompareInputsOfGeneralCaseTo1D'
assert hasattr(mod, 'ShowLaplacian'), 'missing ShowLaplacian'
assert hasattr(mod, 'AskAboutActuallySolving'), 'missing AskAboutActuallySolving'
assert hasattr(mod, 'PDEPatreonEndscreen'), 'missing PDEPatreonEndscreen'
