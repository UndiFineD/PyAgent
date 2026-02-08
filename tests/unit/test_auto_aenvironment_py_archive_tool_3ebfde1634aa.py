
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\aenvironment_py_archive_tool_3ebfde1634aa.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'ArchiveTool'), 'missing ArchiveTool'
assert hasattr(mod, 'ArchiveContext'), 'missing ArchiveContext'
assert hasattr(mod, 'ArchiveCleanup'), 'missing ArchiveCleanup'
assert hasattr(mod, 'quick_pack'), 'missing quick_pack'
assert hasattr(mod, 'quick_cleanup'), 'missing quick_cleanup'
assert hasattr(mod, 'TempArchive'), 'missing TempArchive'
