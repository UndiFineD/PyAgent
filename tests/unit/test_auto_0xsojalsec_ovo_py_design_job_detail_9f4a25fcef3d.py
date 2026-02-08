
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_ovo_py_design_job_detail_9f4a25fcef3d.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'design_job_detail'), 'missing design_job_detail'
assert hasattr(mod, 'scatterplot_fragment'), 'missing scatterplot_fragment'
assert hasattr(mod, 'visualize_designs_fragment'), 'missing visualize_designs_fragment'
