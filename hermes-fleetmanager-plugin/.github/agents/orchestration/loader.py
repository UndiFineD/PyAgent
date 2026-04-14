from __future__ import annotations

import importlib.util
import inspect
from pathlib import Path
from types import ModuleType
from typing import Any


def load_agent_module(agent_name: str) -> ModuleType:
    """Load a module from the local agents code directory safely.

    Raises FileNotFoundError or ImportError on failure.
    """
    # Load modules from the sibling `code` directory: .github/agents/code
    code_dir = Path(__file__).resolve().parents[1] / "code"
    module_path = code_dir / f"{agent_name}.py"
    if not module_path.exists():
        raise FileNotFoundError(f"No code module found for agent '{agent_name}'")

    module_key = f"agent_runtime_{agent_name.replace('-', '_')}"
    spec = importlib.util.spec_from_file_location(module_key, module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load module spec for {agent_name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def find_agent_class(module: ModuleType) -> type[Any]:
    """Return the first class in module ending with 'Agent'."""
    for _, obj in inspect.getmembers(module, inspect.isclass):
        if obj.__module__ == module.__name__ and obj.__name__.endswith("Agent"):
            return obj
    raise LookupError(f"No *Agent class found in {module.__name__}")
