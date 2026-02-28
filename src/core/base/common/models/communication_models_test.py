# Auto-synced test for core/base/common/models/communication_models.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "communication_models.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "CascadeContext"), "CascadeContext missing"
    assert hasattr(mod, "PromptTemplate"), "PromptTemplate missing"
    assert hasattr(mod, "ConversationMessage"), "ConversationMessage missing"
    assert hasattr(mod, "ConversationHistory"), "ConversationHistory missing"
    assert hasattr(mod, "SpeculativeProposal"), "SpeculativeProposal missing"
    assert hasattr(mod, "VerificationOutcome"), "VerificationOutcome missing"
    assert hasattr(mod, "AsyncSpeculativeToken"), "AsyncSpeculativeToken missing"
    assert hasattr(mod, "PipelineCorrection"), "PipelineCorrection missing"
    assert hasattr(mod, "ExpertProfile"), "ExpertProfile missing"
    assert hasattr(mod, "MoERoutingDecision"), "MoERoutingDecision missing"
    assert hasattr(mod, "SwarmAuditTrail"), "SwarmAuditTrail missing"
    assert hasattr(mod, "ExpertEvaluation"), "ExpertEvaluation missing"
    assert hasattr(mod, "PromptTemplateManager"), "PromptTemplateManager missing"
    assert hasattr(mod, "ResponsePostProcessor"), "ResponsePostProcessor missing"
    assert hasattr(mod, "PromptVersion"), "PromptVersion missing"
    assert hasattr(mod, "BatchRequest"), "BatchRequest missing"
    assert hasattr(mod, "BatchResult"), "BatchResult missing"
    assert hasattr(mod, "MultimodalInput"), "MultimodalInput missing"
    assert hasattr(mod, "ContextWindow"), "ContextWindow missing"
    assert hasattr(mod, "MultimodalBuilder"), "MultimodalBuilder missing"
    assert hasattr(mod, "CachedResult"), "CachedResult missing"
    assert hasattr(mod, "TelemetrySpan"), "TelemetrySpan missing"
    assert hasattr(mod, "SpanContext"), "SpanContext missing"

