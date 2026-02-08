
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_ovo_py_descriptor_scatterplot_0ff85d69a081.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'PlotSettings'), 'missing PlotSettings'
assert hasattr(mod, 'descriptor_scatterplot_input_component'), 'missing descriptor_scatterplot_input_component'
assert hasattr(mod, 'descriptor_scatterplot_design_explorer_component'), 'missing descriptor_scatterplot_design_explorer_component'
assert hasattr(mod, 'descriptor_scatterplot_pool_details_component'), 'missing descriptor_scatterplot_pool_details_component'
assert hasattr(mod, 'format_descriptor_name'), 'missing format_descriptor_name'
assert hasattr(mod, 'get_trimmed_min_max'), 'missing get_trimmed_min_max'
assert hasattr(mod, 'format_range'), 'missing format_range'
assert hasattr(mod, 'print_missing'), 'missing print_missing'
