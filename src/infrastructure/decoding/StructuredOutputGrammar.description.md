# StructuredOutputGrammar

**File**: `src\infrastructure\decoding\StructuredOutputGrammar.py`  
**Type**: Python Module  
**Summary**: 0 classes, 0 functions, 12 imports  
**Lines**: 38  
**Complexity**: 0 (simple)

## Overview

StructuredOutputGrammar - Grammar-constrained decoding infrastructure.

Inspired by vLLM's v1/structured_output/ backends (xgrammar, guidance, outlines).
Provides JSON schema, regex, choice, and EBNF grammar constraints for LLM outputs.

## Dependencies

**Imports** (12):
- `grammar.ChoiceGrammar`
- `grammar.EBNFGrammar`
- `grammar.GrammarCompiler`
- `grammar.GrammarRule`
- `grammar.JSONSchemaGrammar`
- `grammar.RegexGrammar`
- `grammar.StructuredOutputGrammar`
- `grammar.StructuredOutputManager`
- `grammar.StructuredOutputOptions`
- `grammar.StructuredOutputsParams`
- `grammar.compile_grammar`
- `grammar.validate_structured_output_params`

---
*Auto-generated documentation*
