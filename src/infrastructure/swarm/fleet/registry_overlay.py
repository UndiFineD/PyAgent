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


from __future__ import annotations
from src.core.base.lifecycle.version import VERSION
import json
import logging
from typing import Any
from pathlib import Path

__version__ = VERSION


class RegistryOverlay:
    """
    RegistryOverlay handles dynamic overrides for bootstrap configurations.
    It allows the fleet to update its core agent map without modifying source code.
    """

    def __init__(self, overlay_path: Path | None = None) -> None:
        if overlay_path is None:
            # Default to agent_store/registry_overlay.json
            self.overlay_path = Path("data/memory/agent_store/registry_overlay.json")
        else:
            self.overlay_path = overlay_path

        self.overrides: dict[str, Any] = {}
        self._load_overlay()

    def _load_overlay(self) -> None:
        """Loads overrides from the JSON file."""
        if not self.overlay_path.exists():
            return

        try:
            with open(self.overlay_path, encoding="utf-8") as f:
                data = json.load(f)
                self.overrides = data.get("agents", {})
                logging.info(
                    f"RegistryOverlay: Loaded {len(self.overrides)} overrides from {self.overlay_path}"
                )
        except Exception as e:
            logging.error(f"RegistryOverlay: Failed to load overlay: {e}")

    def get_agent_config(
        self, agent_id: str, default: tuple[str, str, Any]
    ) -> tuple[str, str, Any]:
        """Returns the overridden config or the default."""
        if agent_id in self.overrides:
            override = self.overrides[agent_id]
            # Expected format in JSON: [module, class, params]
            if isinstance(override, list) and len(override) >= 2:
                logging.info(f"RegistryOverlay: Applying override for '{agent_id}'")
                return (
                    override[0],
                    override[1],
                    override[2] if len(override) > 2 else None,
                )
        return default

    def save_override(
        self, agent_id: str, module_path: str, class_name: str, params: Any = None
    ) -> None:
        """Saves a new override to the overlay file."""
        self.overrides[agent_id] = [module_path, class_name, params]

        self.overlay_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with open(self.overlay_path, "w", encoding="utf-8") as f:
                json.dump({"agents": self.overrides}, f, indent=4)
        except Exception as e:
            logging.error(f"RegistryOverlay: Failed to save overlay: {e}")
