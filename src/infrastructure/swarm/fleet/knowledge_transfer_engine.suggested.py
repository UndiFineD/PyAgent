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
KnowledgeTransferEngine
Engine for cross-fleet knowledge transfer.
Enables sharing lessons between decoupled fleet instances.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from src.core.base.lifecycle.version import VERSION

import sys

suggestions_dir = Path(__file__).parent
if str(suggestions_dir) not in sys.path:
    sys.path.insert(0, str(suggestions_dir))

try:
    from knowledge_transfer_core import KnowledgeTransferCore
except ImportError as e:
    logging.error(f"Failed to import KnowledgeTransferCore: {e}")
    raise

__version__ = VERSION


class KnowledgeTransferEngine:
    """
    Manages export and import of knowledge/lessons between fleets.
    Shell for KnowledgeTransferCore.
    """

    def __init__(self, workspace_root: str) -> None:
        self.workspace_root = Path(workspace_root)
        self.export_path = self.workspace_root / "data/memory/knowledge_exports"
        self.export_path.mkdir(parents=True, exist_ok=True)
        self.core = KnowledgeTransferCore()

    def export_knowledge(self, fleet_id: str, knowledge_data: dict[str, Any]) -> str:
        """Exports a fleet's knowledge (lessons, entities) to a shareable file."""
        export_file = self.export_path / f"knowledge_{fleet_id}.json"

        with open(export_file, "w", encoding="utf-8") as f:
            json.dump(knowledge_data, f, indent=2)

        logging.info(f"KnowledgeTransfer: Exported knowledge for {fleet_id} to {export_file}")
        return str(export_file)

    def import_knowledge(self, source_file: str) -> dict[str, Any]:
        """Imports knowledge from an external JSON file."""
        source_path = Path(source_file)
        if not source_path.exists():
            raise FileNotFoundError(f"Knowledge file not found: {source_file}")

        with open(source_path, encoding="utf-8") as f:
            data = json.load(f)

        logging.info(f"KnowledgeTransfer: Imported knowledge from {source_file}")
        return data

    def merge_lessons(self, current_lessons: list[Any], imported_lessons: list[Any]) -> list[Any]:
        """Merges imported lessons into the current set, avoiding duplicates."""
        return self.core.merge_lessons(current_lessons, imported_lessons)
