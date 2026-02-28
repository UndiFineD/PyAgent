# Auto-synced test for core/base/common/utils/dynamic_importer.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "dynamic_importer.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "import_from_path"), "import_from_path missing"
    assert hasattr(mod, "resolve_obj_by_qualname"), "resolve_obj_by_qualname missing"
    assert hasattr(mod, "resolve_obj_by_qualname_parts"), "resolve_obj_by_qualname_parts missing"
    assert hasattr(mod, "PlaceholderModule"), "PlaceholderModule missing"
    assert hasattr(mod, "lazy_import"), "lazy_import missing"
    assert hasattr(mod, "safe_import"), "safe_import missing"
    assert hasattr(mod, "LazyModuleRegistry"), "LazyModuleRegistry missing"
    assert hasattr(mod, "register_lazy_module"), "register_lazy_module missing"
    assert hasattr(mod, "get_lazy_module"), "get_lazy_module missing"
    assert hasattr(mod, "LazyAttribute"), "LazyAttribute missing"
    assert hasattr(mod, "reload_module"), "reload_module missing"
    assert hasattr(mod, "unload_module"), "unload_module missing"
    assert hasattr(mod, "is_module_available"), "is_module_available missing"
    assert hasattr(mod, "get_module_version"), "get_module_version missing"
    assert hasattr(mod, "require_module"), "require_module missing"

