#!/usr / bin / env python3
# Copyright (c) 2025 DebVisor contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org / licenses / LICENSE - 2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""src.agent-context

Maintains and improves `*.description.md` “context” files for source code.

The primary entrypoint is `ContextAgent`, a `BaseAgent` subclass that:

- Accepts a path to a context file (typically `some_module.description.md`).
- Best-effort derives the corresponding source file by matching the same stem
    against common extensions.
- Delegates to `BaseAgent.improve_content()` (Copilot CLI / LLM-backed) to
    improve the description; if a source file exists it includes a truncated slice
    of source code in the prompt to make the description more accurate.

This module also defines a large set of supporting enums, dataclasses, and
helper classes for template management, tagging, versioning, validation,
annotations, prioritization, metadata export, and additional context analysis.

CLI
---
This file exposes a CLI via `create_main_function(...)`:

        python src/agent-context.py path/to/file.description.md
"""

from __future__ import annotations
import hashlib
import json
import logging
import re
import zlib
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from base_agent import BaseAgent, create_main_function


class ContextPriority(Enum):
    """Priority levels for context relevance."""
    CRITICAL = 5
    HIGH = 4
    MEDIUM = 3
    LOW = 2
    MINIMAL = 1


class FileCategory(Enum):
    """Categories for context files."""
    CODE = "code"
    DOCUMENTATION = "documentation"
    CONFIGURATION = "configuration"
    TEST = "test"
    BUILD = "build"
    DATA = "data"
    OTHER = "other"


@dataclass
class ContextTemplate:
    """Template for context documentation."""
    name: str
    file_type: str
    sections: List[str]
    template_content: str
    required_fields: List[str] = field(default_factory=lambda: [])


@dataclass
class ContextTag:
    """A tag for categorizing context."""
    name: str
    description: str = ""
    color: str = "#666666"
    parent: Optional[str] = None


@dataclass
class ContextVersion:
    """Version information for context."""
    version: str
    timestamp: str
    content_hash: str
    changes: List[str] = field(default_factory=lambda: [])
    author: str = ""


@dataclass
class ValidationRule:
    """Rule for validating context content."""
    name: str
    pattern: str
    message: str
    severity: str = "warning"
    required: bool = False


@dataclass
class ContextAnnotation:
    """An annotation / comment on context."""
    id: str
    line_number: int
    content: str
    author: str = ""
    timestamp: str = ""
    resolved: bool = False


# Default templates for common file types
DEFAULT_TEMPLATES: Dict[str, ContextTemplate] = {
    "python": ContextTemplate(
        name="Python Module",
        file_type=".py",
        sections=["Purpose", "Classes", "Functions", "Dependencies", "Usage"],
        template_content="""# Description: `{filename}`

