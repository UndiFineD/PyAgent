#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tools package.

Importing this package will register all tools via `tool_registry`. Each tool module
calls `register_tool()` during import.

The recommended entrypoint is `python -m src.tools` (see `__main__.py`).
"""

from __future__ import annotations

import importlib
import logging
import pkgutil

_log = logging.getLogger(__name__)

# Modules excluded from auto-import (not tool providers themselves)
_SKIP = frozenset({"tool_registry", "__main__", "common"})

# Import all modules in this package so they can register themselves.
# Avoid altering __path__; the import system already sets it correctly for this package.
for _finder, _name, _ispkg in pkgutil.iter_modules(__path__):
    if _ispkg:
        continue
    if _name in _SKIP:
        continue
    try:
        importlib.import_module(f"{__name__}.{_name}")
    except Exception as _exc:
        # If a tool fails to import, do not crash on package import.
        # The tool may have optional dependencies; log at DEBUG level only.
        _log.debug("tools: skipped %s — %s", _name, _exc)
