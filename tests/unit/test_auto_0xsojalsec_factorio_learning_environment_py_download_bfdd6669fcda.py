
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_factorio_learning_environment_py_download_bfdd6669fcda.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'OptimizedSpriteDownloader'), 'missing OptimizedSpriteDownloader'
assert hasattr(mod, 'download_sprites_from_hf'), 'missing download_sprites_from_hf'
assert hasattr(mod, 'check_for_archive'), 'missing check_for_archive'
assert hasattr(mod, 'download_archive_strategy'), 'missing download_archive_strategy'
assert hasattr(mod, 'download_snapshot_strategy'), 'missing download_snapshot_strategy'
assert hasattr(mod, 'download_parallel_strategy'), 'missing download_parallel_strategy'
assert hasattr(mod, 'create_sprite_archive'), 'missing create_sprite_archive'
assert hasattr(mod, 'generate_sprites'), 'missing generate_sprites'
