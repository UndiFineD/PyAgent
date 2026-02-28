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
Orchestrator registry core.py module.
"""


from __future__ import annotations

import os
from typing import Any

from src.core.base.lifecycle.version import VERSION

# Rust acceleration
try:
    from rust_core import to_snake_case_rust

    _RUST_ACCEL = True
except ImportError:
    _RUST_ACCEL = False

__version__ = VERSION


class OrchestratorRegistryCore:
    """
    Pure logic core for Orchestrator Registry.
    Handles dynamic discovery of orchestrator classes.
    """

    def __init__(self, current_sdk_version: str) -> None:
        self.sdk_version: str = current_sdk_version

    def process_discovered_files(self, file_paths: list[str]) -> dict[str, tuple[str, str, bool, str | None]]:
        """
        Processes a list of file paths and extracts orchestrator configurations.
        Expects relative paths from workspace root.
        """
        discovered: dict[str, tuple[str, str, bool, str | None]] = {}

        for rel_path in file_paths:
            file = os.path.basename(rel_path)
            if file.endswith(".py") and not file.startswith("__"):
                filename_base: str = file[:-3]

                # Convert filename to likely class name (snake_case -> PascalCase)
                # e.g., "signal_bus_orchestrator" -> "SignalBusOrchestrator"
                class_name = "".join(x.capitalize() for x in filename_base.split("_"))

                # Check for orchestrator-like components (case-insensitive for snake_case filenames)
                search_name = filename_base.lower()
                if any(
                    x.lower() in search_name
                    for x in [
                        "Orchestrator",
                        "Manager",
                        "Selector",
                        "Engine",
                        "Spawner",
                        "Bridge",
                    ]
                ):
                    # Calculate module path
                    module_path: str = rel_path.replace(os.sep, ".").replace(".py", "")

                    # Convert ClassName -> snake_case key
                    # Robust handling for both PascalCase and snake_case (Phase 135)
                    # "SelfHealingOrchestrator" -> "self_healing"
                    # "signal_bus_orchestrator" -> "signal_bus"
                    raw_short = class_name
                    for suffix in ["Orchestrator", "orchestrator", "_orchestrator"]:
                        raw_short = raw_short.replace(suffix, "")

                    short_key: str = self._to_snake_case(raw_short)
                    full_key: str = self._to_snake_case(class_name)

                    # Default heuristic for 'needs_fleet'
                    needs_fleet: bool = any(
                        x.lower() in search_name
                        for x in [
                            "Orchestrator",
                            "Spawner",
                            "Bridge",
                            "Selector",
                            "Engine",
                        ]
                    )

                    # (module, class, needs_fleet, arg_path)
                    cfg = (module_path, class_name, needs_fleet, None)

                    if short_key:
                        discovered[short_key] = cfg
                    discovered[full_key] = cfg
                    discovered[class_name] = cfg  # Also keep original class name for direct access

        return discovered

    def _to_snake_case(self, name: str) -> str:
        # Use Rust acceleration when available (~3x faster)
        if _RUST_ACCEL:
            try:
                return to_snake_case_rust(name)
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                pass
        # Python fallback
        import re

        s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
        return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()

    def parse_manifest(self, raw_manifest: dict[str, Any]) -> dict[str, tuple[str, str, bool, str | None]]:
        """
        Parses the raw manifest dictionary and filters incompatible plugins.
        Returns a dict of {Name: (module, class, needs_fleet, arg_path)}.
        """
        valid_configs: dict[str, tuple[str, str, bool, str | None]] = {}
        for key, cfg in raw_manifest.items():
            # Expecting: "Name": ["module.path", "ClassName", needs_fleet, "arg_path", "min_sdk_version"]
            if isinstance(cfg, list) and len(cfg) >= 2:
                # Version gate
                min_sdk: str = cfg[4] if len(cfg) > 4 else "1.0.0"

                if self.is_compatible(min_sdk):
                    needs_fleet: bool = cfg[2] if len(cfg) > 2 else False
                    arg_path: str | None = cfg[3] if len(cfg) > 3 else None
                    valid_configs[key] = (cfg[0], cfg[1], needs_fleet, arg_path)

        return valid_configs

    def is_compatible(self, required_version: str) -> bool:
        """
        Checks if the current SDK version meets the required version.
        """
        try:
            p_parts = [int(x) for x in self.sdk_version.split(".")]
            r_parts = [int(x) for x in required_version.split(".")]

            # Pad to length 3
            p_parts += [0] * (3 - len(p_parts))
            r_parts += [0] * (3 - len(r_parts))

            if p_parts[0] > r_parts[0]:
                return True
            if p_parts[0] < r_parts[0]:
                return False
            return p_parts[1] >= r_parts[1]
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            return True
