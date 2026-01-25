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

# -*- coding: utf-8 -*-
"""Test classes from test_agent_context.py - core module."""

from __future__ import annotations
from pathlib import Path
import sys

# Import test utilities
from tests.utils.agent_test_utils import *

# Import from src if needed


class TestSemanticSearch:
    """Tests for semantic search using embeddings."""

    def test_semantic_search_basic(self, tmp_path: Path) -> None:
        """Test basic semantic search."""
        with agent_dir_on_path():
            mod: sys.ModuleType = load_agent_module("src/logic/agents/cognitive/context_agent.py")

        content = "def calculate_total(items) -> bool: return sum(items)"
        target: Path = tmp_path / "test.description.md"
        target.write_text(content)

        agent = mod.ContextAgent(str(target))
        previous = agent.read_previous_content()

        assert "calculate_total" in previous

    def test_semantic_search_relevance(self, tmp_path: Path) -> None:
        """Test semantic search returns relevant results."""
        with agent_dir_on_path():
            mod: sys.ModuleType = load_agent_module("src/logic/agents/cognitive/context_agent.py")

        content = "# User Authentication\nThis module handles user login."
        target: Path = tmp_path / "auth.description.md"
        target.write_text(content)

        agent = mod.ContextAgent(str(target))
        content = agent.read_previous_content()

        assert "Authentication" in content


# =============================================================================
# Session 9: Cross-Repository Context Tests
# =============================================================================


class TestCrossRepositoryContext:
    """Tests for cross-repository context analysis."""

    def test_cross_repo_reference(self, tmp_path: Path) -> None:
        """Test detecting cross-repository references."""
        with agent_dir_on_path():
            mod: sys.ModuleType = load_agent_module("src/logic/agents/cognitive/context_agent.py")

        content = "Depends on: github.com / org / other-repo"
        target: Path = tmp_path / "test.description.md"
        target.write_text(content)

        agent = mod.ContextAgent(str(target))
        previous = agent.read_previous_content()

        assert "github.com" in previous


# =============================================================================
# Session 9: Context Diffing Tests
# =============================================================================


class TestContextDiffing:
    """Tests for context diffing between versions."""

    def test_diff_content_detection(self, tmp_path: Path) -> None:
        """Test diff content is detected."""
        with agent_dir_on_path():
            mod: sys.ModuleType = load_agent_module("src/logic/agents/cognitive/context_agent.py")

        content = """
## Version 2.0
- New feature
## Version 1.0
- Original feature
"""
        target: Path = tmp_path / "test.description.md"
        target.write_text(content)

        agent = mod.ContextAgent(str(target))
        previous = agent.read_previous_content()

        assert "Version 2.0" in previous
        assert "Version 1.0" in previous


# =============================================================================
# Session 9: Context Template Application Tests
# =============================================================================


class TestContextTemplateApplication:
    """Tests for context template application."""

    def test_template_placeholder_detection(self, tmp_path: Path) -> None:
        """Test template placeholder detection."""
        with agent_dir_on_path():
            mod: sys.ModuleType = load_agent_module("src/logic/agents/cognitive/context_agent.py")

        content = "# {module_name}\n\nDescription: {description}"
        target: Path = tmp_path / "template.description.md"
        target.write_text(content)

        agent = mod.ContextAgent(str(target))
        previous = agent.read_previous_content()

        assert "{module_name}" in previous


# =============================================================================
# Session 9: Context Inheritance Tests
# =============================================================================


class TestContextInheritance:
    """Tests for context inheritance chains."""

    def test_inheritance_detection(self, tmp_path: Path) -> None:
        """Test detecting inheritance in context."""
        with agent_dir_on_path():
            mod: sys.ModuleType = load_agent_module("src/logic/agents/cognitive/context_agent.py")

        content = "Extends: base_module\nInherits: core.BaseClass"
        target: Path = tmp_path / "test.description.md"
        target.write_text(content)

        agent = mod.ContextAgent(str(target))
        previous = agent.read_previous_content()

        assert "Extends:" in previous


# =============================================================================
# Session 9: Context Tagging Tests
# =============================================================================


