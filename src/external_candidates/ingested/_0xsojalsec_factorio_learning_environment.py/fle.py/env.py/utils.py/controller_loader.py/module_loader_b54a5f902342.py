# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-factorio-learning-environment\fle\env\utils\controller_loader\module_loader.py
import importlib.util
from typing import Any, Optional


class ModuleLoader:
    """Handles loading Python modules from file paths."""

    @staticmethod
    def from_path(path: str) -> Optional[Any]:
        """Load and return a module from the given path."""
        spec = importlib.util.spec_from_file_location("temp_module", path)
        if not spec or not spec.loader:
            return None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
