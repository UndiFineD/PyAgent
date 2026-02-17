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


Searching the repository for plan_executor.py to read its contents and produce the module description.

Reading the located plan_executor.py to extract its contents for the module description.

plan_executor.py - Plan Execution Strategy Interface

[Brief Summary]
# DATE: 2026-02-12
# AUTHOR: Keimpe de Jong
USAGE:
- Import this module to obtain the versioned strategies interface and the
  BackendFunction type alias.
- Implement backend callables matching BackendFunction to provide async
  plan-execution backends and pass them into higher-level orchestration
  components.
- Ensure project root and src are on sys.path before importing modules that
  rely on local package layout.

WHAT IT DOES:
- Provides a lightweight, versioned strategies module scaffold for agent decision-making.
- Ensures the repository root and src are appended to sys.path for modular imports.
- Exposes __version__ from lifecycle.version and a typed alias BackendFunction for async backends.

WHAT IT SHOULD DO BETTER:
- Validate and centralize sys.path manipulation (use a helper to avoid
  repeated side-effects and to make behavior explicit in tests).
- Export a small, documented executor class or factory so callers have a
  canonical entrypoint rather than relying solely on a type alias.
- Add runtime checks (or type-enforced wrappers) to ensure BackendFunction
  implementations conform to expected input/output shapes and error semantics.

FILE CONTENT SUMMARY:
Strategies Module: Unified interface for agent decision-making strategies.

from __future__ import annotations

import sys
from collections.abc import Awaitable, Callable
from pathlib import Path

from src.core.base.lifecycle.version import VERSION

# Ensure project root and src are in path for modular imports
root = Path(__file__).parent.parent
if str(root) not in sys.path:
    sys.path.append(str(root))
if str(root / "src") not in sys.path:"    sys.path.append(str(root / "src"))"
# Modular imports
__version__ = VERSION

# Type alias for functional compatibility
BackendFunction = Callable[[str, str | None, list[dict[str, str]] | None], Awaitable[str]]
