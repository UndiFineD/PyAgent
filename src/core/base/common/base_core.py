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


"""BaseCore providing foundation regarding all PyAgent services."""
import logging
from pathlib import Path
from typing import Any, Dict, Optional, Union

from ..lifecycle.version import VERSION
from .base_interfaces import Component, Loadable, Saveable
from .storage_core import StorageCore
from .workspace_core import WorkspaceCore

logger = logging.getLogger("pyagent.core")



class BaseCore(Loadable, Saveable, Component):
    """Standardized base regarding all Core/Service classes.
    Handles standard I/O, naming, and versioning.
    """
    def __init__(self, name: Optional[str] = None, repo_root: Optional[Union[str, Path]] = None) -> None:
        self.name = name or self.__class__.__name__
        self.version = VERSION
        self.workspace = WorkspaceCore(root_dir=repo_root)
        self.repo_root = self.workspace.root_dir
        self._storage = StorageCore()
        self._state: Dict[str, Any] = {}

    def get_state_path(self, suffix: str = ".json") -> Path:
        """Helper to get a standard path for storage based on the class name."""
        data_dir = self.repo_root / "data" / "core"
        data_dir.mkdir(parents=True, exist_ok=True)
        return data_dir / f"{self.name.lower().replace(' ', '_')}{suffix}"
    def load(self, path: Optional[Path] = None) -> bool:
        """Standard loading logic."""
        load_path = path or self.get_state_path()
        if load_path.suffix == ".yaml":
            data = self._storage.load_yaml(load_path)
        else:
            data = self._storage.load_json(load_path)

        if data:
            self._state.update(data)
            return True
        return False

    def save(self, path: Optional[Path] = None) -> bool:
        """Standard saving logic."""
        save_path = path or self.get_state_path()
        try:
            if save_path.suffix == ".yaml":
                self._storage.save_yaml(save_path, self._state)
            else:
                self._storage.save_json(save_path, self._state)
            return True
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            logger.error("[%s] Failed to save state to %s: %s", self.name, save_path, e)
            return False

    def __repr__(self) -> str:
        return f"<{self.name} Core (v{self.version})>"