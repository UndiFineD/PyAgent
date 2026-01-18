"""
Compilation Infrastructure.

Phase 36: torch.compile integration providing:
- TorchCompileIntegration: torch.compile wrapper
- CompilationCounter: Compilation metrics

Beyond vLLM:
- Profile-guided compilation
- Incremental compilation
- Hybrid strategies
"""

from .TorchCompileIntegration import (
    CompileMode,
    CompileBackend,
    CompileConfig,
    CompileStats,
    CompilerInterface,
    TorchCompiler,
    CompilationCounter as CompileCounter,
    IncrementalCompiler,
    ProfileGuidedCompiler,
    compile_fn,
    set_compile_enabled,
    get_compile_config,
    with_compiler_context,
)

__all__ = [
    "CompileMode",
    "CompileBackend",
    "CompileConfig",
    "CompileStats",
    "CompilerInterface",
    "TorchCompiler",
    "CompileCounter",
    "IncrementalCompiler",
    "ProfileGuidedCompiler",
    "compile_fn",
    "set_compile_enabled",
    "get_compile_config",
    "with_compiler_context",
]
