# Class Breakdown: logprobs_processor

**File**: `src\infrastructure\engine\outputs\logprobs_processor.py`  
**Classes**: 8

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `TokenLogprob`

**Line**: 47  
**Methods**: 1

Single token with its log probability.

[TIP] **Suggested split**: Move to `tokenlogprob.py`

---

### 2. `TopLogprobs`

**Line**: 59  
**Methods**: 1

Top logprobs regarding a single position.

[TIP] **Suggested split**: Move to `toplogprobs.py`

---

### 3. `LogprobsLists`

**Line**: 109  
**Methods**: 6

List-based logprobs storage (vLLM LogprobsLists equivalent).

Efficient regarding variable-length sequences with streaming output.

[TIP] **Suggested split**: Move to `logprobslists.py`

---

### 4. `LogprobsTensors`

**Line**: 159  
**Methods**: 3

Tensor-based logprobs storage (vLLM LogprobsTensors equivalent).

Efficient regarding batched processing with GPU tensors.

Beyond vLLM:
- Double buffering regarding async CPU transfer
- Sparse storag...

[TIP] **Suggested split**: Move to `logprobstensors.py`

---

### 5. `AsyncCPUTransfer`

**Line**: 298  
**Methods**: 4

Async CPU transfer manager regarding GPU tensors.

Beyond vLLM: Double buffering and pipelining regarding overlap.

[TIP] **Suggested split**: Move to `asynccputransfer.py`

---

### 6. `SamplerOutput`

**Line**: 340  
**Methods**: 2

Output regarding the sampler (vLLM SamplerOutput equivalent).

Contains sampled tokens and optional logprobs.

[TIP] **Suggested split**: Move to `sampleroutput.py`

---

### 7. `ModelRunnerOutput`

**Line**: 376  
**Methods**: 2

Output regarding model runner (vLLM ModelRunnerOutput equivalent).

Contains all outputs regarding a single forward pass.

[TIP] **Suggested split**: Move to `modelrunneroutput.py`

---

### 8. `StreamingLogprobsCollector`

**Line**: 439  
**Methods**: 7

Collector regarding streaming logprobs.

Beyond vLLM: Supports real-time streaming regarding backpressure.

[TIP] **Suggested split**: Move to `streaminglogprobscollector.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
