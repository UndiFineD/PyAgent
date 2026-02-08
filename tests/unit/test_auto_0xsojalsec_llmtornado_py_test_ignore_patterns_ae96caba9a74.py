
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_llmtornado_py_test_ignore_patterns_ae96caba9a74.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'temp_dir'), 'missing temp_dir'
assert hasattr(mod, 'test_default_ignores'), 'missing test_default_ignores'
assert hasattr(mod, 'test_gitignore_patterns'), 'missing test_gitignore_patterns'
assert hasattr(mod, 'test_fskbignore_patterns'), 'missing test_fskbignore_patterns'
assert hasattr(mod, 'test_pattern_reload'), 'missing test_pattern_reload'
