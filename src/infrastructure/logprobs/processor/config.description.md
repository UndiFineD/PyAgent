# config

**File**: `src\infrastructure\logprobs\processor\config.py`  
**Type**: Python Module  
**Summary**: 6 classes, 1 functions, 11 imports  
**Lines**: 143  
**Complexity**: 21 (complex)

## Overview

Python module containing implementation for config.

## Classes (6)

### `LogprobFormat`

**Inherits from**: Enum

Logprobs output format.

### `TopLogprob`

Top-k logprob entry for a single token.

**Methods** (2):
- `probability(self)`
- `__lt__(self, other)`

### `LogprobEntry`

Logprob entry for a generated token.

**Methods** (2):
- `probability(self)`
- `entropy(self)`

### `PromptLogprobs`

Logprobs for prompt tokens.

**Methods** (5):
- `__init__(self, token_ids, tokens, logprobs)`
- `__len__(self)`
- `__getitem__(self, index)`
- `mean_logprob(self)`
- `perplexity(self)`

### `SampleLogprobs`

Logprobs for sampled tokens.

**Methods** (9):
- `__len__(self)`
- `__getitem__(self, index)`
- `__iter__(self)`
- `append(self, entry)`
- `token_ids(self)`
- `tokens(self)`
- `logprobs(self)`
- `mean_logprob(self)`
- `perplexity(self)`

### `LogprobsResult`

Complete logprobs result.

**Methods** (2):
- `total_tokens(self)`
- `total_perplexity(self)`

## Functions (1)

### `compute_perplexity(logprobs)`

## Dependencies

**Imports** (11):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `enum.auto`
- `math`
- `typing.Iterator`
- `typing.List`
- `typing.Optional`
- `typing.Sequence`
- `typing.Tuple`

---
*Auto-generated documentation*
