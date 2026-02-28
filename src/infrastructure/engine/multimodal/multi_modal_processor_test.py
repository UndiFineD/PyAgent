# Auto-synced test for infrastructure/engine/multimodal/multi_modal_processor.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "multi_modal_processor.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "ModalityType"), "ModalityType missing"
    assert hasattr(mod, "MultiModalConfig"), "MultiModalConfig missing"
    assert hasattr(mod, "PlaceholderInfo"), "PlaceholderInfo missing"
    assert hasattr(mod, "MultiModalData"), "MultiModalData missing"
    assert hasattr(mod, "MultiModalInputs"), "MultiModalInputs missing"
    assert hasattr(mod, "BaseMultiModalProcessor"), "BaseMultiModalProcessor missing"
    assert hasattr(mod, "ImageProcessor"), "ImageProcessor missing"
    assert hasattr(mod, "VideoProcessor"), "VideoProcessor missing"
    assert hasattr(mod, "AudioProcessor"), "AudioProcessor missing"
    assert hasattr(mod, "TextEmbedProcessor"), "TextEmbedProcessor missing"
    assert hasattr(mod, "MultiModalRegistry"), "MultiModalRegistry missing"
    assert hasattr(mod, "MULTIMODAL_REGISTRY"), "MULTIMODAL_REGISTRY missing"
    assert hasattr(mod, "process_multimodal_inputs"), "process_multimodal_inputs missing"
    assert hasattr(mod, "get_placeholder_tokens"), "get_placeholder_tokens missing"

