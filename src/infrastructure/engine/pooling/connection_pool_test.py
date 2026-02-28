# Auto-synced test for infrastructure/engine/pooling/connection_pool.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "connection_pool.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "ConnectionState"), "ConnectionState missing"
    assert hasattr(mod, "Closeable"), "Closeable missing"
    assert hasattr(mod, "Pingable"), "Pingable missing"
    assert hasattr(mod, "PoolStats"), "PoolStats missing"
    assert hasattr(mod, "PooledConnection"), "PooledConnection missing"
    assert hasattr(mod, "ConnectionPool"), "ConnectionPool missing"
    assert hasattr(mod, "AsyncConnectionPool"), "AsyncConnectionPool missing"
    assert hasattr(mod, "PooledConnectionManager"), "PooledConnectionManager missing"
    assert hasattr(mod, "MultiHostPool"), "MultiHostPool missing"