class TestContextTagging:
    """Tests for context tagging and categorization."""

    def test_tag_detection(self, tmp_path: Path) -> None:
        """Test tag detection in context."""
        with agent_dir_on_path():
            mod: sys.ModuleType = load_agent_module("src/logic/agents/cognitive/context_agent.py")

        content = "Tags: [security], [authentication], [api]"
        target: Path = tmp_path / "test.description.md"
        target.write_text(content)

        agent = mod.ContextAgent(str(target))
        previous = agent.read_previous_content()

        assert "[security]" in previous

    def test_category_detection(self, tmp_path: Path) -> None:
        """Test category detection."""
        with agent_dir_on_path():
            mod: sys.ModuleType = load_agent_module("src/logic/agents/cognitive/context_agent.py")

        content = "Category: Core Infrastructure"
        target: Path = tmp_path / "test.description.md"
        target.write_text(content)

        agent = mod.ContextAgent(str(target))
        previous = agent.read_previous_content()

        assert "Category:" in previous


# =============================================================================
# Session 9: Natural Language Search Tests
# =============================================================================


class TestNaturalLanguageSearch:
    """Tests for natural language context search."""

    def test_natural_language_query(self, tmp_path: Path) -> None:
        """Test natural language content is searchable."""
        with agent_dir_on_path():
            mod: sys.ModuleType = load_agent_module("src/logic/agents/cognitive/context_agent.py")

        content = "This module handles the user login process and session management."
        target: Path = tmp_path / "test.description.md"
        target.write_text(content)

        agent = mod.ContextAgent(str(target))
        previous = agent.read_previous_content()

        assert "user login" in previous


# =============================================================================
# Session 9: Context Versioning Tests
# =============================================================================


class TestContextVersioning:
    """Tests for context versioning and history tracking."""

    def test_version_header_detection(self, tmp_path: Path) -> None:
        """Test version header detection."""
        with agent_dir_on_path():
            mod: sys.ModuleType = load_agent_module("src/logic/agents/cognitive/context_agent.py")

        content = "# Context v2.0.0\n\nUpdated description."
        target: Path = tmp_path / "test.description.md"
        target.write_text(content)

        agent = mod.ContextAgent(str(target))
        previous = agent.read_previous_content()

        assert "v2.0.0" in previous


# =============================================================================
# Session 9: Context Compression Tests
# =============================================================================


class TestContextCompression:
    """Tests for context compression efficiency."""

    def test_large_context_readable(self, tmp_path: Path) -> None:
        """Test large context can be read."""
        with agent_dir_on_path():
            mod: sys.ModuleType = load_agent_module("src/logic/agents/cognitive/context_agent.py")

        content: str = "\n".join([f"Line {i}: Description text" for i in range(100)])
        target: Path = tmp_path / "large.description.md"
        target.write_text(content)

        agent = mod.ContextAgent(str(target))
        previous = agent.read_previous_content()

        assert "Line 0" in previous
        assert "Line 99" in previous


# =============================================================================
# Session 9: Context Export Tests
# =============================================================================


class TestContextExport:
    """Tests for context export to documentation systems."""

    def test_markdown_format_preserved(self, tmp_path: Path) -> None:
        """Test markdown format is preserved for export."""
        with agent_dir_on_path():
            mod: sys.ModuleType = load_agent_module("src/logic/agents/cognitive/context_agent.py")

        content = "# Title\n\n## Section\n\n- Item 1\n- Item 2"
        target: Path = tmp_path / "test.description.md"
        target.write_text(content)

        agent = mod.ContextAgent(str(target))
        previous = agent.read_previous_content()

        assert "# Title" in previous
        assert "## Section" in previous


# =============================================================================
# Session 9: Context Validation Tests
# =============================================================================


class TestContextValidation:
    """Tests for context validation rules."""

    def test_valid_context_format(self, tmp_path: Path) -> None:
        """Test valid context format is accepted."""
        with agent_dir_on_path():
            mod: sys.ModuleType = load_agent_module("src/logic/agents/cognitive/context_agent.py")

        content = "# Module: test_module\n\n## Purpose\n\nTest purpose."
        target: Path = tmp_path / "test.description.md"
        target.write_text(content)

        agent = mod.ContextAgent(str(target))
        previous = agent.read_previous_content()

        assert "Module:" in previous


# =============================================================================
# Session 9: Context Annotation Tests
# =============================================================================


class TestContextAnnotation:
    """Tests for context annotation persistence."""

    def test_annotation_detection(self, tmp_path: Path) -> None:
        """Test annotation detection."""
        with agent_dir_on_path():
            mod: sys.ModuleType = load_agent_module("src/logic/agents/cognitive/context_agent.py")

        content = "<!-- @author: John Doe -->\n# Module"
        target: Path = tmp_path / "test.description.md"
        target.write_text(content)

        agent = mod.ContextAgent(str(target))
        previous = agent.read_previous_content()

        assert "@author" in previous


