def test_import_ecosystem_populator():
    import importlib.util
    from pathlib import Path

    p = Path("src/tools/mcp/ecosystem_populator.py")
    spec = importlib.util.spec_from_file_location("mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    if spec.loader:
        spec.loader.exec_module(mod)
    assert hasattr(mod, "get_expanded_ecosystem")