## Purpose
[Describe the module's purpose]

## Classes
[List and describe classes]

## Functions
[List and describe key functions]

## Dependencies
[List required packages and modules]

## Usage
```python
# Example usage
```
""",
        required_fields=["Purpose"]
    ),
    "javascript": ContextTemplate(
        name="JavaScript Module",
        file_type=".js",
        sections=["Purpose", "Exports", "Dependencies", "Usage"],
        template_content="""# Description: `{filename}`

## Purpose
[Describe the module's purpose]

## Exports
[List exported functions, classes, constants]

## Dependencies
[List npm packages and local imports]

## Usage
```javascript
// Example usage
```
""",
        required_fields=["Purpose"]
    ),
    "shell": ContextTemplate(
        name="Shell Script",
        file_type=".sh",
        sections=["Purpose", "Usage", "Arguments", "Environment Variables"],
        template_content="""# Description: `{filename}`

## Purpose
[Describe the script's purpose]

## Usage
```bash
./script.sh [options]
```

## Arguments
| Argument | Description | Required |
|----------|-------------|----------|
| -h       | Show help   | No       |

## Environment Variables
[List required environment variables]
""",
        required_fields=["Purpose", "Usage"]
    ),
    "config": ContextTemplate(
        name="Configuration File",
        file_type=".json/.yaml/.toml",
        sections=["Purpose", "Schema", "Options"],
        template_content="""# Description: `{filename}`

## Purpose
[Describe the configuration's purpose]

## Schema
[Describe the configuration structure]

## Options
| Option | Type | Default | Description |
|--------|------|---------|-------------|
|        |      |         |             |
""",
        required_fields=["Purpose"]
    ),
    "test": ContextTemplate(
        name="Test File",
        file_type="_test.py / test_.py",
        sections=["Purpose", "Test Cases", "Fixtures", "Coverage"],
        template_content="""# Description: `{filename}`

## Purpose
[Describe what this test file covers]

## Test Cases
[List test cases and their purposes]

## Fixtures
[Describe test fixtures used]

## Coverage
[Note which modules / functions are tested]
""",
        required_fields=["Purpose", "Test Cases"]
    ),
}

# Default validation rules
DEFAULT_VALIDATION_RULES: List[ValidationRule] = [
    ValidationRule(
        name="has_purpose",
        pattern=r"##\s*Purpose\b",
        message="Context should have a Purpose section",
        severity="error",
        required=True
    ),
    ValidationRule(
        name="no_empty_sections",
        pattern=r"##\s*\w+\s*\n\s*\n##",
        message="Empty section detected",
        severity="warning"
    ),
    ValidationRule(
        name="valid_code_blocks",
        pattern=r"```\w*\n[\s\S]*?```",
        message="Code blocks should have language identifier",
        severity="info"
    ),
]


# ========== Session 6 Enums ==========


class SearchAlgorithm(Enum):
    """Algorithms for semantic search."""
    KEYWORD = "keyword"
    FUZZY = "fuzzy"
    SEMANTIC = "semantic"
    HYBRID = "hybrid"


class ExportFormat(Enum):
    """Formats for context export."""
    MARKDOWN = "markdown"
    HTML = "html"
    PDF = "pdf"
    DOCX = "docx"
    RST = "rst"


class InheritanceMode(Enum):
    """Modes for context inheritance."""
    OVERRIDE = "override"
    MERGE = "merge"
    APPEND = "append"


class VisualizationType(Enum):
    """Types of context visualization."""
    DEPENDENCY_GRAPH = "dependency_graph"
    CALL_HIERARCHY = "call_hierarchy"
    FILE_TREE = "file_tree"
    MIND_MAP = "mind_map"


class ConflictResolution(Enum):
    """Strategies for merge conflict resolution."""
    OURS = "ours"
    THEIRS = "theirs"
    MANUAL = "manual"
    AUTO = "auto"


class SharingPermission(Enum):
    """Permission levels for context sharing."""
    READ_ONLY = "read_only"
    READ_WRITE = "read_write"
    ADMIN = "admin"


# ========== Session 6 Dataclasses ==========


@dataclass
class SemanticSearchResult:
    """Result from semantic code search.

    Attributes:
        file_path: Path to the matching file.
        content_snippet: Relevant code snippet.
        similarity_score: Similarity score (0 - 1).
        context_type: Type of context matched.
        line_range: Tuple of start and end line numbers.
    """
    file_path: str
    content_snippet: str
    similarity_score: float
    context_type: str = ""
    line_range: Tuple[int, int] = (0, 0)


@dataclass
class CrossRepoContext:
    """Context from cross-repository analysis.

    Attributes:
        repo_name: Name of the repository.
        repo_url: URL to the repository.
        related_files: List of related file paths.
        similarity_score: Overall similarity score.
        common_patterns: Patterns shared between repos.
    """
    repo_name: str
    repo_url: str
    related_files: List[str] = field(default_factory=lambda: [])
    similarity_score: float = 0.0
    common_patterns: List[str] = field(default_factory=lambda: [])


@dataclass
class ContextDiff:
    """Diff between context versions.

    Attributes:
        version_from: Source version.
        version_to: Target version.
        added_sections: List of added sections.
        removed_sections: List of removed sections.
        modified_sections: List of modified section names.
        change_summary: Brief summary of changes.
    """
    version_from: str
    version_to: str
    added_sections: List[str] = field(default_factory=lambda: [])
    removed_sections: List[str] = field(default_factory=lambda: [])
    modified_sections: List[str] = field(default_factory=lambda: [])
    change_summary: str = ""


@dataclass
class InheritedContext:
    """Inherited context from parent file.

    Attributes:
        parent_path: Path to parent context file.
        inherited_sections: Sections inherited from parent.
        mode: Inheritance mode used.
        overrides: Sections that override parent.
    """
    parent_path: str
    inherited_sections: List[str] = field(default_factory=lambda: [])
    mode: InheritanceMode = InheritanceMode.MERGE
    overrides: List[str] = field(default_factory=lambda: [])


@dataclass
class NLQueryResult:
    """Result from natural language query.

    Attributes:
        query: Original query string.
        answer: Generated answer.
        relevant_contexts: List of relevant context files.
        confidence: Confidence score (0 - 1).
    """
    query: str
    answer: str
    relevant_contexts: List[str] = field(default_factory=lambda: [])
    confidence: float = 0.0


@dataclass
class ExportedContext:
    """Exported context document.

    Attributes:
        format: Export format used.
        content: Exported content.
        metadata: Export metadata.
        created_at: Creation timestamp.
    """
    format: ExportFormat
    content: str
    metadata: Dict[str, Any] = field(default_factory=lambda: {})
    created_at: str = ""


@dataclass
class ContextRecommendation:
    """Recommendation for context improvement.

    Attributes:
        source_file: File used as reference.
        suggested_sections: Sections to add.
        reason: Why this recommendation was made.
        confidence: Recommendation confidence.
    """
    source_file: str
    suggested_sections: List[str] = field(default_factory=lambda: [])
    reason: str = ""
    confidence: float = 0.0


@dataclass
class GeneratedCode:
    """Context-aware generated code.

    Attributes:
        language: Programming language.
        code: Generated code content.
        context_used: Context files used for generation.
        description: Description of what the code does.
    """
    language: str
    code: str
    context_used: List[str] = field(default_factory=lambda: [])
    description: str = ""


@dataclass
class RefactoringSuggestion:
    """Context-based refactoring suggestion.

    Attributes:
        suggestion_type: Type of refactoring.
        description: What to refactor.
        affected_files: Files affected by refactoring.
        estimated_impact: Impact assessment.
    """
    suggestion_type: str
    description: str
    affected_files: List[str] = field(default_factory=lambda: [])
    estimated_impact: str = "medium"


@dataclass
class VisualizationData:
    """Data for context visualization.

    Attributes:
        viz_type: Type of visualization.
        nodes: List of node data.
        edges: List of edge connections.
        layout: Layout algorithm to use.
    """
    viz_type: VisualizationType
    nodes: List[Dict[str, Any]] = field(default_factory=lambda: [])
    edges: List[Tuple[str, str]] = field(default_factory=lambda: [])
    layout: str = "hierarchical"


@dataclass
class SharedContext:
    """Context shared with team members.

    Attributes:
        context_id: Unique identifier.
        owner: Owner username.
        shared_with: List of usernames shared with.
        permission: Permission level.
        last_sync: Last synchronization timestamp.
    """
    context_id: str
    owner: str
    shared_with: List[str] = field(default_factory=lambda: [])
    permission: SharingPermission = SharingPermission.READ_ONLY
    last_sync: str = ""


@dataclass
class MergeConflict:
    """Merge conflict information.

    Attributes:
        section: Section with conflict.
        ours: Our version of content.
        theirs: Their version of content.
        resolution: Applied resolution.
    """
    section: str
    ours: str
    theirs: str
    resolution: Optional[ConflictResolution] = None


@dataclass
class BranchComparison:
    """Comparison of context across branches.

    Attributes:
        branch_a: First branch name.
        branch_b: Second branch name.
        files_only_in_a: Files only in branch A.
        files_only_in_b: Files only in branch B.
        modified_files: Files modified between branches.
    """
    branch_a: str
    branch_b: str
    files_only_in_a: List[str] = field(default_factory=lambda: [])
    files_only_in_b: List[str] = field(default_factory=lambda: [])
    modified_files: List[str] = field(default_factory=lambda: [])


# ========== Session 6 Helper Classes ==========


class SemanticSearchEngine:
    """Performs semantic code search using embeddings.

    Provides functionality to search code using semantic similarity
    rather than just keyword matching.

    Attributes:
        results: List of search results.
        index: Index of embedded content.

    Example:
        >>> engine=SemanticSearchEngine()
        >>> results=engine.search("function that handles authentication")
    """

    def __init__(self) -> None:
        """Initialize the semantic search engine."""
        self.results: List[SemanticSearchResult] = []
        self.index: Dict[str, List[float]] = {}
        self.algorithm: SearchAlgorithm = SearchAlgorithm.KEYWORD
        self.similarity_metric: str = "cosine"
        self.documents: Dict[str, str] = {}  # Add documents storage

    def set_algorithm(self, algorithm: SearchAlgorithm) -> None:
        """Set the search algorithm."""
        self.algorithm = algorithm

    def add_document(self, doc_id: str, content: str) -> None:
        """Add a document to the search index."""
        self.documents[doc_id] = content
        self.index_content(doc_id, content)

    def clear(self) -> None:
        """Clear all indexed documents and results."""
        self.results.clear()
        self.index.clear()
        self.documents.clear()

    def index_content(self, file_path: str, content: str) -> None:
        """Index content for searching.

        Args:
            file_path: Path to the file.
            content: File content to index.
        """
        # Simplified embedding (in production, use actual embeddings)
        words = set(content.lower().split())
        self.index[file_path] = [hash(w) % 1000 / 1000 for w in list(words)[:100]]

    def search(
            self,
            query: str,
            algorithm: SearchAlgorithm = SearchAlgorithm.SEMANTIC) -> List[SemanticSearchResult]:
        """Search for related code.

        Args:
            query: Search query.
            algorithm: Search algorithm to use.

        Returns:
            List of search results.
        """
        self.results = []
        query_words = set(query.lower().split())

        for file_path, content in self.documents.items():
            content_words = set(content.lower().split())
            overlap = query_words & content_words
            if not overlap:
                continue

            score = len(overlap) / max(1, len(query_words))
            self.results.append(SemanticSearchResult(
                file_path=file_path,
                content_snippet=content[:80],
                similarity_score=min(score, 1.0)
            ))

        return sorted(self.results, key=lambda r: r.similarity_score, reverse=True)


class CrossRepoAnalyzer:
    """Analyzes context across multiple repositories.

    Provides functionality to find related code and patterns
    across different repositories.

    Example:
        >>> analyzer=CrossRepoAnalyzer()
        >>> analyzer.add_repository("owner / repo", "https://github.com / owner / repo")
        >>> results=analyzer.find_related_contexts("auth.py")
    """

    def __init__(self) -> None:
        """Initialize the cross-repo analyzer."""
        self.repositories: Dict[str, CrossRepoContext] = {}
        self.repos: Dict[str, Dict[str, str]] = {}  # Add repos attribute

    def add_repo(self, name: str, url: str) -> None:
        """Add a repository."""
        self.repos[name] = {"name": name, "url": url}

    def analyze(self, file_path: str) -> List[CrossRepoContext]:
        """Analyze a file path across configured repositories.

        Compatibility wrapper used by tests.
        """
        return self.find_related_contexts(file_path)

    def find_common_patterns(self) -> List[str]:
        """Find common patterns across repos."""
        return []

    def add_repository(self, name: str, url: str) -> CrossRepoContext:
        """Add a repository for analysis.

        Args:
            name: Repository name.
            url: Repository URL.

        Returns:
            Created CrossRepoContext.
        """
        context = CrossRepoContext(repo_name=name, repo_url=url)
        self.repositories[name] = context
        return context

    def find_related_contexts(self, file_path: str) -> List[CrossRepoContext]:
        """Find related contexts across repositories.

        Args:
            file_path: Path to analyze.

        Returns:
            List of related cross - repo contexts.
        """
        results: List[CrossRepoContext] = []
        for repo in self.repositories.values():
            # Simplified matching
            repo.similarity_score = 0.5
            repo.related_files.append(file_path)
            results.append(repo)
        return results


class ContextDiffer:
    """Shows changes in context between versions.

    Provides detailed diff visualization between context versions.

    Example:
        >>> differ=ContextDiffer()
        >>> diff=differ.diff_versions(old_content, new_content)
    """

    def __init__(self) -> None:
        """Initialize context differ."""
        self.diffs: List[str] = []

    def compute_diff(self, content_from: str, content_to: str) -> ContextDiff:
        """Compute a structured diff between two context contents."""
        return self.diff_versions(content_from, content_to)

    def get_section_changes(self, content_from: str, content_to: str) -> Dict[str, List[str]]:
        """Return section-level changes between two contents."""
        diff = self.diff_versions(content_from, content_to)
        return {
            "added": diff.added_sections,
            "removed": diff.removed_sections,
            "modified": diff.modified_sections,
        }

    def summarize_diff(self, diff: ContextDiff) -> str:
        """Summarize a ContextDiff into a human-readable sentence."""
        return diff.change_summary or (
            f"Added {len(diff.added_sections)}, removed {len(diff.removed_sections)}, "
            f"modified {len(diff.modified_sections)} sections"
        )

    def diff_versions(
        self,
        content_from: str,
        content_to: str,
        version_from: str = "v1",
        version_to: str = "v2"
    ) -> ContextDiff:
        """Create diff between two content versions.

        Args:
            content_from: Original content.
            content_to: New content.
            version_from: Source version label.
            version_to: Target version label.

        Returns:
            ContextDiff with changes.
        """
        # Extract sections
        sections_from: set[str] = set(re.findall(r"##\s+(\w+)", content_from))
        sections_to: set[str] = set(re.findall(r"##\s+(\w+)", content_to))
        added: List[str] = list(sections_to - sections_from)
        removed: List[str] = list(sections_from - sections_to)
        modified: List[str] = []
        # Check for modified content in common sections
        common = sections_from & sections_to
        for section in common:
            if content_from.count(section) != content_to.count(section):
                modified.append(section)
        return ContextDiff(
            version_from=version_from,
            version_to=version_to,
            added_sections=added,
            removed_sections=removed,
            modified_sections=modified,
            change_summary=(
                f"Added {len(added)}, removed {len(removed)}, "
                f"modified {len(modified)} sections"
            ))


class ContextInheritance:
    """Manages context inheritance from parent files.

    Provides functionality for child contexts to inherit
    from parent contexts.

    Example:
        >>> inheritance=ContextInheritance()
        >>> inherited=inheritance.inherit_from("parent.description.md", "child.description.md")
    """

    def __init__(self) -> None:
        """Initialize context inheritance manager."""
        self.inheritance_map: Dict[str, InheritedContext] = {}
        self.mode: InheritanceMode = InheritanceMode.MERGE
        self.parent_path: Optional[str] = None

    def set_mode(self, mode: InheritanceMode) -> None:
        """Set inheritance mode."""
        self.mode = mode

    def set_parent(self, parent_path: str) -> None:
        """Set parent context."""
        self.parent_path = parent_path

    def apply(self, child_content: str, parent_content: str) -> str:
        """Apply the currently configured inheritance mode."""
        return self.resolve_inheritance(parent_content, child_content, self.mode)

    def get_hierarchy(self) -> List[str]:
        """Get inheritance hierarchy."""
        return [self.parent_path] if self.parent_path else []

    def inherit_from(
        self,
        parent_path: str,
        child_path: str,
        mode: InheritanceMode = InheritanceMode.MERGE
    ) -> InheritedContext:
        """Set up inheritance relationship.

        Args:
            parent_path: Path to parent context.
            child_path: Path to child context.
            mode: Inheritance mode.

        Returns:
            InheritedContext configuration.
        """
        inherited = InheritedContext(
            parent_path=parent_path,
            mode=mode
        )
        self.inheritance_map[child_path] = inherited
        return inherited

    def resolve_inheritance(
            self,
            parent_content: str,
            child_content: str,
            mode: InheritanceMode) -> str:
        """Resolve inheritance to produce final content.

        Args:
            parent_content: Parent context content.
            child_content: Child context content.
            mode: Inheritance mode.

        Returns:
            Resolved content.
        """
        if mode == InheritanceMode.OVERRIDE:
            return child_content
        elif mode == InheritanceMode.APPEND:
            return parent_content + "\n\n" + child_content
        else:  # MERGE
            # Simple merge: keep child sections, add missing from parent
            child_sections = set(re.findall(r"##\s+(\w+)", child_content))
            parent_sections = re.findall(r"(##\s+\w+.*?)(?=##|\Z)", parent_content, re.DOTALL)

            result = child_content
            for section in parent_sections:
                section_name = re.search(r"##\s+(\w+)", section)
                if section_name and section_name.group(1) not in child_sections:
                    result += "\n" + section.strip()
            return result


class NLQueryEngine:
    """Searches context with natural language queries.

    Provides natural language interface for searching context.

    Example:
        >>> engine=NLQueryEngine()
        >>> result=engine.query("How does authentication work?", contexts)
    """

    def __init__(self) -> None:
        """Initialize NL query engine."""
        self.contexts: Dict[str, str] = {}

    def add_context(self, name: str, content: str) -> None:
        """Add context to the engine."""
        self.contexts[name] = content

    def extract_keywords(self, query: str) -> List[str]:
        """Extract keywords from query."""
        return query.lower().split()

    def query(self, question: str, contexts: Optional[Dict[str, str]] = None) -> NLQueryResult:
        """Query contexts with natural language.

        Args:
            question: Natural language question.
            contexts: Optional dictionary of context file paths to contents.
                      If omitted, uses contexts added via add_context().

        Returns:
            NLQueryResult with answer.
        """
        # Simplified NL query - in production, use LLM
        relevant: List[str] = []
        keywords = question.lower().split()
        active_contexts = contexts if contexts is not None else self.contexts
        for path, content in active_contexts.items():
            content_lower = content.lower()
            if any(kw in content_lower for kw in keywords):
                relevant.append(path)
        return NLQueryResult(
            query=question,
            answer=f"Found {len(relevant)} relevant context files",
            relevant_contexts=relevant,
            confidence=0.7 if relevant else 0.2
        )


class ContextExporter:
    """Exports context to documentation systems.

    Provides functionality to export context to various formats.

    Example:
        >>> exporter=ContextExporter()
        >>> exported=exporter.export(content, ExportFormat.HTML)
    """

    def __init__(self, default_format: ExportFormat = ExportFormat.MARKDOWN) -> None:
        self.default_format: ExportFormat = default_format

    def set_format(self, format: ExportFormat) -> None:
        """Set the default export format."""
        self.default_format = format

    def get_supported_formats(self) -> List[ExportFormat]:
        """Return all supported export formats."""
        return list(ExportFormat)

    def export(self, content: str, format: Optional[ExportFormat] = None) -> ExportedContext:
        """Export context to specified format.

        Args:
            content: Context content to export.
            format: Target export format. If omitted, uses default_format.

        Returns:
            ExportedContext with exported content.
        """
        fmt = format if format is not None else self.default_format

        exported_content = content
        if fmt == ExportFormat.HTML:
            exported_content = self._to_html(content)
        elif fmt == ExportFormat.RST:
            exported_content = self._to_rst(content)
        return ExportedContext(
            format=fmt,
            content=exported_content,
            created_at=datetime.now().isoformat()
        )

    def _to_html(self, content: str) -> str:
        """Convert markdown to HTML."""
        # Simplified conversion
        html = content
        html = re.sub(r"^# (.+)$", r"<h1>\1</h1>", html, flags=re.M)
        html = re.sub(r"^## (.+)$", r"<h2>\1</h2>", html, flags=re.M)
        html = re.sub(r"^- (.+)$", r"<li>\1</li>", html, flags=re.M)
        return f"<html><body>{html}</body></html>"

    def _to_rst(self, content: str) -> str:
        """Convert markdown to RST."""
        rst = content
        # Convert headers
        rst = re.sub(r"^# (.+)$", lambda m: m.group(1) + "\n" +
                     "=" * len(m.group(1)), rst, flags=re.M)
        rst = re.sub(r"^## (.+)$", lambda m: m.group(1) + "\n" +
                     "-" * len(m.group(1)), rst, flags=re.M)
        return rst


class ContextRecommender:
    """Recommends context improvements based on similar files.

    Analyzes similar files to suggest context improvements.

    Example:
        >>> recommender=ContextRecommender()
        >>> recommendations=recommender.recommend("auth.py", similar_contexts)
    """

    def __init__(self) -> None:
        self.reference_files: Dict[str, str] = {}

    def add_reference(self, file_name: str, content: str) -> None:
        """Add a reference context file used for recommendations."""
        self.reference_files[file_name] = content

    def find_similar(self, query: str) -> List[str]:
        """Find reference files that look similar to the query."""
        query_words = set(query.lower().split())
        matches: List[str] = []
        for name, content in self.reference_files.items():
            content_words = set(content.lower().split())
            if query_words & content_words:
                matches.append(name)
        return matches

    def recommend(
        self,
        content_or_target_file: str,
        similar_contexts: Optional[Dict[str, str]] = None
    ) -> List[ContextRecommendation]:
        """Generate context recommendations.

        Compatibility behavior:
        - If similar_contexts is provided, it is treated as the corpus.
        - Otherwise, content_or_target_file is treated as the target content
          and reference_files are used as the corpus.
        """
        corpus = similar_contexts if similar_contexts is not None else self.reference_files
        target_content = content_or_target_file

        recommendations: List[ContextRecommendation] = []
        if not corpus:
            return recommendations

        target_sections = set(re.findall(r"##\s+(\w+)", target_content))

        section_counts: Dict[str, int] = {}
        for _, content in corpus.items():
            sections = re.findall(r"##\s+(\w+)", content)
            for section in sections:
                section_counts[section] = section_counts.get(section, 0) + 1

        common_sections: List[Tuple[str, int]] = sorted(section_counts.items(), key=lambda x: x[1], reverse=True)
        suggested = [name for name, _ in common_sections if name not in target_sections][:5]
        if suggested:
            recommendations.append(ContextRecommendation(
                source_file=list(corpus.keys())[0],
                suggested_sections=suggested,
                reason="Common sections in similar files",
                confidence=0.8
            ))

        return recommendations


class CodeGenerator:
    """Generates code based on context.

    Uses context information to generate relevant code.

    Example:
        >>> generator=CodeGenerator()
        >>> code=generator.generate("Create a login function", context)
    """

    def __init__(self) -> None:
        self.language: str = "python"
        self.contexts: Dict[str, str] = {}

    def set_language(self, language: str) -> None:
        """Set the default target language for generated code."""
        self.language = language

    def add_context(self, name: str, content: str) -> None:
        """Add a named context document that can be referenced later."""
        self.contexts[name] = content

    def get_supported_languages(self) -> List[str]:
        """Return supported target languages."""
        return [
            "python",
            "javascript",
            "typescript",
            "java",
            "csharp",
            "go",
            "rust",
        ]

    def generate(
        self,
        prompt: str,
        context: str = "",
        language: Optional[str] = None,
        *,
        context_files: Optional[List[str]] = None,
    ) -> GeneratedCode:
        """Generate code based on stored context.

        Backwards compatible with the older signature:
            generate(prompt, context, language="python")

        Newer API (used by tests):
            set_language(...), add_context(...), generate(prompt, context_files=[...])
        """
        resolved_language = language or self.language or "python"

        used_contexts: List[str] = []
        context_snippets: List[str] = []

        if context_files:
            for name in context_files:
                if name in self.contexts:
                    used_contexts.append(name)
                    context_snippets.append(self.contexts[name])
        elif context:
            # Inline context (legacy usage)
            used_contexts.append(context[:50] + ("..." if len(context) > 50 else ""))
            context_snippets.append(context)

        # Simplified generation - in production, use an LLM.
        context_header = "" if not used_contexts else f"# Context used: {', '.join(used_contexts)}\n"
        code = (
            f"# Generated for: {prompt}\n"
            f"{context_header}"
            f"def generated_function():\n"
            f"    \"\"\"Auto-generated stub.\"\"\"\n"
            f"    pass\n"
        )

        return GeneratedCode(
            language=resolved_language,
            code=code,
            context_used=used_contexts,
            description=prompt,
        )


class RefactoringAdvisor:
    """Suggests refactoring based on context analysis.

    Analyzes context to suggest code refactoring opportunities.

    Example:
        >>> advisor=RefactoringAdvisor()
        >>> suggestions=advisor.analyze(contexts)
    """

    def __init__(self) -> None:
        self.patterns: Dict[str, Dict[str, str]] = {}

    def add_pattern(self, name: str, pattern: str, description: str) -> None:
        """Add a custom refactoring pattern.

        Args:
            name: Pattern identifier.
            pattern: Regex pattern to search for.
            description: Human-readable suggestion description.
        """
        self.patterns[name] = {"pattern": pattern, "description": description}

    def analyze(self, contexts: Any) -> List[RefactoringSuggestion]:
        """Analyze contexts for refactoring opportunities.

        Args:
            contexts: Either a single context string or a dictionary of
                context file paths to contents.

        Returns:
            List of refactoring suggestions.
        """
        context_map: Dict[str, str]
        if isinstance(contexts, str):
            context_map = {"inline": contexts}
        elif isinstance(contexts, dict):
            context_map = contexts  # type: ignore
        else:
            raise TypeError("contexts must be a string or a dict")

        suggestions: List[RefactoringSuggestion] = []

        # Apply custom patterns first.
        for path, content in context_map.items():
            for name, spec in self.patterns.items():
                try:
                    if re.search(spec["pattern"], content):
                        suggestions.append(RefactoringSuggestion(
                            suggestion_type=name,
                            description=spec.get("description", ""),
                            affected_files=[path],
                            estimated_impact="low",
                        ))
                except re.error:
                    # Invalid user-provided regex; ignore for robustness.
                    continue

        # Look for duplicate descriptions (indicating code duplication)
        descriptions: Dict[str, List[str]] = {}
        for path, content in context_map.items():
            purpose = re.search(r"##\s*Purpose\s*\n(.+?)(?=##|\Z)", content, re.DOTALL)
            if purpose:
                desc = purpose.group(1).strip()[:100]
                if desc not in descriptions:
                    descriptions[desc] = []
                descriptions[desc].append(path)
        for desc, files in descriptions.items():
            if len(files) > 1:
                suggestions.append(RefactoringSuggestion(
                    suggestion_type="extract_common",
                    description=f"Similar purpose found in {len(files)} files",
                    affected_files=files,
                    estimated_impact="medium"
                ))
        return suggestions

    def prioritize(self, suggestions: List[RefactoringSuggestion]) -> List[RefactoringSuggestion]:
        """Prioritize refactoring suggestions.

        Args:
            suggestions: Suggestions to prioritize.

        Returns:
            Suggestions sorted by estimated impact.
        """
        impact_rank = {"high": 0, "medium": 1, "low": 2}

        def rank(s: RefactoringSuggestion) -> int:
            return impact_rank.get(getattr(s, "estimated_impact", "medium"), 1)

        return sorted(list(suggestions), key=rank)


class ContextVisualizer:
    """Visualizes context relationships.

    Creates visual representations of context dependencies and hierarchies.

    Example:
        >>> visualizer=ContextVisualizer()
        >>> data=visualizer.create_dependency_graph(contexts)
    """

    def __init__(self, viz_type: VisualizationType = VisualizationType.DEPENDENCY_GRAPH) -> None:
        self.viz_type: VisualizationType = viz_type
        self.nodes: List[Dict[str, Any]] = []
        self.edges: List[Tuple[str, str]] = []
        self.layout: str = "hierarchical"

    def set_type(self, viz_type: VisualizationType) -> None:
        self.viz_type = viz_type

    def add_node(self, node_id: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        if metadata is None:
            metadata = {}
        self.nodes.append({"id": node_id, **metadata})

    def add_edge(self, source: str, target: str) -> None:
        self.edges.append((source, target))

    def generate(self) -> VisualizationData:
        return VisualizationData(
            viz_type=self.viz_type,
            nodes=self.nodes,
            edges=self.edges,
            layout=self.layout,
        )

    def export_json(self) -> str:
        data = self.generate()
        payload: Dict[str, Any] = {
            "viz_type": data.viz_type.value,
            "nodes": data.nodes,
            "edges": data.edges,
            "layout": data.layout,
        }
        return json.dumps(payload)

    def create_dependency_graph(self, contexts: Dict[str, str]) -> VisualizationData:
        """Create dependency graph visualization.

        Args:
            contexts: Dictionary of context file paths to contents.

        Returns:
            VisualizationData for rendering.
        """
        nodes: List[Dict[str, str]] = []
        edges: List[Tuple[str, str]] = []
        for path, content in contexts.items():
            nodes.append({"id": path, "label": Path(path).name})
            # Find references to other files
            for other_path in contexts.keys():
                if other_path != path:
                    other_name = Path(other_path).stem
                    if other_name in content:
                        edges.append((path, other_path))
        return VisualizationData(
            viz_type=VisualizationType.DEPENDENCY_GRAPH,
            nodes=nodes,
            edges=edges
        )

    def create_call_hierarchy(self, contexts: Dict[str, str]) -> VisualizationData:
        """Create call hierarchy visualization.

        Args:
            contexts: Dictionary of context file paths to contents.

        Returns:
            VisualizationData for rendering.
        """
        nodes: List[Dict[str, str]] = []
        edges: List[Tuple[str, str]] = []
        for path in contexts.keys():
            nodes.append({"id": path, "label": Path(path).name})
        return VisualizationData(
            viz_type=VisualizationType.CALL_HIERARCHY,
            nodes=nodes,
            edges=edges,
            layout="tree"
        )


class ContextSharingManager:
    """Manages context sharing across team members.

    Provides functionality for sharing and synchronizing context.

    Example:
        >>> manager=ContextSharingManager()
        >>> shared=manager.share("context.md", ["user1", "user2"])
    """

    def __init__(self, owner: str = "current_user") -> None:
        """Initialize sharing manager."""
        self.owner: str = owner
        self.shared_contexts: Dict[str, SharedContext] = {}
        self._contents: Dict[str, str] = {}

    def create_shared(
        self,
        content: str,
        context_id: Optional[str] = None,
        permission: SharingPermission = SharingPermission.READ_ONLY,
    ) -> SharedContext:
        if context_id is None:
            context_id = f"context_{len(self.shared_contexts) + 1}"
        shared = SharedContext(
            context_id=context_id,
            owner=self.owner,
            shared_with=[],
            permission=permission,
            last_sync=datetime.now().isoformat(),
        )
        self.shared_contexts[context_id] = shared
        self._contents[context_id] = content
        return shared

    def share_with(self, context_id: str, user: str) -> None:
        shared = self.shared_contexts.get(context_id)
        if not shared:
            raise KeyError(f"Unknown context_id: {context_id}")
        if user not in shared.shared_with:
            shared.shared_with.append(user)
        shared.last_sync = datetime.now().isoformat()

    def set_permission(self, context_id: str, permission: SharingPermission) -> None:
        shared = self.shared_contexts.get(context_id)
        if not shared:
            raise KeyError(f"Unknown context_id: {context_id}")
        shared.permission = permission
        shared.last_sync = datetime.now().isoformat()

    def revoke_access(self, context_id: str, user: str) -> None:
        shared = self.shared_contexts.get(context_id)
        if not shared:
            raise KeyError(f"Unknown context_id: {context_id}")
        if user in shared.shared_with:
            shared.shared_with.remove(user)
        shared.last_sync = datetime.now().isoformat()

    def get_shared_contexts(self) -> List[SharedContext]:
        return list(self.shared_contexts.values())

    def share(
        self,
        context_id: str,
        users: List[str],
        owner: str = "current_user",
        permission: SharingPermission = SharingPermission.READ_ONLY
    ) -> SharedContext:
        """Share context with users.

        Args:
            context_id: Context identifier.
            users: List of usernames to share with.
            owner: Owner username.
            permission: Permission level.

        Returns:
            SharedContext configuration.
        """
        # Backwards compatible API: keep accepting explicit owner/users.
        self.owner = owner
        shared = self.create_shared("", context_id=context_id, permission=permission)
        for user in users:
            self.share_with(shared.context_id, user)
        return shared

    def get_shared_users(self, context_id: str) -> List[str]:
        """Get users a context is shared with.

        Args:
            context_id: Context identifier.

        Returns:
            List of usernames.
        """
        shared = self.shared_contexts.get(context_id)
        return shared.shared_with if shared else []


class MergeConflictResolver:
    """Resolves merge conflicts in context files.

    Provides strategies for resolving conflicts during context merges.

    Example:
        >>> resolver=MergeConflictResolver()
        >>> resolved=resolver.resolve(conflict, ConflictResolution.OURS)
    """

    def __init__(self, strategy: ConflictResolution = ConflictResolution.AUTO) -> None:
        self.strategy: ConflictResolution = strategy

    def set_strategy(self, strategy: ConflictResolution) -> None:
        self.strategy = strategy

    def detect_conflicts(self, ours: str, theirs: Optional[str] = None) -> List[MergeConflict]:
        """Detect merge conflicts.

        Supports two modes:
        - detect_conflicts(content_with_markers)
        - detect_conflicts(ours, theirs)
        """
        if theirs is None:
            content = ours
            conflicts: List[MergeConflict] = []
            pattern = r"<<<<<<<[^\n]*\n(.*?)\n=======\n(.*?)\n>>>>>>>"
            for match in re.finditer(pattern, content, re.DOTALL):
                conflicts.append(MergeConflict(
                    section="conflict",
                    ours=match.group(1),
                    theirs=match.group(2)
                ))
            return conflicts

        if ours == theirs:
            return []

        def _section_name(text: str) -> str:
            first = text.strip().splitlines()[0] if text.strip() else ""
            if first.startswith("##"):
                return first.lstrip("#").strip() or "section"
            return "content"

        return [MergeConflict(section=_section_name(ours), ours=ours, theirs=theirs)]

    def resolve(self, conflict: MergeConflict, strategy: Optional[ConflictResolution] = None) -> str:
        """Resolve a merge conflict.

        Args:
            conflict: Conflict to resolve.
            strategy: Optional resolution strategy (defaults to current strategy).

        Returns:
            Resolved content.
        """
        effective = strategy or self.strategy
        if effective == ConflictResolution.OURS:
            conflict.resolution = effective
            return conflict.ours
        if effective == ConflictResolution.THEIRS:
            conflict.resolution = effective
            return conflict.theirs
        if effective == ConflictResolution.AUTO:
            # Auto: prefer longer content
            conflict.resolution = effective
            return conflict.ours if len(conflict.ours) >= len(conflict.theirs) else conflict.theirs

        conflict.resolution = ConflictResolution.MANUAL
        return f"MANUAL RESOLUTION NEEDED:\n{conflict.ours}\n---\n{conflict.theirs}"

    def resolve_all(
        self,
        conflicts: List[MergeConflict],
        strategy: Optional[ConflictResolution] = None,
    ) -> str:
        """Resolve all conflicts and join results."""
        return "\n".join(self.resolve(c, strategy=strategy) for c in conflicts)


class BranchComparer:
    """Compares context across git branches.

    Provides functionality to compare context files between branches.

    Example:
        >>> comparer=BranchComparer()
        >>> comparison=comparer.compare("main", "feature")
    """

    def __init__(self) -> None:
        self.branch_a: str = ""
        self.branch_b: str = ""
        self._last_comparison: Optional[BranchComparison] = None

    def set_branches(self, branch_a: str, branch_b: str) -> None:
        self.branch_a = branch_a
        self.branch_b = branch_b

    def get_modified_files(self) -> List[str]:
        if not self._last_comparison:
            return []
        return list(self._last_comparison.modified_files)

    def summarize(self, comparison: BranchComparison) -> str:
        return (
            f"Compare {comparison.branch_a} -> {comparison.branch_b}: "
            f"only_in_a={len(comparison.files_only_in_a)}, "
            f"only_in_b={len(comparison.files_only_in_b)}, "
            f"modified={len(comparison.modified_files)}"
        )

    def compare(
        self,
        branch_a: Optional[str] = None,
        branch_b: Optional[str] = None,
        contexts_a: Optional[Dict[str, str]] = None,
        contexts_b: Optional[Dict[str, str]] = None,
    ) -> BranchComparison:
        """Compare contexts between branches.

        Args:
            branch_a: First branch name (optional; defaults to stored branches).
            branch_b: Second branch name (optional; defaults to stored branches).
            contexts_a: Contexts from branch A (optional; defaults to empty).
            contexts_b: Contexts from branch B (optional; defaults to empty).

        Returns:
            BranchComparison with differences.
        """
        resolved_a = branch_a if branch_a is not None else self.branch_a
        resolved_b = branch_b if branch_b is not None else self.branch_b
        ctx_a = contexts_a or {}
        ctx_b = contexts_b or {}

        files_a = set(ctx_a.keys())
        files_b = set(ctx_b.keys())
        modified: List[str] = []
        for f in files_a & files_b:
            if ctx_a[f] != ctx_b[f]:
                modified.append(f)
        comparison = BranchComparison(
            branch_a=resolved_a,
            branch_b=resolved_b,
            files_only_in_a=list(files_a - files_b),
            files_only_in_b=list(files_b - files_a),
            modified_files=modified
        )
        self._last_comparison = comparison
        return comparison


class ContextAgent(BaseAgent):
    """Updates code file context descriptions using AI assistance."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._validate_file_extension()
        self.source_path = self._derive_source_path()

        # New features
        self._templates: Dict[str, ContextTemplate] = dict(DEFAULT_TEMPLATES)
        self._tags: Dict[str, ContextTag] = {}
        self._versions: List[ContextVersion] = []
        self._validation_rules: List[ValidationRule] = list(DEFAULT_VALIDATION_RULES)
        self._annotations: List[ContextAnnotation] = []
        self._priority: ContextPriority = ContextPriority.MEDIUM
        self._category: FileCategory = FileCategory.OTHER
        self._compressed_content: Optional[bytes] = None
        self._metadata: Dict[str, Any] = {}

    def _validate_file_extension(self) -> None:
        """Validate that the file has the correct extension."""
        if not self.file_path.name.endswith('.description.md'):
            # Just warn, don't fail
            pass

    def _derive_source_path(self) -> Optional[Path]:
        """Derive source file path from .description.md filename."""
        if self.file_path.name.endswith('.description.md'):
            stem = self.file_path.name.replace('.description.md', '')
            # Try common extensions
            for ext in [
                '.py', '.js', '.ts', '.go', '.rs', '.java', '.sh',
                '.json', '.yaml', '.yml', '.toml', '.ini', '.cfg',
                '.md', '.rst', '.txt'
            ]:
                source = self.file_path.parent / f"{stem}{ext}"
                if source.exists():
                    return source
        return None

    # ========== Template Management ==========

    def set_template(self, template_name: str) -> bool:
        """Set the active template by name."""
        if template_name in self._templates:
            logging.info(f"Using template: {template_name}")
            return True
        logging.warning(f"Template '{template_name}' not found")
        return False

    def get_template_by_name(self, template_name: str) -> Optional[ContextTemplate]:
        """Get a template by name."""
        return self._templates.get(template_name.lower())

    def get_template(self, template_name: str) -> Optional[ContextTemplate]:
        """Compatibility alias: get a template by name.

        Tests and older callers use get_template(...); internally this agent
        stores templates in the _templates mapping.
        """
        return self._templates.get(template_name.lower())

    def add_template(self, template: ContextTemplate) -> None:
        """Add a custom template."""
        self._templates[template.name.lower()] = template
        logging.info(f"Added template: {template.name}")

    def get_template_for_file(self) -> Optional[ContextTemplate]:
        """Get the appropriate template for the current file."""
        if not self.source_path:
            return None

        ext = self.source_path.suffix.lower()
        name = self.source_path.name.lower()

        # Check test files first
        if "test" in name or name.startswith("test_"):
            return self._templates.get("test")

        # Match by extension
        ext_mapping = {
            ".py": "python",
            ".js": "javascript",
            ".ts": "javascript",
            ".sh": "shell",
            ".bash": "shell",
            ".json": "config",
            ".yaml": "config",
            ".yml": "config",
            ".toml": "config",
        }

        template_name = ext_mapping.get(ext)
        return self._templates.get(template_name) if template_name else None

    def apply_template(self, template_name: Optional[str] = None) -> str:
        """Apply a template to generate initial content."""
        template = None
        if template_name:
            template = self._templates.get(template_name)
        else:
            template = self.get_template_for_file()

        if not template:
            return self._get_default_content()

        filename = self.file_path.name.replace('.description.md', '')
        return template.template_content.format(filename=filename)

    # ========== Tagging ==========

    def add_tag(self, tag: ContextTag) -> None:
        """Add a tag."""
        self._tags[tag.name] = tag

    def remove_tag(self, tag_name: str) -> bool:
        """Remove a tag."""
        if tag_name in self._tags:
            del self._tags[tag_name]
            return True
        return False

    def get_tags(self) -> List[ContextTag]:
        """Get all tags."""
        return list(self._tags.values())

    def has_tag(self, tag_name: str) -> bool:
        """Check if a tag exists."""
        return tag_name in self._tags

    def get_tags_by_parent(self, parent_name: str) -> List[ContextTag]:
        """Get all tags with a specific parent."""
        return [t for t in self._tags.values() if t.parent == parent_name]

    # ========== Versioning ==========

    def create_version(
        self,
        version: str,
        changes: Optional[List[str]] = None,
        author: str = ""
    ) -> ContextVersion:
        """Create a new version snapshot."""
        content = self.current_content or self.previous_content or ""
        content_hash = hashlib.sha256(content.encode()).hexdigest()[:12]

        version_obj = ContextVersion(
            version=version,
            timestamp=datetime.now().isoformat(),
            content_hash=content_hash,
            changes=changes or [],
            author=author
        )

        self._versions.append(version_obj)
        logging.info(f"Created version {version}")
        return version_obj

    def get_versions(self) -> List[ContextVersion]:
        """Get all versions."""
        return self._versions

    def get_latest_version(self) -> Optional[ContextVersion]:
        """Get the latest version."""
        return self._versions[-1] if self._versions else None

    def get_version_diff(self, v1: str, v2: str) -> Dict[str, Any]:
        """Get diff between two versions."""
        ver1 = next((v for v in self._versions if v.version == v1), None)
        ver2 = next((v for v in self._versions if v.version == v2), None)

        if not ver1 or not ver2:
            return {"error": "Version not found"}

        return {
            "from_version": v1,
            "to_version": v2,
            "from_hash": ver1.content_hash,
            "to_hash": ver2.content_hash,
            "changed": ver1.content_hash != ver2.content_hash,
            "changes_v2": ver2.changes
        }

    # ========== Compression ==========

    def compress_content(self, content: Optional[str] = None) -> bytes:
        """Compress content for storage."""
        if content is None:
            content = self.current_content or self.previous_content or ""

        self._compressed_content = zlib.compress(content.encode(), level=9)
        return self._compressed_content

    def decompress_content(self, compressed: Optional[bytes] = None) -> str:
        """Decompress stored content."""
        if compressed is None:
            compressed = self._compressed_content

        if compressed is None:
            return ""

        return zlib.decompress(compressed).decode()

    def get_compression_ratio(self, content: Optional[str] = None) -> float:
        """Get compression ratio (space savings) for the current/previous content."""
        if content is None:
            content = self.current_content or self.previous_content or ""

        original_size = len(content.encode())
        if original_size == 0:
            return 0.0

        compressed = self._compressed_content
        if compressed is None:
            compressed = self.compress_content(content)
        compressed_size = len(compressed)
        return 1 - (compressed_size / original_size)

    # ========== Validation ==========

    def add_validation_rule(self, rule: ValidationRule) -> None:
        """Add a validation rule."""
        self._validation_rules.append(rule)

    def validate_content(self, content: Optional[str] = None) -> List[Dict[str, Any]]:
        """Validate content against all rules."""
        if content is None:
            content = self.current_content or self.previous_content or ""

        issues: List[Dict[str, Any]] = []

        for rule in self._validation_rules:
            if rule.required:
                # Required patterns must be present
                if not re.search(rule.pattern, content):
                    issues.append({
                        "rule": rule.name,
                        "message": rule.message,
                        "severity": rule.severity,
                        "required": True
                    })
            else:
                # Non - required patterns are warnings when matched
                matches = re.findall(rule.pattern, content)
                if matches and rule.severity != "info":
                    issues.append({
                        "rule": rule.name,
                        "message": rule.message,
                        "severity": rule.severity,
                        "matches": len(matches)
                    })

        return issues

    def is_valid(self, content: Optional[str] = None) -> bool:
        """Check if content passes all required validations."""
        issues = self.validate_content(content)
        return not any(i.get("severity") == "error" for i in issues)

    # ========== Annotations ==========

    def add_annotation(
        self,
        line_number: int,
        content: str,
        author: str = ""
    ) -> ContextAnnotation:
        """Add an annotation to the context."""
        annotation = ContextAnnotation(
            id=hashlib.md5(f"{line_number}:{content}".encode()).hexdigest()[:8],
            line_number=line_number,
            content=content,
            author=author,
            timestamp=datetime.now().isoformat()
        )
        self._annotations.append(annotation)
        return annotation

    def get_annotations(self) -> List[ContextAnnotation]:
        """Get all annotations."""
        return self._annotations

    def get_annotations_for_line(self, line_number: int) -> List[ContextAnnotation]:
        """Get annotations for a specific line."""
        return [a for a in self._annotations if a.line_number == line_number]

    def resolve_annotation(self, annotation_id: str) -> bool:
        """Mark an annotation as resolved."""
        for annotation in self._annotations:
            if annotation.id == annotation_id:
                annotation.resolved = True
                return True
        return False

    def remove_annotation(self, annotation_id: str) -> bool:
        """Remove an annotation."""
        for i, annotation in enumerate(self._annotations):
            if annotation.id == annotation_id:
                del self._annotations[i]
                return True
        return False

    # ========== Priority Scoring ==========

    def set_priority(self, priority: ContextPriority) -> None:
        """Set the priority level."""
        self._priority = priority

    def get_priority(self) -> ContextPriority:
        """Get the priority level."""
        return self._priority

    def calculate_priority_score(self) -> float:
        """Calculate a priority score based on various factors."""
        score = 0.0
        content = self.current_content or self.previous_content or ""

        # Base score from priority level
        score += self._priority.value * 10

        # Add points for content completeness
        sections = ["Purpose", "Usage", "Dependencies", "Examples"]
        for section in sections:
            if f"## {section}" in content:
                score += 5

        # Add points for code examples
        code_blocks = re.findall(r"```\w+", content)
        score += min(len(code_blocks) * 3, 15)

        # Add points for having tags
        score += min(len(self._tags) * 2, 10)

        # Penalize for validation issues
        issues = self.validate_content(content)
        score -= len([i for i in issues if i.get("severity") == "error"]) * 10
        score -= len([i for i in issues if i.get("severity") == "warning"]) * 5

        return max(0, min(100, score))

    # ========== Categorization ==========

    def set_category(self, category: FileCategory) -> None:
        """Set the file category."""
        self._category = category

    def get_category(self) -> FileCategory:
        """Get the file category."""
        return self._category

    def auto_categorize(self) -> FileCategory:
        """Automatically categorize based on file analysis."""
        if not self.source_path:
            return FileCategory.OTHER

        name = self.source_path.name.lower()
        ext = self.source_path.suffix.lower()

        # Test files
        if "test" in name or name.startswith("test_"):
            self._category = FileCategory.TEST
        # Configuration files
        elif ext in [".json", ".yaml", ".yml", ".toml", ".ini", ".cfg"]:
            self._category = FileCategory.CONFIGURATION
        # Build files
        elif name in ["makefile", "dockerfile", "cmakelists.txt"] or ext in [".mk"]:
            self._category = FileCategory.BUILD
        # Documentation
        elif ext in [".md", ".rst", ".txt"]:
            self._category = FileCategory.DOCUMENTATION
        # Data files
        elif ext in [".csv", ".xml", ".sql"]:
            self._category = FileCategory.DATA
        # Code files
        elif ext in [".py", ".js", ".ts", ".go", ".rs", ".java", ".cpp", ".c"]:
            self._category = FileCategory.CODE
        else:
            self._category = FileCategory.OTHER

        return self._category

    # ========== Metadata ==========

    def set_metadata(self, key: str, value: Any) -> None:
        """Set a metadata value."""
        self._metadata[key] = value

    def get_metadata(self, key: str) -> Optional[Any]:
        """Get a metadata value."""
        return self._metadata.get(key)

    def get_all_metadata(self) -> Dict[str, Any]:
        """Get all metadata."""
        return dict(self._metadata)

    def export_metadata(self) -> str:
        """Export metadata as JSON."""
        data: Dict[str, Any] = {
            "priority": self._priority.value,
            "category": self._category.value,
            "tags": [t.name for t in self._tags.values()],
            "versions": len(self._versions),
            "annotations": len(self._annotations),
            "custom": self._metadata
        }
        return json.dumps(data, indent=2)

    # ========== Core Methods ==========
    def _get_default_content(self) -> str:
        """Return rich, structured template for new descriptions."""
        self.file_path.name.replace('.description.md', '')
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
        return ("# AI Improvement Unavailable\n"
                "# GitHub CLI not found. Install from https://cli.github.com/\n\n"
                "# Original content preserved below:\n\n")

    def improve_content(self, prompt: str) -> str:
        """Use AI to improve the context.

        When Copilot CLI is unavailable, BaseAgent keeps the existing file
        content unchanged instead of injecting duplicated placeholder blocks.
        """
        logging.info(f"Improving context for {self.file_path}")
        # Include source code in AI context for accurate descriptions
        if self.source_path and self.source_path.exists():
            logging.debug(f"Using source file: {self.source_path}")
            try:
                # Limit source code to 8000 chars to avoid token limits
                source_code = self.source_path.read_text(encoding='utf-8')[:8000]
                enhanced_prompt = (
                    f"{prompt}\n\n"
                    f"Source code to analyze ({self.source_path.name}):\n"
                    f"```\n{source_code}\n```\n\n"
                    "Based on the source code above, provide a comprehensive description."
                )
                return super().improve_content(enhanced_prompt)
            except (OSError, UnicodeDecodeError):
                pass

        return super().improve_content(prompt)


# Create main function using the helper
main = create_main_function(
    ContextAgent,
    'Context Agent: Updates code file descriptions',
    'Path to the context file (e.g., file.description.md)'
)

if __name__ == '__main__':
    main()
