# Class Breakdown: communication_models

**File**: `src\core\base\common\models\communication_models.py`  
**Classes**: 24

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `WorkState`

**Line**: 34  
**Methods**: 2

Mutable storage regarding intermediate results in a multi-agent pipeline.

[TIP] **Suggested split**: Move to `workstate.py`

---

### 2. `CascadeContext`

**Line**: 50  
**Methods**: 4

Context for tracking cascade operations and preventing infinite recursion.

[TIP] **Suggested split**: Move to `cascadecontext.py`

---

### 3. `PromptTemplate`

**Line**: 136  
**Methods**: 1

reusable prompt template.

[TIP] **Suggested split**: Move to `prompttemplate.py`

---

### 4. `ConversationMessage`

**Line**: 154  
**Methods**: 0

A message in conversation history.

[TIP] **Suggested split**: Move to `conversationmessage.py`

---

### 5. `ConversationHistory`

**Line**: 163  
**Methods**: 2

Manages a conversation history with message storage and retrieval.

[TIP] **Suggested split**: Move to `conversationhistory.py`

---

### 6. `SpeculativeProposal`

**Line**: 179  
**Methods**: 0

Draft proposal from a lower-tier agent to a higher-tier agent (Phase 56).
Used in speculative swarm mode to accelerate decision making.

[TIP] **Suggested split**: Move to `speculativeproposal.py`

---

### 7. `VerificationOutcome`

**Line**: 194  
**Methods**: 0

Outcome of a speculative proposal verification (Phase 56).
Determines if the draft was accepted, rejected, or partially modified.

[TIP] **Suggested split**: Move to `verificationoutcome.py`

---

### 8. `AsyncSpeculativeToken`

**Line**: 210  
**Methods**: 0

A single token yielded by the speculative async pipeline (Phase 60).
Includes a flag indicating if it's a 'draft' or 'verified' token.

[TIP] **Suggested split**: Move to `asyncspeculativetoken.py`

---

### 9. `PipelineCorrection`

**Line**: 223  
**Methods**: 0

signal to roll back and correct the output stream (Phase 60).

[TIP] **Suggested split**: Move to `pipelinecorrection.py`

---

### 10. `ExpertProfile`

**Line**: 234  
**Methods**: 0

Metadata about an agent's expertise for MoE routing (Phase 61).

[TIP] **Suggested split**: Move to `expertprofile.py`

---

### 11. `MoERoutingDecision`

**Line**: 251  
**Methods**: 0

The result of routing a task through the MoE Gatekeeper (Phase 61).

[TIP] **Suggested split**: Move to `moeroutingdecision.py`

---

### 12. `SwarmAuditTrail`

**Line**: 264  
**Methods**: 0

Detailed audit log for swarm decision making (Phase 69).
Tracks routing, fusion, and expert selection reasoning.

[TIP] **Suggested split**: Move to `swarmaudittrail.py`

---

### 13. `ExpertEvaluation`

**Line**: 279  
**Methods**: 0

Feedback evaluation for an expert's performance on a specific task (Phase 68).
Used to drive Expert Specialization Evolution.

[TIP] **Suggested split**: Move to `expertevaluation.py`

---

### 14. `PromptTemplateManager`

**Line**: 294  
**Methods**: 3

Manages a collection of prompt templates.

[TIP] **Suggested split**: Move to `prompttemplatemanager.py`

---

### 15. `ResponsePostProcessor`

**Line**: 310  
**Methods**: 3

Manages post-processing hooks for agent responses.

[TIP] **Suggested split**: Move to `responsepostprocessor.py`

---

### 16. `PromptVersion`

**Line**: 330  
**Methods**: 1

Versioned prompt for A/B testing.

[TIP] **Suggested split**: Move to `promptversion.py`

---

### 17. `BatchRequest`

**Line**: 377  
**Methods**: 4

Request in a batch processing queue.

[TIP] **Suggested split**: Move to `batchrequest.py`

---

### 18. `BatchResult`

**Line**: 412  
**Methods**: 0

Result of a batch processing request.

[TIP] **Suggested split**: Move to `batchresult.py`

---

### 19. `MultimodalInput`

**Line**: 423  
**Methods**: 0

Multimodal input for agents.

[TIP] **Suggested split**: Move to `multimodalinput.py`

---

### 20. `ContextWindow`

**Line**: 433  
**Methods**: 4

Manages token-based context window.

[TIP] **Suggested split**: Move to `contextwindow.py`

---

### 21. `MultimodalBuilder`

**Line**: 465  
**Methods**: 4

Builds multimodal input sets.

[TIP] **Suggested split**: Move to `multimodalbuilder.py`

---

### 22. `CachedResult`

**Line**: 488  
**Methods**: 0

A cached agent result.

[TIP] **Suggested split**: Move to `cachedresult.py`

---

### 23. `TelemetrySpan`

**Line**: 500  
**Methods**: 0

A telemetry span for tracing.

[TIP] **Suggested split**: Move to `telemetryspan.py`

---

### 24. `SpanContext`

**Line**: 513  
**Methods**: 3

Context for a telemetry span.

[TIP] **Suggested split**: Move to `spancontext.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
