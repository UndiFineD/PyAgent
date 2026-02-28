# Auto-synced test for core/base/common/utils/collection_utils.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "collection_utils.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "LazyDict"), "LazyDict missing"
    assert hasattr(mod, "as_list"), "as_list missing"
    assert hasattr(mod, "as_iter"), "as_iter missing"
    assert hasattr(mod, "is_list_of"), "is_list_of missing"
    assert hasattr(mod, "chunk_list"), "chunk_list missing"
    assert hasattr(mod, "chunk_iter"), "chunk_iter missing"
    assert hasattr(mod, "flatten_2d_lists"), "flatten_2d_lists missing"
    assert hasattr(mod, "flatten_deep"), "flatten_deep missing"
    assert hasattr(mod, "full_groupby"), "full_groupby missing"
    assert hasattr(mod, "partition"), "partition missing"
    assert hasattr(mod, "first"), "first missing"
    assert hasattr(mod, "first_or_raise"), "first_or_raise missing"
    assert hasattr(mod, "last"), "last missing"
    assert hasattr(mod, "swap_dict_values"), "swap_dict_values missing"
    assert hasattr(mod, "deep_merge_dicts"), "deep_merge_dicts missing"
    assert hasattr(mod, "invert_dict"), "invert_dict missing"
    assert hasattr(mod, "invert_dict_multi"), "invert_dict_multi missing"
    assert hasattr(mod, "filter_none"), "filter_none missing"
    assert hasattr(mod, "pick_keys"), "pick_keys missing"
    assert hasattr(mod, "omit_keys"), "omit_keys missing"
    assert hasattr(mod, "unique"), "unique missing"
    assert hasattr(mod, "unique_by"), "unique_by missing"
    assert hasattr(mod, "sliding_window"), "sliding_window missing"
    assert hasattr(mod, "pairwise"), "pairwise missing"

