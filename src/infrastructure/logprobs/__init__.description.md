# __init__

**File**: `src\infrastructure\logprobs\__init__.py`  
**Type**: Python Module  
**Summary**: 0 classes, 0 functions, 13 imports  
**Lines**: 50  
**Complexity**: 0 (simple)

## Overview

Logprobs processing with GC-optimized storage.

Exports:
    - LogprobFormat: Format enum
    - LogprobEntry: Single token logprob
    - FlatLogprobs: GC-optimized flat storage
    - LogprobsProcessor: Processing utilities
    - StreamingLogprobs: Streaming accumulator

## Dependencies

**Imports** (13):
- `LogprobsProcessor.FlatLogprobs`
- `LogprobsProcessor.LogprobEntry`
- `LogprobsProcessor.LogprobFormat`
- `LogprobsProcessor.LogprobsAnalyzer`
- `LogprobsProcessor.LogprobsProcessor`
- `LogprobsProcessor.LogprobsResult`
- `LogprobsProcessor.PromptLogprobs`
- `LogprobsProcessor.SampleLogprobs`
- `LogprobsProcessor.StreamingLogprobs`
- `LogprobsProcessor.TopLogprob`
- `LogprobsProcessor.compute_entropy`
- `LogprobsProcessor.compute_perplexity`
- `LogprobsProcessor.normalize_logprobs`

---
*Auto-generated documentation*
