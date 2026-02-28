# Auto-synced test for rust_core.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "rust_core.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "extract_graph_entities_regex"), "extract_graph_entities_regex missing"
    assert hasattr(mod, "build_graph_edges_rust"), "build_graph_edges_rust missing"

