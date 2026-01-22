# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""BaseCore providing foundation for all PyAgent services."""

import logging
from pathlib import Path
from typing import Any, Dict, Optional, Union
from .base_interfaces import Loadable, Saveable, Component
from .storage_core import StorageCore
from .workspace_core import WorkspaceCore
from ..lifecycle.version import VERSION

logger = logging.getLogger("pyagent.core")

class BaseCore(Loadable, Saveable, Component):
    """
    Standardized base for all Core/Service classes.
    Handles standard I/O, naming, and versioning.
    """
    def __init__(self, name: Optional[str] = None, repo_root: Optional[Union[str, Path]] = None):
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
        except Exception as e: # pylint: disable=broad-exception-caught
            logger.error(f"[{self.name}] Failed to save state to {save_path}: {e}")
            return False

    def __repr__(self) -> str:
        return f"<{self.name} Core (v{self.version})>"
