# __init__

**File**: `src\infrastructure\tokenizer\__init__.py`  
**Type**: Python Module  
**Summary**: 0 classes, 0 functions, 15 imports  
**Lines**: 66  
**Complexity**: 0 (simple)

## Overview

Tokenizer management with multi-backend support.

This package provides:
- Protocol-based tokenizer abstraction
- Multi-backend support (HuggingFace, Mistral, Tiktoken)
- LRU caching for tokenizer reuse
- Async tokenization support

## Dependencies

**Imports** (15):
- `TokenizerRegistry.BaseTokenizer`
- `TokenizerRegistry.HuggingFaceTokenizer`
- `TokenizerRegistry.MistralTokenizer`
- `TokenizerRegistry.SpecialTokenHandling`
- `TokenizerRegistry.TiktokenTokenizer`
- `TokenizerRegistry.TokenizeResult`
- `TokenizerRegistry.TokenizerBackend`
- `TokenizerRegistry.TokenizerConfig`
- `TokenizerRegistry.TokenizerInfo`
- `TokenizerRegistry.TokenizerPool`
- `TokenizerRegistry.TokenizerProtocol`
- `TokenizerRegistry.TokenizerRegistry`
- `TokenizerRegistry.create_tokenizer`
- `TokenizerRegistry.estimate_token_count`
- `TokenizerRegistry.get_tokenizer`

---
*Auto-generated documentation*
