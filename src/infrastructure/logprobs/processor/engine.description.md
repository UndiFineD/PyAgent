# engine

**File**: `src\infrastructure\logprobs\processor\engine.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 12 imports  
**Lines**: 74  
**Complexity**: 7 (moderate)

## Overview

Python module containing implementation for engine.

## Classes (2)

### `LogprobsProcessor`

Process and extract logprobs from model outputs.

**Methods** (4):
- `__init__(self, top_k, output_format)`
- `process_logits(self, logits, token_ids, tokenizer)`
- `_log_softmax(self, logits)`
- `_decode(self, tid, tokenizer)`

### `StreamingLogprobs`

Streaming logprobs accumulator.

**Methods** (3):
- `__init__(self, top_k, max_tokens)`
- `add_token(self, token_id, logprob, top_k_ids, top_k_logprobs)`
- `finalize(self)`

## Dependencies

**Imports** (12):
- `__future__.annotations`
- `config.LogprobEntry`
- `config.LogprobFormat`
- `config.TopLogprob`
- `math`
- `numpy`
- `storage.FlatLogprobs`
- `threading`
- `typing.Any`
- `typing.List`
- `typing.Optional`
- `typing.Union`

---
*Auto-generated documentation*
