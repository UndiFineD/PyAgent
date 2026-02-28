# Auto-synced test for infrastructure/swarm/network/http_client.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "http_client.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "HTTPClient"), "HTTPClient missing"
    assert hasattr(mod, "AsyncHTTPClient"), "AsyncHTTPClient missing"
    assert hasattr(mod, "RetryableHTTPClient"), "RetryableHTTPClient missing"
    assert hasattr(mod, "get_bytes"), "get_bytes missing"
    assert hasattr(mod, "get_text"), "get_text missing"
    assert hasattr(mod, "get_json"), "get_json missing"
    assert hasattr(mod, "async_get_bytes"), "async_get_bytes missing"
    assert hasattr(mod, "async_get_text"), "async_get_text missing"
    assert hasattr(mod, "async_get_json"), "async_get_json missing"
    assert hasattr(mod, "HTTPConnection"), "HTTPConnection missing"
    assert hasattr(mod, "global_http_connection"), "global_http_connection missing"

