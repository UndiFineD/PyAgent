# Auto-synced test for infrastructure/engine/structured/structured_output_orchestrator.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "structured_output_orchestrator.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "StructuredOutputBackendType"), "StructuredOutputBackendType missing"
    assert hasattr(mod, "ConstraintType"), "ConstraintType missing"
    assert hasattr(mod, "GrammarProtocol"), "GrammarProtocol missing"
    assert hasattr(mod, "BackendProtocol"), "BackendProtocol missing"
    assert hasattr(mod, "ConstraintSpec"), "ConstraintSpec missing"
    assert hasattr(mod, "OrchestratorConfig"), "OrchestratorConfig missing"
    assert hasattr(mod, "BackendWrapper"), "BackendWrapper missing"
    assert hasattr(mod, "CompiledGrammarHandle"), "CompiledGrammarHandle missing"
    assert hasattr(mod, "StructuredOutputOrchestrator"), "StructuredOutputOrchestrator missing"
    assert hasattr(mod, "AsyncStructuredOutputOrchestrator"), "AsyncStructuredOutputOrchestrator missing"
    assert hasattr(mod, "BatchProcessor"), "BatchProcessor missing"

