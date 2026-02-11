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

"""
Module: manifest_repository
Manages the storage and retrieval of Logic Manifests for the swarm.
"""

from __future__ import annotations
import json
import logging
from pathlib import Path
from typing import Dict

from src.core.base.lifecycle.logic_manifest import LogicManifest

logger = logging.getLogger(__name__)

class ManifestRepository:
    """Repository for managing cognitive shards (Logic Manifests)."""

    def __init__(self, storage_path: str = "data/manifests") -> None:
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self._cache: Dict[str, LogicManifest] = {}

    def save_manifest(self, role: str, manifest: LogicManifest) -> None:
        """Save a manifest to disk."""
        file_path = self.storage_path / f"{role}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(manifest.__dict__, f, indent=4)
        self._cache[role] = manifest

    def get_manifest(self, role: str) -> LogicManifest | None:
        """Retrieve a manifest by role name."""
        if role in self._cache:
            return self._cache[role]

        file_path = self.storage_path / f"{role}.json"
        if not file_path.exists():
            return None

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                manifest = LogicManifest.from_dict(data)
                self._cache[role] = manifest
                return manifest
        except (json.JSONDecodeError, IOError) as e:
            logger.error("Error loading manifest %s: %s", role, e)
            return None

    def list_roles(self) -> list[str]:
        """List all available roles in the repository."""
        return [p.stem for p in self.storage_path.glob("*.json")]