# =============================================================================
# Session 9: Context Recommendation Tests
# =============================================================================


class TestContextRecommendation:
    """Tests for context recommendation accuracy."""

    def test_related_content_detection(self, tmp_path: Path) -> None:
        """Test related content detection."""
        with agent_dir_on_path():
            mod: sys.ModuleType = load_agent_module("src/logic/agents/cognitive/context_agent.py")

        content = "Related: auth_module, user_module, session_module"
        target: Path = tmp_path / "test.description.md"
        target.write_text(content)

        agent = mod.ContextAgent(str(target))
        previous = agent.read_previous_content()

        assert "auth_module" in previous


# =============================================================================
# Session 9: Context-Aware Code Generation Tests
# =============================================================================


class TestContextAwareCodeGeneration:
    """Tests for context-aware code generation."""

    def test_code_example_detection(self, tmp_path: Path) -> None:
        """Test code example detection in context."""
        with agent_dir_on_path():
            mod: sys.ModuleType = load_agent_module("src/logic/agents/cognitive/context_agent.py")

        content = """
## Example Usage

```python
from module import function
result=function(arg)
```
"""
        target: Path = tmp_path / "test.description.md"
        target.write_text(content)

        agent = mod.ContextAgent(str(target))
        previous = agent.read_previous_content()

        assert "```python" in previous


# =============================================================================
# Session 9: Context-Based Refactoring Tests
# =============================================================================


class TestContextBasedRefactoring:
    """Tests for context-based refactoring suggestions."""

    def test_refactoring_note_detection(self, tmp_path: Path) -> None:
        """Test refactoring note detection."""
        with agent_dir_on_path():
            mod: sys.ModuleType = load_agent_module("src/logic/agents/cognitive/context_agent.py")

        content = "TODO: Refactor this module to use async / await"
        target: Path = tmp_path / "test.description.md"
        target.write_text(content)

        agent = mod.ContextAgent(str(target))
        previous = agent.read_previous_content()

        assert "Refactor" in previous


# =============================================================================
# Session 9: Context Merge Conflict Tests
# =============================================================================


class TestContextMergeConflict:
    """Tests for context merge conflict resolution."""

    def test_conflict_marker_detection(self, tmp_path: Path) -> None:
        """Test conflict marker detection."""
        with agent_dir_on_path():
            mod: sys.ModuleType = load_agent_module("src/logic/agents/cognitive/context_agent.py")

        content = """
<<<<<<< HEAD
Old description
=======
New description
>>>>>>> branch
"""
        target: Path = tmp_path / "test.description.md"
        target.write_text(content)

        agent = mod.ContextAgent(str(target))
        previous = agent.read_previous_content()

        assert "<<<<<<< HEAD" in previous


# =============================================================================
# Session 9: Context Access Control Tests
# =============================================================================


class TestContextAccessControl:
    """Tests for context access control."""

    def test_read_access(self, tmp_path: Path) -> None:
        """Test read access to context."""
        with agent_dir_on_path():
            mod: sys.ModuleType = load_agent_module("src/logic/agents/cognitive/context_agent.py")

        content = "# Private Module\n\nInternal use only."
        target: Path = tmp_path / "test.description.md"
        target.write_text(content)

        agent = mod.ContextAgent(str(target))
        previous = agent.read_previous_content()

        assert "Private Module" in previous


# =============================================================================
# Session 9: Context Archival Tests
# =============================================================================


class TestContextArchival:
    """Tests for context archival and retention."""

    def test_archived_marker_detection(self, tmp_path: Path) -> None:
        """Test archived marker detection."""
        with agent_dir_on_path():
            mod: sys.ModuleType = load_agent_module("src/logic/agents/cognitive/context_agent.py")

        content = "<!-- ARCHIVED: 2024-12-01 -->\n# Old Module"
        target: Path = tmp_path / "test.description.md"
        target.write_text(content)

        agent = mod.ContextAgent(str(target))
        previous = agent.read_previous_content()

        assert "ARCHIVED" in previous


# =============================================================================
# Session 9: Context Search Indexing Tests
# =============================================================================


class TestContextSearchIndexing:
    """Tests for context search indexing."""

    def test_keywords_extracted(self, tmp_path: Path) -> None:
        """Test keywords can be extracted from context."""
        with agent_dir_on_path():
            mod: sys.ModuleType = load_agent_module("src/logic/agents/cognitive/context_agent.py")

        content = "Keywords: authentication, security, oauth2, jwt"
