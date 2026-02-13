#!/usr/bin/env python3
# Refactored by copilot-placeholder
# Refactored by copilot-placeholder
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
ContextAgent - Context description authoring and RAG routing

[Brief Summary]
DATE: 2026-02-13
AUTHOR: Keimpe de Jong
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


"""
Auto-extracted class from agent_context.py
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
    """Updates code file context descriptions using AI assistance."""

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
        """Selects the best vector shards based on file path and query sentiment."""
        active_path = str(self.file_path)
        selected = self.rag_core.route_query_to_shards(
            query, active_path, self.rag_shards
        )
        logging.info(f"ContextAgent: Query '{query}' routed to {len(selected)} shards.")
        return selected

    def _validate_file_extension(self) -> None:
        """Validate that the file has the correct extension."""
        if not self.file_path.name.endswith(".description.md"):
            logging.warning(
                f"File {self.file_path.name} does not end with .description.md. "
                "Context operations may be limited."
            )

    def _derive_source_path(self) -> Path | None:
        """Derive source file path from .description.md filename."""
        if self.file_path.name.endswith(".description.md"):
            stem = self.file_path.name.replace(".description.md", "")
            # Use configurable extensions
            for ext in self.config.get("extensions", []):
                source = self.file_path.parent / f"{stem}{ext}"
                if source.exists():
                    return source
        return None

    # ========== Core Methods ==========
    def _get_default_content(self) -> str:
        """Return rich, structured template for new descriptions."""
        self.file_path.name.replace(".description.md", "")
        return """# Description: `{filename}`

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
    """Updates code file context descriptions using AI assistance."""

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
        """Selects the best vector shards based on file path and query sentiment."""
        active_path = str(self.file_path)
        selected = self.rag_core.route_query_to_shards(
            query, active_path, self.rag_shards
        )
        logging.info(f"ContextAgent: Query '{query}' routed to {len(selected)} shards.")
        return selected

    def _validate_file_extension(self) -> None:
        """Validate that the file has the correct extension."""
        if not self.file_path.name.endswith(".description.md"):
            logging.warning(
                f"File {self.file_path.name} does not end with .description.md. "
                "Context operations may be limited."
            )

    def _derive_source_path(self) -> Path | None:
        """Derive source file path from .description.md filename."""
        if self.file_path.name.endswith(".description.md"):
            stem = self.file_path.name.replace(".description.md", "")
            # Use configurable extensions
            for ext in self.config.get("extensions", []):
                source = self.file_path.parent / f"{stem}{ext}"
                if source.exists():
                    return source
        return None

    # ========== Core Methods ==========
    def _get_default_content(self) -> str:
        """Return rich, structured template for new descriptions."""
        self.file_path.name.replace(".description.md", "")
        return """# Description: `{filename}`

## Purpose
[One - line purpose statement]

## Key Features
- [Feature 1]
- [Feature 2]

## Usage
```bash
# Example usage
```
"""

    def _get_fallback_response(self) -> str:
        """Return fallback response when Copilot is unavailable."""
        return (
            "# AI Improvement Unavailable\n"
            "# GitHub CLI not found. Install from https://cli.github.com/\n\n"
            "# Original content preserved below:\n\n"
        )

    async def improve_content(self, prompt: str, target_file: str | None = None) -> str:
        """Use AI to improve the context.

        When Copilot CLI is unavailable, BaseAgent keeps the existing file
        content unchanged instead of injecting duplicated placeholder blocks.
        """
        _ = prompt
        _ = target_file
        logging.info(f"Improving context for {self.file_path}")
        # Include source code in AI context for accurate descriptions
        if self.source_path and self.source_path.exists():
            logging.debug(f"Using source file: {self.source_path}")
            try:
                # Limit source code to 8000 chars to avoid token limits
                source_code = self.source_path.read_text(encoding="utf-8")[:8000]
                enhanced_prompt = (
                    f"{prompt}\n\n"
                    f"Source code to analyze ({self.source_path.name}):\n"
                    f"```\n{source_code}\n```\n\n"
                    "Based on the source code above, provide a comprehensive description."
                )
                return await super().improve_content(enhanced_prompt)
            except (OSError, UnicodeDecodeError):
                pass

        return await super().improve_content(prompt)
