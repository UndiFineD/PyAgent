# Auto-synced test for core/base/common/multimodal_core.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "multimodal_core.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "StreamState"), "StreamState missing"
    assert hasattr(mod, "TemporalModalityBuffer"), "TemporalModalityBuffer missing"
    assert hasattr(mod, "StreamingVisionEncoder"), "StreamingVisionEncoder missing"
    assert hasattr(mod, "StreamingAudioProcessor"), "StreamingAudioProcessor missing"
    assert hasattr(mod, "MultimodalCore"), "MultimodalCore missing"
    assert hasattr(mod, "MultimodalStreamSession"), "MultimodalStreamSession missing"

