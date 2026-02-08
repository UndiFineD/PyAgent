
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_praisonai_py_flow_display_3b3f3dc80ec6.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'FlowDisplay'), 'missing FlowDisplay'
assert hasattr(mod, 'track_workflow'), 'missing track_workflow'
