#!/usr/bin/env python3
"""Parser-safe minimal `BaseCore` implementation.

This file provides a conservative fallback for the project's BaseCore
so other modules can import successfully while full implementations are
restored incrementally.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional, Union
import logging

logger = logging.getLogger("pyagent.core")


# Try to import project-specific dependencies; fall back to safe shims.
try:
    from ..lifecycle.version import VERSION
except Exception:  # pragma: no cover - fallback
    VERSION = "0.0.0"

try:
    from .base_interfaces import Component, Loadable, Saveable
except Exception:  # pragma: no cover - fallback
    class Component:  # type: ignore[no-redef]
        pass

    class Loadable:  # type: ignore[no-redef]
        def load(self, path: Optional[Path] = None) -> bool:  # pragma: no cover - shim
            return False

    class Saveable:  # type: ignore[no-redef]
        def save(self, path: Optional[Path] = None) -> bool:  # pragma: no cover - shim
            return False

try:
    from .storage_core import StorageCore
except Exception:  # pragma: no cover - fallback
    class StorageCore:  # type: ignore[no-redef]
        def load_json(self, path: Path) -> Dict[str, Any]:
            return {}

        def load_yaml(self, path: Path) -> Dict[str, Any]:
            return {}

        def save_json(self, path: Path, data: Dict[str, Any]) -> None:  # pragma: no cover - shim
            pass

        def save_yaml(self, path: Path, data: Dict[str, Any]) -> None:  # pragma: no cover - shim
            pass

try:
    from .workspace_core import WorkspaceCore
except Exception:  # pragma: no cover - fallback
    class WorkspaceCore:  # type: ignore[no-redef]
        def __init__(self, root_dir: Optional[Union[str, Path]] = None) -> None:  # pragma: no cover
            self.root_dir = Path(root_dir) if root_dir else Path.cwd()


class BaseCore(Loadable, Saveable, Component):
    """Conservative base class for core/service classes.

    Provides basic state load/save, workspace/root handling and a stable
    representation used across the codebase.
    """

    def __init__(self, name: Optional[str] = None, repo_root: Optional[Union[str, Path]] = None) -> None:
        self.name = name or self.__class__.__name__
        self.version = VERSION
        self.workspace = WorkspaceCore(root_dir=repo_root)
        self.repo_root = Path(self.workspace.root_dir)
        self._storage = StorageCore()
        self._state: Dict[str, Any] = {}

    def get_state_path(self, suffix: str = ".json") -> Path:
        data_dir = Path(self.repo_root) / "data" / "core"
        data_dir.mkdir(parents=True, exist_ok=True)
        return data_dir / f"{self.name.lower().replace(' ', '_')}{suffix}"

    def load(self, path: Optional[Path] = None) -> bool:
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
        save_path = path or self.get_state_path()
        try:
            if save_path.suffix == ".yaml":
                self._storage.save_yaml(save_path, self._state)
            else:
                self._storage.save_json(save_path, self._state)
            return True
        except Exception as exc:  # pragma: no cover - conservative handling
            logger.error("[%s] Failed to save state to %s: %s", self.name, save_path, exc)
            return False

    def __repr__(self) -> str:
        return f"<{self.name} Core (v{self.version})>"