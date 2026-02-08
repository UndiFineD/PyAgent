
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_make_circuit_boards_py_shortcodes_c7dc61310c9b.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'on_page_markdown'), 'missing on_page_markdown'
assert hasattr(mod, 'flag'), 'missing flag'
assert hasattr(mod, 'option'), 'missing option'
assert hasattr(mod, 'setting'), 'missing setting'
assert hasattr(mod, '_resolve_path'), 'missing _resolve_path'
assert hasattr(mod, '_resolve'), 'missing _resolve'
assert hasattr(mod, '_badge'), 'missing _badge'
assert hasattr(mod, '_badge_for_sponsors'), 'missing _badge_for_sponsors'
assert hasattr(mod, '_badge_for_version'), 'missing _badge_for_version'
assert hasattr(mod, '_badge_for_version_insiders'), 'missing _badge_for_version_insiders'
assert hasattr(mod, '_badge_for_feature'), 'missing _badge_for_feature'
assert hasattr(mod, '_badge_for_plugin'), 'missing _badge_for_plugin'
assert hasattr(mod, '_badge_for_extension'), 'missing _badge_for_extension'
assert hasattr(mod, '_badge_for_utility'), 'missing _badge_for_utility'
assert hasattr(mod, '_badge_for_example'), 'missing _badge_for_example'
assert hasattr(mod, '_badge_for_example_view'), 'missing _badge_for_example_view'
assert hasattr(mod, '_badge_for_example_download'), 'missing _badge_for_example_download'
assert hasattr(mod, '_badge_for_default'), 'missing _badge_for_default'
assert hasattr(mod, '_badge_for_default_none'), 'missing _badge_for_default_none'
assert hasattr(mod, '_badge_for_default_computed'), 'missing _badge_for_default_computed'
assert hasattr(mod, '_badge_for_metadata'), 'missing _badge_for_metadata'
assert hasattr(mod, '_badge_for_required'), 'missing _badge_for_required'
assert hasattr(mod, '_badge_for_customization'), 'missing _badge_for_customization'
assert hasattr(mod, '_badge_for_multiple'), 'missing _badge_for_multiple'
assert hasattr(mod, '_badge_for_experimental'), 'missing _badge_for_experimental'
