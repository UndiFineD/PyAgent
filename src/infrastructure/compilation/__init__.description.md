# __init__

**File**: `src\infrastructure\compilation\__init__.py`  
**Type**: Python Module  
**Summary**: 0 classes, 0 functions, 13 imports  
**Lines**: 44  
**Complexity**: 0 (simple)

## Overview

Compilation Infrastructure.

Phase 36: torch.compile integration providing:
- TorchCompileIntegration: torch.compile wrapper
- CompilationCounter: Compilation metrics

Beyond vLLM:
- Profile-guided compilation
- Incremental compilation
- Hybrid strategies

## Dependencies

**Imports** (13):
- `TorchCompileIntegration.CompilationCounter`
- `TorchCompileIntegration.CompileBackend`
- `TorchCompileIntegration.CompileConfig`
- `TorchCompileIntegration.CompileMode`
- `TorchCompileIntegration.CompileStats`
- `TorchCompileIntegration.CompilerInterface`
- `TorchCompileIntegration.IncrementalCompiler`
- `TorchCompileIntegration.ProfileGuidedCompiler`
- `TorchCompileIntegration.TorchCompiler`
- `TorchCompileIntegration.compile_fn`
- `TorchCompileIntegration.get_compile_config`
- `TorchCompileIntegration.set_compile_enabled`
- `TorchCompileIntegration.with_compiler_context`

---
*Auto-generated documentation*
