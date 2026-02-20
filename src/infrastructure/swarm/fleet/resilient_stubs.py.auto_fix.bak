#!/usr/bin/env python3
from __future__ import annotations
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


"""
ResilientStub
- Resilient loading stubs for the PyAgent fleet.
- Provides stub objects when plugins fail to load due to missing dependencies.
"""

import importlib
import logging
from collections.abc import Callable
from typing import Any

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


def resilient_import(module_name: str, class_name: str | None = None) -> Any:
    """
    Decorator/Utility to import a module or class resiliently.
    Returns a ResilientStub if the import fails.
    """
    try:
        module = importlib.import_module(module_name)
        if class_name:
            return getattr(module, class_name)

        return module
    except (ImportError, SyntaxError) as e:
        logging.warning(f"ResilientImport: Failed to load '{module_name}'. Returning stub. Error: {e}")
        return ResilientStub(class_name or module_name, str(e))



class ResilientStub:
    """A stub object that logs errors instead of crashing when called."""
    def __init__(self, name: str, error: str) -> None:
        self._name = name
        self._error = error
        logging.error(f"STUB ACTIVE: Component '{name}' failed to load. Reason: {error}")

    def __getattr__(self, name: str) -> Callable:
        def _stub_method(*_args: Any, **_kwargs: Any) -> str:
            msg = f"Cannot call '{name}' on component '{self._name}': it failed to load. Error: {self._error}"
            logging.error(msg)
            return f"ERROR: {msg}"
        return _stub_method

    def __call__(self, *_args: Any, **_kwargs: Any) -> str:
        """Fallback for direct invocation."""
        msg = f"Cannot invoke component '{self._name}': it failed to load. Error: {self._error}"
        logging.error(msg)
        return f"ERROR: {msg}"

    def get_status(self) -> dict[str, Any]:
        """Returns the failure status of the component."""
        return {"status": "failed_to_load", "error": self._error, "name": self._name}

    def execute_task(self, _task: str) -> str:
        """Stub for task execution."""
        return f"ERROR: Component '{self._name}' failed to load. {self._error}"

    def improve_content(self, _prompt: str) -> str:
        """Stub for content improvement."""
        return f"ERROR: Component '{self._name}' failed to load. {self._error}"

    def calculate_metrics(self, *_args: Any, **_kwargs: Any) -> dict[str, Any]:
        """Stub for metrics calculation."""
        return {}
