
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_ovo_py_proteinqc_logic_9c42ec1635ae.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'tool_supports_scheduler'), 'missing tool_supports_scheduler'
assert hasattr(mod, 'get_available_schedulers'), 'missing get_available_schedulers'
assert hasattr(mod, 'get_available_tools'), 'missing get_available_tools'
assert hasattr(mod, 'get_descriptor_plot_setting'), 'missing get_descriptor_plot_setting'
assert hasattr(mod, 'get_thresholds_colormap'), 'missing get_thresholds_colormap'
assert hasattr(mod, 'get_plddt_color'), 'missing get_plddt_color'
assert hasattr(mod, 'get_pae_colormap'), 'missing get_pae_colormap'
assert hasattr(mod, 'get_rmsd_colormap'), 'missing get_rmsd_colormap'
assert hasattr(mod, 'get_higher_is_better_colormap'), 'missing get_higher_is_better_colormap'
assert hasattr(mod, 'get_lower_is_better_colormap'), 'missing get_lower_is_better_colormap'
assert hasattr(mod, 'get_neutral_colormap'), 'missing get_neutral_colormap'
assert hasattr(mod, 'get_descriptor_cmap'), 'missing get_descriptor_cmap'
assert hasattr(mod, 'get_cmap'), 'missing get_cmap'
assert hasattr(mod, 'get_flag_color'), 'missing get_flag_color'
assert hasattr(mod, 'get_descriptor_comment'), 'missing get_descriptor_comment'
