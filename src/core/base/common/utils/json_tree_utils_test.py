# Auto-synced test for core/base/common/utils/json_tree_utils.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "json_tree_utils.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "JSONTree"), "JSONTree missing"
    assert hasattr(mod, "json_iter_leaves"), "json_iter_leaves missing"
    assert hasattr(mod, "json_iter_leaves_with_path"), "json_iter_leaves_with_path missing"
    assert hasattr(mod, "json_iter_leaves_fast"), "json_iter_leaves_fast missing"
    assert hasattr(mod, "json_map_leaves"), "json_map_leaves missing"
    assert hasattr(mod, "json_map_leaves_async"), "json_map_leaves_async missing"
    assert hasattr(mod, "json_reduce_leaves"), "json_reduce_leaves missing"
    assert hasattr(mod, "json_count_leaves"), "json_count_leaves missing"
    assert hasattr(mod, "json_count_leaves_fast"), "json_count_leaves_fast missing"
    assert hasattr(mod, "json_depth"), "json_depth missing"
    assert hasattr(mod, "json_flatten"), "json_flatten missing"
    assert hasattr(mod, "json_flatten_fast"), "json_flatten_fast missing"
    assert hasattr(mod, "json_unflatten"), "json_unflatten missing"
    assert hasattr(mod, "json_get_path"), "json_get_path missing"
    assert hasattr(mod, "json_set_path"), "json_set_path missing"
    assert hasattr(mod, "json_filter_leaves"), "json_filter_leaves missing"
    assert hasattr(mod, "json_validate_leaves"), "json_validate_leaves missing"
    assert hasattr(mod, "json_find_leaves"), "json_find_leaves missing"
    assert hasattr(mod, "RUST_ACCELERATION_AVAILABLE"), "RUST_ACCELERATION_AVAILABLE missing"

