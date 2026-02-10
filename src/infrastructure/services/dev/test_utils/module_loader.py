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


"""Module loading utilities for test environment."""

from __future__ import annotations

import importlib.util
import logging
import re
import sys
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from types import ModuleType

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class ModuleLoader:
    """Handles dynamic loading of agent modules and sys.path management."""

    def __init__(self, agent_dir: Path | None = None) -> None:
        """Initialize with project root (containing src)."""
        # Search for project root by looking for 'src' folder
        current = Path(__file__).resolve()
        root_found = None
        for parent in current.parents:
            if (parent / "src").is_dir() and (parent / "tests").is_dir():
                root_found = parent
                break
        self.agent_dir = agent_dir or root_found or current.parents[5]
        self.src_dir = self.agent_dir / "src"

    @contextmanager
    def agent_dir_on_path(self) -> Iterator[None]:
        """Temporarily add the project root to sys.path."""
        old_sys_path = list(sys.path)
        path_str = str(self.agent_dir)
        if path_str not in sys.path:
            sys.path.insert(0, path_str)
        try:
            yield
        finally:
            sys.path[:] = old_sys_path

    @contextmanager
    def agent_sys_path(self) -> Iterator[None]:
        """Add scripts/agent to sys.path temporarily."""
        path = str(self.agent_dir)
        if path not in sys.path:
            sys.path.insert(0, path)
            try:
                yield
            finally:
                sys.path.remove(path)
        else:
            yield

    def load_module_from_path(self, name: str, path: Path) -> ModuleType:
        """Load a module from a specific path."""
        logging.debug(f"Loading module {name} from {path}")
        spec = importlib.util.spec_from_file_location(name, str(path))
        if spec is None or spec.loader is None:
            logging.error(f"Could not load module {name} from {path}")
            raise ImportError(f"Could not load module {name} from {path}")
        mod = importlib.util.module_from_spec(spec)
        sys.modules[name] = mod
        spec.loader.exec_module(mod)
        return mod

    def load_agent_module(self, filename: str, module_name: str | None = None) -> ModuleType:
        """Load an agent module from scripts/agent by filename."""
        path = self.agent_dir / filename
        if not path.exists():
            raise FileNotFoundError(path)
        if module_name is None:
            safe = re.sub(r"[^0-9a-zA-Z_]+", "_", path.stem)
            if not safe or safe[0].isdigit():
                safe = f"m_{safe}"
            module_name = f"_dv_legacy_{safe}"

        try:
            return self.load_module_from_path(module_name, path)
        except Exception:  # pylint: disable=broad-exception-caught
            # Clean up if execution fails
            sys.modules.pop(module_name, None)
            raise

    def get_base_agent_module(self) -> ModuleType:
        """Load base_agent module without modifying sys.path."""
        return self.load_agent_module("base_agent.py", "base_agent")
