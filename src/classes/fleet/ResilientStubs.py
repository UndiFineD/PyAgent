#!/usr/bin/env python3

"""
Resilient loading stubs for the PyAgent fleet.
Provides placeholder objects when plugins fail to load due to missing dependencies.
"""

import logging
import importlib
from typing import Any, Dict, List, Optional, Callable

def resilient_import(module_name: str, class_name: Optional[str] = None):
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
    """A placeholder object that logs errors instead of crashing when called."""
    def __init__(self, name: str, error: str) -> None:
        self._name = name
        self._error = error
        logging.error(f"STUB ACTIVE: Component '{name}' failed to load. Reason: {error}")

    def __getattr__(self, name: str):
        def _stub_method(*args, **kwargs):
            msg = f"Cannot call '{name}' on component '{self._name}': it failed to load. Error: {self._error}"
            logging.error(msg)
            return f"ERROR: {msg}"
        return _stub_method

    def __call__(self, *args, **kwargs):
        msg = f"Cannot invoke component '{self._name}': it failed to load. Error: {self._error}"
        logging.error(msg)
        return f"ERROR: {msg}"

    def get_status(self) -> Dict[str, Any]:
        return {"status": "failed_to_load", "error": self._error, "name": self._name}
    
    def execute_task(self, task: str) -> str:
        return f"ERROR: Component '{self._name}' failed to load. {self._error}"

    def improve_content(self, prompt: str) -> str:
        return f"ERROR: Component '{self._name}' failed to load. {self._error}"

    def calculate_metrics(self, *args, **kwargs):
        return {}
