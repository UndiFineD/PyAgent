
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_talk_scenes_a29c8afac6a4.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'DoingMathVsHowMathIsPresented'), 'missing DoingMathVsHowMathIsPresented'
assert hasattr(mod, 'PiCharts'), 'missing PiCharts'
assert hasattr(mod, 'AskAboutCircleProportion'), 'missing AskAboutCircleProportion'
assert hasattr(mod, 'BorweinIntegrals'), 'missing BorweinIntegrals'
