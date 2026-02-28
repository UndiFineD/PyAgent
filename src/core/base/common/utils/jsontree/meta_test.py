# Auto-synced test for core/base/common/utils/jsontree/meta.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "meta.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "json_count_leaves"), "json_count_leaves missing"
    assert hasattr(mod, "json_depth"), "json_depth missing"
    assert hasattr(mod, "json_filter_leaves"), "json_filter_leaves missing"
    assert hasattr(mod, "json_validate_leaves"), "json_validate_leaves missing"
    assert hasattr(mod, "json_find_leaves"), "json_find_leaves missing"

