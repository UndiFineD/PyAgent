
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_owl_py_ask_news_toolkit_fc97fcbc3af1.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, '_process_response'), 'missing _process_response'
assert hasattr(mod, 'AskNewsToolkit'), 'missing AskNewsToolkit'
assert hasattr(mod, 'AsyncAskNewsToolkit'), 'missing AsyncAskNewsToolkit'
