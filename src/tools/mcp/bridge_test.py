def test_import_bridge():
    """Minimal import sanity test for `src/tools/mcp/bridge.py`."""
    import importlib.util
    from pathlib import Path

    p = Path("src/tools/mcp/bridge.py")
    spec = importlib.util.spec_from_file_location("mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    if spec.loader:
        spec.loader.exec_module(mod)
    assert hasattr(mod, "__name__")
