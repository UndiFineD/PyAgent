# Auto-synced test for core/base/common/utils/jsontree/iteration.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "iteration.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "json_iter_leaves"), "json_iter_leaves missing"
    assert hasattr(mod, "json_iter_leaves_with_path"), "json_iter_leaves_with_path missing"

