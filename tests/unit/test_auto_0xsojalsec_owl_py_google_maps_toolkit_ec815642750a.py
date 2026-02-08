
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_owl_py_google_maps_toolkit_ec815642750a.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'handle_googlemaps_exceptions'), 'missing handle_googlemaps_exceptions'
assert hasattr(mod, '_format_offset_to_natural_language'), 'missing _format_offset_to_natural_language'
assert hasattr(mod, 'GoogleMapsToolkit'), 'missing GoogleMapsToolkit'
