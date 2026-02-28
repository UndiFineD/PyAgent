# Splice: src/core/base/common/models/communication_models.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- CascadeContext
- PromptTemplate
- ConversationMessage
- ConversationHistory
- SpeculativeProposal
- VerificationOutcome
- AsyncSpeculativeToken
- PipelineCorrection
- ExpertProfile
- MoERoutingDecision
- SwarmAuditTrail
- ExpertEvaluation
- PromptTemplateManager
- ResponsePostProcessor
- PromptVersion
- BatchRequest
- BatchResult
- MultimodalInput
- ContextWindow
- MultimodalBuilder
- CachedResult
- TelemetrySpan
- SpanContext

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
