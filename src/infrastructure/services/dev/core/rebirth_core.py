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
Core logic for Swarm Rebirth (Phase 180).
Handles mass directory scaffolding and cleanup.
"""

import os
import shutil
from typing import Any

import yaml


class RebirthCore:
    """Pure logic core for swarm rebirth processes, handling project scaffolding."""

    @staticmethod
    def scaffold_structure(root_dir: str, structure: dict[str, Any]) -> int:
        """
        Recursively creates a directory structure from a dictionary.
        Returns the number of directories created.
        """
        count = 0
        for name, sub in structure.items():
            path = os.path.join(root_dir, name)
            if isinstance(sub, dict):
                os.makedirs(path, exist_ok=True)
                count += 1
                count += RebirthCore.scaffold_structure(path, sub)
            elif isinstance(sub, list):
                os.makedirs(path, exist_ok=True)
                count += 1
                for item in sub:
                    # Create empty files for list items
                    open(os.path.join(path, item), "a").close()
        return count

    @staticmethod
    def purge_pycache(root_dir: str) -> None:
        """
        Forcefully removes all __pycache__ folders.
        """
        for root, dirs, _ in os.walk(root_dir):
            if "__pycache__" in dirs:
                shutil.rmtree(os.path.join(root, "__pycache__"))
                dirs.remove("__pycache__")

    @staticmethod
    def parse_manifest(manifest_path: str) -> dict[str, Any]:
        """
        Parses the rebirth manifest.yaml.
        """
        if not os.path.exists(manifest_path):
            return {}
        with open(manifest_path, encoding="utf-8") as f:
            return yaml.safe_load(f)
