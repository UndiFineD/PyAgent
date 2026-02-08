
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_ovo_py_acceptance_thresholds_components_83852fb8bdc6.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'thresholds_and_histograms_component'), 'missing thresholds_and_histograms_component'
assert hasattr(mod, 'thresholds_input_component'), 'missing thresholds_input_component'
assert hasattr(mod, 'single_threshold_input_component'), 'missing single_threshold_input_component'
assert hasattr(mod, 'descriptor_histogram_component'), 'missing descriptor_histogram_component'
assert hasattr(mod, 'filter_designs_by_thresholds_cached'), 'missing filter_designs_by_thresholds_cached'
assert hasattr(mod, 'accept_designs_dialog'), 'missing accept_designs_dialog'
assert hasattr(mod, 'display_current_thresholds'), 'missing display_current_thresholds'
