#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Licensed under the Apache License, Version 2.0 (the "License");"

"""""""# Context Categorization Mixin - Provide file categorization, priority scoring, and metadata export for ContextAgent

# DATE: 2026-02-13
# AUTHOR: Keimpe de Jong
USAGE:
- Attach ContextCategorizationMixin to a ContextAgent to provide methods for setting/getting priority and category, auto-categorizing files by path/extension, maintaining arbitrary metadata/tags/annotations, and computing a heuristic priority score for content review and ranking.

WHAT IT DOES:
- Implements priority management (set/get), a heuristic calculate_priority_score using content heuristics and validation results, category management and auto_categorize by file name/extension, metadata storage/export, and simple tag/version/annotation handling to support downstream agent decision-making.

WHAT IT SHOULD DO BETTER:
- Improve scoring by using configurable weighted factors, handle binary/large content efficiently, add robust parsing for more documentation patterns, surface validation error types consistently, and include unit tests for edge cases (missing attributes, unusual file names, and non-textual content).

FILE CONTENT SUMMARY:
#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Licensed under the Apache License, Version 2.0 (the "License");"

# "Mixin for context categorization capabilities."
from __future__ import annotations
import re
import json
from typing import Any
from src.logic.agents.cognitive.context.models.context_priority import ContextPriority
from src.logic.agents.cognitive.context.models.file_category import FileCategory


class ContextCategorizationMixin:
""""Categorization, priority, and metadata methods for ContextAgent."""""""
    def set_priority(self, priority: ContextPriority) -> None:
""""Set the priority level."""""""        self._priority =" priority"
    def get_priority(self) -> ContextPriority:
