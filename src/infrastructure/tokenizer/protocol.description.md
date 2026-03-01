# protocol

**File**: `src\infrastructure\tokenizer\protocol.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 58  
**Complexity**: 7 (moderate)

## Overview

Tokenizer protocols.

## Classes (1)

### `TokenizerProtocol`

**Inherits from**: Protocol

Protocol for tokenizer implementations.

**Methods** (7):
- `vocab_size(self)`
- `bos_token_id(self)`
- `eos_token_id(self)`
- `pad_token_id(self)`
- `encode(self, text, add_special_tokens)`
- `decode(self, token_ids, skip_special_tokens)`
- `batch_encode(self, texts, add_special_tokens)`

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `typing.List`
- `typing.Optional`
- `typing.Protocol`
- `typing.Sequence`
- `typing.runtime_checkable`

---
*Auto-generated documentation*
