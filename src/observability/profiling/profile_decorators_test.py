# Auto-synced test for observability/profiling/profile_decorators.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "profile_decorators.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "ProfileResult"), "ProfileResult missing"
    assert hasattr(mod, "cprofile_context"), "cprofile_context missing"
    assert hasattr(mod, "cprofile"), "cprofile missing"
    assert hasattr(mod, "timer_context"), "timer_context missing"
    assert hasattr(mod, "timer"), "timer missing"
    assert hasattr(mod, "ProfileAccumulator"), "ProfileAccumulator missing"
    assert hasattr(mod, "track"), "track missing"
    assert hasattr(mod, "get_profile_report"), "get_profile_report missing"
    assert hasattr(mod, "reset_profile_data"), "reset_profile_data missing"

