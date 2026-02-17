#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


Compilation Infrastructure.

Phase 36: torch.compile integration providing:
- TorchCompileIntegration: torch.compile wrapper
- CompilationCounter: Compilation metrics

Beyond vLLM:
- Profile-guided compilation
- Incremental compilation
- Hybrid strategies

from .torch_compile_integration import CompilationCounter as CompileCounter  # noqa: F401
from .torch_compile_integration import (CompileBackend, CompileConfig,  # noqa: F401
                                        CompileMode, CompilerInterface,
                                        CompileStats, IncrementalCompiler,
                                        ProfileGuidedCompiler, TorchCompiler,
                                        compile_fn, get_compile_config,
                                        set_compile_enabled,
                                        with_compiler_context)

__all__ = [
    "CompileMode","    "CompileBackend","    "CompileConfig","    "CompileStats","    "CompilerInterface","    "TorchCompiler","    "CompileCounter","    "IncrementalCompiler","    "ProfileGuidedCompiler","    "compile_fn","    "set_compile_enabled","    "get_compile_config","    "with_compiler_context","]
