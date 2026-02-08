
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_volweb_py_tasks_cdfc4cee7999.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'compute_handles'), 'missing compute_handles'
assert hasattr(mod, 'dump_process_pslist'), 'missing dump_process_pslist'
assert hasattr(mod, 'dump_process_memmap'), 'missing dump_process_memmap'
assert hasattr(mod, 'dump_file'), 'missing dump_file'
