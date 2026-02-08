
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_market_claude_code_skills_py_ai_processor_d6b689289647.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'AIChange'), 'missing AIChange'
assert hasattr(mod, 'AIProcessor'), 'missing AIProcessor'
