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
# ContextAgent - Context description authoring and RAG routing

# DATE: 2026-02-13
# AUTHOR: Keimpe de Jong
USAGE:
- Instantiate with a Path or filename pointing at a `.description.md` file: ContextAgent("path/to/file.description.md")
- Use route_query(query) to find relevant RAG shards for a query.
- Read/write the .description.md file content via the agent's BaseAgent APIs and use mixin methods to manage templates, tags, versions, validation, annotations, categorization and RAG operations.

WHAT IT DOES:
- Provides an orchestrating agent that updates and manages code/file description documents (.description.md) using multiple context-related mixins and a local RAG core.
- Routes natural-language queries to the best vector shards, derives the source file corresponding to a description file, and initializes configurable templates, tags, versions, validation rules, annotations, priority, category, and metadata.
- Warns if the filename doesn't follow the expected `.description.md` pattern and attempts to locate the original source file by checking configured extensions.

WHAT IT SHOULD DO BETTER:
- More robust extension and filename handling (config-driven suffixes and stricter validation) and clearer error semantics when the source file cannot be derived.
- Expose and document the mixin APIs and lifecycle hooks (e.g., when templates/tags/versions are mutated) and add unit tests for _derive_source_path and route_query behavior.
- Persist and load compressed content/metadata using the transactional StateTransaction API and add configurability for the LocalRAGCore (persistence, shard limits, routing heuristics).

FILE CONTENT SUMMARY:
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

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.core.base.lifecycle.version import VERSION
from src.core.base.lifecycle.base_agent import BaseAgent
from src.logic.agents.cognitive.core.local_rag_core import LocalRAGCore, RAGShard
from src.logic.agents.cognitive.context.models.context_priority import ContextPriority
from src.logic.agents.cognitive.context.models.file_category import FileCategory

from src.logic.agents.cognitive.context_template_mixin import ContextTemplateMixin, DEFAULT_TEMPLATES
from src.logic.agents.cognitive.context_tagging_mixin import ContextTaggingMixin
from src.logic.agents.cognitive.context_versioning_mixin import ContextVersioningMixin
from src.logic.agents.cognitive.context_validation_mixin import ContextValidationMixin, DEFAULT_VALIDATION_RULES
from src.logic.agents.cognitive.context_annotation_mixin import ContextAnnotationMixin
from src.logic.agents.cognitive.context_categorization_mixin import ContextCategorizationMixin
from src.logic.agents.cognitive.context_rag_mixin import ContextRAGMixin

__version__ = VERSION


# pylint: disable=too-many-ancestors
class ContextAgent(
    BaseAgent,
    ContextTemplateMixin,
    ContextTaggingMixin,
    ContextVersioningMixin,
    ContextValidationMixin,
    ContextAnnotationMixin,
    ContextCategorizationMixin,
    ContextRAGMixin,
):
#     "Updates code file context descriptions using AI assistance.

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.rag_core = LocalRAGCore()
        self.rag_shards: list[RAGShard] = []

        # Configuration
        self.config = {
            "extensions": [
                ".py",
                ".js",
                ".ts",
                ".go",
                ".rs",
                ".java",
                ".sh",
                ".json",
                ".yaml",
                ".yml",
                ".toml",
                ".ini",
                ".cfg",
                ".md",
                ".rst",
                ".txt",
            ]
        }

        self._validate_file_extension()
        self.source_path = self._derive_source_path()

        # New features initialized from defaults
        self._templates: Dict[str, Any] = dict(DEFAULT_TEMPLATES)
        self._tags: Dict[str, str] = {}
        self._versions: List[str] = []
        self._validation_rules: List[str] = list(DEFAULT_VALIDATION_RULES)
        self._annotations: List[str] = []
        self._priority = ContextPriority.MEDIUM
        self._category = FileCategory.OTHER
        self._compressed_content: Optional[bytes] = None
        self._metadata: Dict[str, Any] = {}

    def route_query(self, query: str) -> list[str]:
""""Selects the best vector shards based on file path and query sentiment."""
        active_path = str(self.file_path)
        selected = self.rag_core.route_query_to_shards(
            query, active_path, self.rag_shards
        )
        logging.info(fContextAgent: Query '{query}' routed to {len(selected)} shards.")
        return selected

    def _validate_file_extension(self) -> None:
""""Validate that the file has the correct extension."""
        if not self.file_path.name.endswith(".description.md"):
            logging.warning(
#                 fFile {self.file_path.name} does not end with .description.md.
#                 "Context operations may be limited.
            )

    def _derive_source_path(self) -> Path | None:
""""Derive source file path from .description.md filename."""
        if self.file_path.name.endswith(".description.md"):
            stem = self.file_path.name.replace(".description.md", ")
            # Use configurable extensions
            for ext in self.config.get("extensions", []):
#                 source = self.file_path.parent / f"{stem}{ext}
                if source.exists():
                    return source
        return None

    # ========== Core Methods ==========
    def _get_default_content(self) -> str:
""""Return rich, structured template for new descriptions."""
        self.file_path.name.replace(".description.md", ")
        return "# Description: `{filename}`

## Purpose
[One - line purpose statement]

## Key Features
- [Feature 1]
- [Feature 2]

## Usage
```bash
# Example usage

"""
"""

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.core.base.lifecycle.version import VERSION
from src.core.base.lifecycle.base_agent import BaseAgent
from src.logic.agents.cognitive.core.local_rag_core import LocalRAGCore, RAGShard
from src.logic.agents.cognitive.context.models.context_priority import ContextPriority
from src.logic.agents.cognitive.context.models.file_category import FileCategory

from src.logic.agents.cognitive.context_template_mixin import ContextTemplateMixin, DEFAULT_TEMPLATES
from src.logic.agents.cognitive.context_tagging_mixin import ContextTaggingMixin
from src.logic.agents.cognitive.context_versioning_mixin import ContextVersioningMixin
from src.logic.agents.cognitive.context_validation_mixin import ContextValidationMixin, DEFAULT_VALIDATION_RULES
from src.logic.agents.cognitive.context_annotation_mixin import ContextAnnotationMixin
from src.logic.agents.cognitive.context_categorization_mixin import ContextCategorizationMixin
from src.logic.agents.cognitive.context_rag_mixin import ContextRAGMixin

__version__ = VERSION


# pylint: disable=too-many-ancestors
