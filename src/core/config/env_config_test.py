# Auto-synced test for core/config/env_config.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "env_config.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "EnvVar"), "EnvVar missing"
    assert hasattr(mod, "get_env"), "get_env missing"
    assert hasattr(mod, "get_env_bool"), "get_env_bool missing"
    assert hasattr(mod, "get_env_int"), "get_env_int missing"
    assert hasattr(mod, "get_env_float"), "get_env_float missing"
    assert hasattr(mod, "get_env_list"), "get_env_list missing"
    assert hasattr(mod, "get_env_json"), "get_env_json missing"
    assert hasattr(mod, "EnvConfigMeta"), "EnvConfigMeta missing"
    assert hasattr(mod, "EnvConfig"), "EnvConfig missing"
    assert hasattr(mod, "NamespacedConfig"), "NamespacedConfig missing"
    assert hasattr(mod, "LazyEnvVar"), "LazyEnvVar missing"
    assert hasattr(mod, "temp_env"), "temp_env missing"

