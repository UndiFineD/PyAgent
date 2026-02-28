# Auto-synced test for infrastructure/compute/compilation/torch_compile_integration.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "torch_compile_integration.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "CompileMode"), "CompileMode missing"
    assert hasattr(mod, "CompileBackend"), "CompileBackend missing"
    assert hasattr(mod, "CompileConfig"), "CompileConfig missing"
    assert hasattr(mod, "CompileStats"), "CompileStats missing"
    assert hasattr(mod, "CompilerInterface"), "CompilerInterface missing"
    assert hasattr(mod, "TorchCompiler"), "TorchCompiler missing"
    assert hasattr(mod, "CompilationCounter"), "CompilationCounter missing"
    assert hasattr(mod, "IncrementalCompiler"), "IncrementalCompiler missing"
    assert hasattr(mod, "ProfileGuidedCompiler"), "ProfileGuidedCompiler missing"
    assert hasattr(mod, "compile_fn"), "compile_fn missing"
    assert hasattr(mod, "set_compile_enabled"), "set_compile_enabled missing"
    assert hasattr(mod, "get_compile_config"), "get_compile_config missing"
    assert hasattr(mod, "with_compiler_context"), "with_compiler_context missing"

