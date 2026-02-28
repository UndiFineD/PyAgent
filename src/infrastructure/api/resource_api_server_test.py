# Auto-synced test for infrastructure/api/resource_api_server.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "resource_api_server.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "health"), "health missing"
    assert hasattr(mod, "vllm_infer"), "vllm_infer missing"
    assert hasattr(mod, "ollama_infer"), "ollama_infer missing"
    assert hasattr(mod, "npu_task"), "npu_task missing"

