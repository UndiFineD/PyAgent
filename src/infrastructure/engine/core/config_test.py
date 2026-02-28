# Auto-synced test for infrastructure/engine/core/config.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "config.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "RequestStatus"), "RequestStatus missing"
    assert hasattr(mod, "FinishReason"), "FinishReason missing"
    assert hasattr(mod, "Request"), "Request missing"
    assert hasattr(mod, "SchedulerOutput"), "SchedulerOutput missing"
    assert hasattr(mod, "ModelRunnerOutput"), "ModelRunnerOutput missing"
    assert hasattr(mod, "EngineCoreOutput"), "EngineCoreOutput missing"
    assert hasattr(mod, "EngineCoreOutputs"), "EngineCoreOutputs missing"

