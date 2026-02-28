# Auto-synced test for infrastructure/engine/chat_templates/chat_template_registry.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "chat_template_registry.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "TemplateType"), "TemplateType missing"
    assert hasattr(mod, "TemplateConfig"), "TemplateConfig missing"
    assert hasattr(mod, "TemplateInfo"), "TemplateInfo missing"
    assert hasattr(mod, "RenderOptions"), "RenderOptions missing"
    assert hasattr(mod, "ModelType"), "ModelType missing"
    assert hasattr(mod, "MODEL_TEMPLATE_MAP"), "MODEL_TEMPLATE_MAP missing"
    assert hasattr(mod, "DEFAULT_CONFIG"), "DEFAULT_CONFIG missing"
    assert hasattr(mod, "ChatTemplate"), "ChatTemplate missing"
    assert hasattr(mod, "JinjaTemplate"), "JinjaTemplate missing"
    assert hasattr(mod, "ChatTemplateRegistry"), "ChatTemplateRegistry missing"
    assert hasattr(mod, "TemplateResolver"), "TemplateResolver missing"
    assert hasattr(mod, "register_template"), "register_template missing"
    assert hasattr(mod, "get_template"), "get_template missing"
    assert hasattr(mod, "render_template"), "render_template missing"
    assert hasattr(mod, "detect_template_type"), "detect_template_type missing"

