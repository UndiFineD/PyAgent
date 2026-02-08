
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_prettymapp_py_utils_d30325933b14.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'st_get_osm_geometries'), 'missing st_get_osm_geometries'
assert hasattr(mod, 'st_plot_all'), 'missing st_plot_all'
assert hasattr(mod, 'get_colors_from_style'), 'missing get_colors_from_style'
assert hasattr(mod, 'plt_to_svg'), 'missing plt_to_svg'
assert hasattr(mod, 'svg_to_html'), 'missing svg_to_html'
assert hasattr(mod, 'plt_to_href'), 'missing plt_to_href'
assert hasattr(mod, 'slugify'), 'missing slugify'
assert hasattr(mod, 'gdf_to_bytesio_geojson'), 'missing gdf_to_bytesio_geojson'
