
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_ovo_py_download_component_62fc3805a2c8.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'download_job_designs_component'), 'missing download_job_designs_component'
assert hasattr(mod, 'download_descriptor_table'), 'missing download_descriptor_table'
assert hasattr(mod, 'download_design_files'), 'missing download_design_files'
