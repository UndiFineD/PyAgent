
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_web_navigator_py_views_20318c8cfa1a.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'SharedBaseModel'), 'missing SharedBaseModel'
assert hasattr(mod, 'Done'), 'missing Done'
assert hasattr(mod, 'Click'), 'missing Click'
assert hasattr(mod, 'Type'), 'missing Type'
assert hasattr(mod, 'Wait'), 'missing Wait'
assert hasattr(mod, 'Scroll'), 'missing Scroll'
assert hasattr(mod, 'GoTo'), 'missing GoTo'
assert hasattr(mod, 'Back'), 'missing Back'
assert hasattr(mod, 'Forward'), 'missing Forward'
assert hasattr(mod, 'Key'), 'missing Key'
assert hasattr(mod, 'Download'), 'missing Download'
assert hasattr(mod, 'Scrape'), 'missing Scrape'
assert hasattr(mod, 'Tab'), 'missing Tab'
assert hasattr(mod, 'Upload'), 'missing Upload'
assert hasattr(mod, 'Menu'), 'missing Menu'
assert hasattr(mod, 'Script'), 'missing Script'
assert hasattr(mod, 'HumanInput'), 'missing HumanInput'
