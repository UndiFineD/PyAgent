# Class Breakdown: output_processor

**File**: `src\infrastructure\engine\output_processor.py`  
**Classes**: 15

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `EventType`

**Line**: 36  
**Inherits**: Enum  
**Methods**: 0

Types of request events.

[TIP] **Suggested split**: Move to `eventtype.py`

---

### 2. `RequestEvent`

**Line**: 48  
**Methods**: 0

An event in request lifecycle.

[TIP] **Suggested split**: Move to `requestevent.py`

---

### 3. `LoRARequest`

**Line**: 57  
**Methods**: 0

LoRA adapter request information.

[TIP] **Suggested split**: Move to `lorarequest.py`

---

### 4. `ParentRequest`

**Line**: 66  
**Methods**: 0

Parent request for multi-turn conversations.

[TIP] **Suggested split**: Move to `parentrequest.py`

---

### 5. `SamplingParams`

**Line**: 74  
**Methods**: 0

Parameters for token sampling.

[TIP] **Suggested split**: Move to `samplingparams.py`

---

### 6. `EngineCoreRequest`

**Line**: 88  
**Methods**: 0

Request to be processed by engine core.

[TIP] **Suggested split**: Move to `enginecorerequest.py`

---

### 7. `EngineCoreOutput`

**Line**: 106  
**Methods**: 0

Output from engine core for a single request.

[TIP] **Suggested split**: Move to `enginecoreoutput.py`

---

### 8. `EngineCoreOutputs`

**Line**: 120  
**Methods**: 0

Batch of outputs from engine core.

[TIP] **Suggested split**: Move to `enginecoreoutputs.py`

---

### 9. `RequestOutput`

**Line**: 129  
**Methods**: 0

Final output for a request (to be returned to client).

[TIP] **Suggested split**: Move to `requestoutput.py`

---

### 10. `OutputProcessorOutput`

**Line**: 141  
**Methods**: 0

Output from OutputProcessor.process_outputs().

[TIP] **Suggested split**: Move to `outputprocessoroutput.py`

---

### 11. `RequestOutputCollector`

**Line**: 148  
**Methods**: 3

Queue for collecting request outputs.

[TIP] **Suggested split**: Move to `requestoutputcollector.py`

---

### 12. `RequestState`

**Line**: 170  
**Methods**: 7

Per-request state tracking.

Manages detokenization state, output accumulation, and streaming.

[TIP] **Suggested split**: Move to `requeststate.py`

---

### 13. `LoRARequestStates`

**Line**: 312  
**Methods**: 4

Track LoRA request states.

[TIP] **Suggested split**: Move to `lorarequeststates.py`

---

### 14. `OutputProcessor`

**Line**: 337  
**Methods**: 8

Process EngineCoreOutputs into RequestOutputs.

Manages per-request state, detokenization, and output streaming.

[TIP] **Suggested split**: Move to `outputprocessor.py`

---

### 15. `IterationStats`

**Line**: 524  
**Methods**: 2

Statistics for a single iteration.

[TIP] **Suggested split**: Move to `iterationstats.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
