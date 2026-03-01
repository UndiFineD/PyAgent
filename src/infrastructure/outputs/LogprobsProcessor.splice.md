# Class Breakdown: LogprobsProcessor

**File**: `src\infrastructure\outputs\LogprobsProcessor.py`  
**Classes**: 8

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `TokenLogprob`

**Line**: 35  
**Methods**: 1

Single token with its log probability.

[TIP] **Suggested split**: Move to `tokenlogprob.py`

---

### 2. `TopLogprobs`

**Line**: 46  
**Methods**: 1

Top logprobs for a single position.

[TIP] **Suggested split**: Move to `toplogprobs.py`

---

### 3. `LogprobsLists`

**Line**: 90  
**Methods**: 6

List-based logprobs storage (vLLM LogprobsLists equivalent).

Efficient for variable-length sequences with streaming output.

[TIP] **Suggested split**: Move to `logprobslists.py`

---

### 4. `LogprobsTensors`

**Line**: 139  
**Methods**: 3

Tensor-based logprobs storage (vLLM LogprobsTensors equivalent).

Efficient for batched processing with GPU tensors.

Beyond vLLM:
- Double buffering for async CPU transfer
- Sparse storage for memory...

[TIP] **Suggested split**: Move to `logprobstensors.py`

---

### 5. `AsyncCPUTransfer`

**Line**: 269  
**Methods**: 4

Async CPU transfer manager for GPU tensors.

Beyond vLLM: Double buffering and pipelining for overlap.

[TIP] **Suggested split**: Move to `asynccputransfer.py`

---

### 6. `SamplerOutput`

**Line**: 319  
**Methods**: 2

Output from the sampler (vLLM SamplerOutput equivalent).

Contains sampled tokens and optional logprobs.

[TIP] **Suggested split**: Move to `sampleroutput.py`

---

### 7. `ModelRunnerOutput`

**Line**: 353  
**Methods**: 2

Output from model runner (vLLM ModelRunnerOutput equivalent).

Contains all outputs from a single forward pass.

[TIP] **Suggested split**: Move to `modelrunneroutput.py`

---

### 8. `StreamingLogprobsCollector`

**Line**: 415  
**Methods**: 7

Collector for streaming logprobs.

Beyond vLLM: Supports real-time streaming with backpressure.

[TIP] **Suggested split**: Move to `streaminglogprobscollector.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