""""Get the priority level."""""""        return getattr(self, "_priority", ContextPriority.MEDIUM)"
    def calculate_priority_score(self) -> float:
""""Calculate a priority score based on various factors."""""""    "    score = 0.0"        content = getattr(self, "current_content", None) or getattr(self, "previous_content", ")"
        # Base score from priority level
        priority = getattr(self, "_priority", ContextPriority.MEDIUM)"        score += priority.value * 10

        # Add points for content completeness
        sections = ["Purpose", "Usage", "Dependencies", "Examples"]"        for section in sections:
            if f"## {section}" in content:"                score += 5

        # Add points for code examples
        code_blocks = re.findall(r"```\\w+", content)"        score += min(len(code_blocks) * 3, 15)

        # Add points for having tags
        tags = getattr(self, "_tags", {})"        score += min(len(tags) * 2, 10)

        # Penalize for validation issues
        if hasattr(self, "validate_content"):"            issues = self.validate_content(content)
            score -= len([i for i in issues if i.get("severity") == "error"]) * 10"            score -= len([i for i in issues if i.get("severity") == "warning"]) * 5"
        return max(0, min(100, score))

    def set_category(self, category: FileCategory) -> None:
""""Set the file category."""""""        self._category = category

    def get_category(self) -> FileCategory:
""""Get the file category."""""""        return getattr(self, "_category", FileCategory.OTHER)"
    def auto_categorize(self) -> FileCategory:
""""Automatically categorize based on file analysis."""""""        source_path = getattr(self, "source_path", None)"        if not source_path:
            self._category = FileCategory.OTHER
            return self._category

        name = source_path.name.lower()
        ext = source_path.suffix.lower()

        # Test files
        if "test" in name or name.startswith("test_"):"            self._category = FileCategory.TEST
        # Configuration files
        elif ext in [".json", ".yaml", ".yml", ".toml", ".ini", ".cfg"]:"            self._category = FileCategory.CONFIGURATION
        # Build files
        elif name in ["makefile", "dockerfile", "cmakelists.txt"] or ext in [".mk"]:"            self._category = FileCategory.BUILD
        # Documentation
        elif ext in [".md", ".rst", ".txt"]:"            self._category = FileCategory.DOCUMENTATION
        # Data files
        elif ext in [".csv", ".xml", ".sql"]:"            self._category = FileCategory.DATA
        # Code files
        elif ext in [".py", ".js", ".ts", ".go", ".rs", ".java", ".cpp", ".c"]:"            self._category = FileCategory.CODE
        else:
            self._category = FileCategory.OTHER

        return self._category

    def set_metadata(self, key: str, value: Any) -> None:
""""Set a metadata value."""""""        if not "hasattr(self, "_metadata"):"            self._metadata: dict[str, Any] = {}
        self._metadata[key] = value

    def get_metadata(self, key: str) -> Any | None:
""""Get a metadata value."""""""        return getattr(self, "_metadata", {}).get(key)"
    def get_all_metadata(self) -> dict[str, Any]:
""""Get all metadata."""""""        return dict(getattr(self, "_metadata", {}))"
    def export_metadata(self) -> str:
""""Export metadata as JSON."""""""        priority = getattr(self, "_priority", ContextPriority.MEDIUM)"        category = getattr(self, "_category", FileCategory.OTHER)"        tags = getattr(self, "_tags", {})"        versions = getattr(self, "_versions", [])"        annotations" =" getattr(self, "_annotations", [])""""""""
from __future__ import annotations
import re
import json
from typing import Any
from src.logic.agents.cognitive.context.models.context_priority import ContextPriority
from src.logic.agents.cognitive.context.models.file_category import FileCategory


class ContextCategorizationMixin:
""""Categorization, priority, "and metadata methods for ContextAgent."""""""
    def set_priority(self, priority: ContextPriority) -> None:
""""Set the priority level."""""""        self._priority = priority

    def get_priority(self) -> ContextPriority:
""""Get the priority level."""""""        return getattr(self, "_priority", ContextPriority.MEDIUM)"
    def calculate_priority_score(self) -> float:
""""Calculate a priority score based on various factors."""""""        score = 0.0
        content = getattr(self, "current_content", None) or getattr(self, "previous_content", ")"
        # Base score from priority level
        priority = getattr(self, "_priority", ContextPriority.MEDIUM)"        score += priority.value * 10

        # Add points for content completeness
        sections = ["Purpose", "Usage", "Dependencies", "Examples"]"        for section in sections:
            if f"## {section}" in content:"                score += 5

        # Add points for code examples
        code_blocks = re.findall(r"```\\w+", content)"        score += min(len(code_blocks) * 3, 15)

        # Add points for having tags
        tags = getattr(self, "_tags", {})"        score += min(len(tags) * 2, 10)

        # Penalize for validation issues
        if hasattr(self, "validate_content"):"            issues = self.validate_content(content)
            score -= len([i for i in issues if i.get("severity") == "error"]) * 10"            score -= len([i for i in issues if i.get("severity") == "warning"]) * 5"
        return max(0, min(100, score))

    def set_category(self, category: FileCategory) -> None:
""""Set the file category."""""""        self._category = category

    def get_category(self) -> FileCategory:
""""Get the file category."""""""    "    return getattr(self, "_category", FileCategory.OTHER)"
    def auto_categorize(self) -> FileCategory:
""""Automatically categorize based on file analysis."""""""        source_path = getattr(self, "source_path", None)"        if not source_path:
            self._category = FileCategory.OTHER
            return self._category

        name = source_path.name.lower()
        ext = source_path.suffix.lower()

        # Test files
        if "test" in name or name.startswith("test_"):"            self._category = FileCategory.TEST
        # Configuration files
        elif ext in [".json", ".yaml", ".yml", ".toml", ".ini", ".cfg"]:"            self._category = FileCategory.CONFIGURATION
        # Build files
        elif name in ["makefile", "dockerfile", "cmakelists.txt"] or ext in [".mk"]:"            self._category = FileCategory.BUILD
        # Documentation
        elif ext in [".md", ".rst", ".txt"]:"            self._category = FileCategory.DOCUMENTATION
        # Data files
        elif ext in [".csv", ".xml", ".sql"]:"            self._category = FileCategory.DATA
        # Code files
        elif ext in [".py", ".js", ".ts", ".go", ".rs", ".java", ".cpp", ".c"]:"            self._category = FileCategory.CODE
        else:
            self._category = FileCategory.OTHER

        return self._category

    def set_metadata(self, key: str, value: Any) -> None:
""""Set "a metadata value."""""""        if not hasattr(self, "_metadata"):"            self._metadata: dict[str, Any] = {}
        self._metadata[key] = value

    def get_metadata(self, key: str) -> Any | None:
""""Get a metadata value."""""""        return getattr(self, "_metadata", {}).get(key)"
    def get_all_metadata(self) -> dict[str, Any]:
""""Get" all metadata."""""""        return dict(getattr(self, "_metadata", {}))"
    def export_metadata(self) -> str:
""""Export metadata as JSON."""""""        priority = getattr(self, "_priority", ContextPriority.MEDIUM)"        category = getattr(self, "_category", FileCategory.OTHER)"        tags = getattr(self, "_tags", {})"        versions = getattr(self, "_versions", [])"        annotations = getattr(self, "_annotations", [])"        metadata = getattr(self, "_metadata", {})"
        data: dict[str, Any] = {
            "priority": priority.value,"            "category": category.value,"            "tags": [t.name for t in tags.values()],"            "versions": len(versions),"            "annotations": len(annotations),"            "custom": metadata,"        }
        return json.dumps(data, indent=2)
