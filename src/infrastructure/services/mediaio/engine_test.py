# Auto-synced test for infrastructure/services/mediaio/engine.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "engine.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "MediaIOEngine"), "MediaIOEngine missing"
    assert hasattr(mod, "create_media_engine"), "create_media_engine missing"
    assert hasattr(mod, "load_image"), "load_image missing"
    assert hasattr(mod, "load_video"), "load_video missing"
    assert hasattr(mod, "load_audio"), "load_audio missing"

