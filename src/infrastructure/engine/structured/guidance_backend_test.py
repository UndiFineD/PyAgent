# Auto-synced test for infrastructure/engine/structured/guidance_backend.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "guidance_backend.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "GuidanceTemplateType"), "GuidanceTemplateType missing"
    assert hasattr(mod, "GuidanceVariable"), "GuidanceVariable missing"
    assert hasattr(mod, "GuidanceTemplate"), "GuidanceTemplate missing"
    assert hasattr(mod, "GuidanceState"), "GuidanceState missing"
    assert hasattr(mod, "CompiledGuidanceProgram"), "CompiledGuidanceProgram missing"
    assert hasattr(mod, "GuidanceGrammar"), "GuidanceGrammar missing"
    assert hasattr(mod, "GuidanceBackend"), "GuidanceBackend missing"
    assert hasattr(mod, "AsyncGuidanceBackend"), "AsyncGuidanceBackend missing"

