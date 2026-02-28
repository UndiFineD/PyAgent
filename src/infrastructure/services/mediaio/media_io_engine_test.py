# Auto-synced test for infrastructure/services/mediaio/media_io_engine.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "media_io_engine.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "AudioData"), "AudioData missing"
    assert hasattr(mod, "AudioFormat"), "AudioFormat missing"
    assert hasattr(mod, "AudioLoader"), "AudioLoader missing"
    assert hasattr(mod, "ImageData"), "ImageData missing"
    assert hasattr(mod, "ImageFormat"), "ImageFormat missing"
    assert hasattr(mod, "ImageLoader"), "ImageLoader missing"
    assert hasattr(mod, "MediaIOEngine"), "MediaIOEngine missing"
    assert hasattr(mod, "MediaLoadConfig"), "MediaLoadConfig missing"
    assert hasattr(mod, "MediaLoader"), "MediaLoader missing"
    assert hasattr(mod, "MediaMetadata"), "MediaMetadata missing"
    assert hasattr(mod, "MediaType"), "MediaType missing"
    assert hasattr(mod, "ResizeMode"), "ResizeMode missing"
    assert hasattr(mod, "VideoData"), "VideoData missing"
    assert hasattr(mod, "VideoFormat"), "VideoFormat missing"
    assert hasattr(mod, "VideoLoader"), "VideoLoader missing"
    assert hasattr(mod, "create_media_engine"), "create_media_engine missing"
    assert hasattr(mod, "load_image"), "load_image missing"
    assert hasattr(mod, "load_video"), "load_video missing"
    assert hasattr(mod, "load_audio"), "load_audio missing"

