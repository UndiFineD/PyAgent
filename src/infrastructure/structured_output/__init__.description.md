# __init__

**File**: `src\infrastructure\structured_output\__init__.py`  
**Type**: Python Module  
**Summary**: 0 classes, 0 functions, 37 imports  
**Lines**: 108  
**Complexity**: 0 (simple)

## Overview

Structured Output Framework for Constrained Generation.

This module provides grammar-based token constraints for:
- JSON Schema validation
- Regex pattern matching
- Grammar specifications (EBNF, Lark)
- Choice constraints
- Function call validation

## Dependencies

**Imports** (37):
- `src.infrastructure.structured_output.GrammarEngine.ChoiceGrammar`
- `src.infrastructure.structured_output.GrammarEngine.EBNFGrammar`
- `src.infrastructure.structured_output.GrammarEngine.FSMState`
- `src.infrastructure.structured_output.GrammarEngine.GrammarEngine`
- `src.infrastructure.structured_output.GrammarEngine.JsonSchemaGrammar`
- `src.infrastructure.structured_output.GrammarEngine.RegexGrammar`
- `src.infrastructure.structured_output.GrammarEngine.TokenMask`
- `src.infrastructure.structured_output.LogitProcessor.BitmaskLogitProcessor`
- `src.infrastructure.structured_output.LogitProcessor.CompositeLogitProcessor`
- `src.infrastructure.structured_output.LogitProcessor.ConstrainedLogitProcessor`
- `src.infrastructure.structured_output.LogitProcessor.LogitBias`
- `src.infrastructure.structured_output.LogitProcessor.LogitProcessor`
- `src.infrastructure.structured_output.StructuredOutputManager.CompilationResult`
- `src.infrastructure.structured_output.StructuredOutputManager.GrammarSpec`
- `src.infrastructure.structured_output.StructuredOutputManager.GrammarType`
- ... and 22 more

---
*Auto-generated documentation*
