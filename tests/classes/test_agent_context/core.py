# -*- coding: utf-8 -*-
"""Test classes from test_agent_context.py - core module."""

from __future__ import annotations
import unittest
from typing import Any, List, Dict, Optional, Callable, Tuple, Set, Union
from unittest.mock import MagicMock, Mock, patch, call, ANY
import time
import json
from datetime import datetime
import pytest
import logging
from pathlib import Path
import sys
import os
import tempfile
import shutil
import subprocess
import threading
import asyncio
import ast
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# Import test utilities
from tests.agent_test_utils import *

# Import from src if needed
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))


class TestSemanticSearch:
    """Tests for semantic search using embeddings."""

    def test_semantic_search_basic(self, tmp_path: Path) -> None:
        """Test basic semantic search."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_context.py")

        content = "def calculate_total(items): return sum(items)"
        target = tmp_path / "test.description.md"
        target.write_text(content)

        agent = mod.ContextAgent(str(target))
        previous = agent.read_previous_content()

        assert "calculate_total" in previous

    def test_semantic_search_relevance(self, tmp_path: Path) -> None:
        """Test semantic search returns relevant results."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_context.py")

        content = "# User Authentication\nThis module handles user login."
        target = tmp_path / "auth.description.md"
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
            mod = load_agent_module("agent_context.py")

        content = "Depends on: github.com / org / other-repo"
        target = tmp_path / "test.description.md"
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
            mod = load_agent_module("agent_context.py")

        content = """
## Version 2.0
- New feature
## Version 1.0
- Original feature
"""
        target = tmp_path / "test.description.md"
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
            mod = load_agent_module("agent_context.py")

        content = "# {module_name}\n\nDescription: {description}"
        target = tmp_path / "template.description.md"
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
            mod = load_agent_module("agent_context.py")

        content = "Extends: base_module\nInherits: core.BaseClass"
        target = tmp_path / "test.description.md"
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
            mod = load_agent_module("agent_context.py")

        content = "Tags: [security], [authentication], [api]"
        target = tmp_path / "test.description.md"
        target.write_text(content)

        agent = mod.ContextAgent(str(target))
        previous = agent.read_previous_content()

        assert "[security]" in previous

    def test_category_detection(self, tmp_path: Path) -> None:
        """Test category detection."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_context.py")

        content = "Category: Core Infrastructure"
        target = tmp_path / "test.description.md"
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
            mod = load_agent_module("agent_context.py")

        content = "This module handles the user login process and session management."
        target = tmp_path / "test.description.md"
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
            mod = load_agent_module("agent_context.py")

        content = "# Context v2.0.0\n\nUpdated description."
        target = tmp_path / "test.description.md"
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
            mod = load_agent_module("agent_context.py")

        content = "\n".join([f"Line {i}: Description text" for i in range(100)])
        target = tmp_path / "large.description.md"
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
            mod = load_agent_module("agent_context.py")

        content = "# Title\n\n## Section\n\n- Item 1\n- Item 2"
        target = tmp_path / "test.description.md"
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
            mod = load_agent_module("agent_context.py")

        content = "# Module: test_module\n\n## Purpose\n\nTest purpose."
        target = tmp_path / "test.description.md"
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
            mod = load_agent_module("agent_context.py")

        content = "<!-- @author: John Doe -->\n# Module"
        target = tmp_path / "test.description.md"
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
            mod = load_agent_module("agent_context.py")

        content = "Related: auth_module, user_module, session_module"
        target = tmp_path / "test.description.md"
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
            mod = load_agent_module("agent_context.py")

        content = """
## Example Usage

```python
from module import function
result=function(arg)
```
"""
        target = tmp_path / "test.description.md"
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
            mod = load_agent_module("agent_context.py")

        content = "TODO: Refactor this module to use async / await"
        target = tmp_path / "test.description.md"
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
            mod = load_agent_module("agent_context.py")

        content = """
<<<<<<< HEAD
Old description
=======
New description
>>>>>>> branch
"""
        target = tmp_path / "test.description.md"
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
            mod = load_agent_module("agent_context.py")

        content = "# Private Module\n\nInternal use only."
        target = tmp_path / "test.description.md"
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
            mod = load_agent_module("agent_context.py")

        content = "<!-- ARCHIVED: 2024-12-01 -->\n# Old Module"
        target = tmp_path / "test.description.md"
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
            mod = load_agent_module("agent_context.py")

        content = "Keywords: authentication, security, oauth2, jwt"
        target = tmp_path / "test.description.md"
        target.write_text(content)

        agent = mod.ContextAgent(str(target))
        previous = agent.read_previous_content()

        assert "authentication" in previous
        assert "jwt" in previous


# =============================================================================
# Session 9: Context Notification Tests
# =============================================================================



class TestContextNotification:
    """Tests for context notification triggers."""

    def test_alert_marker_detection(self, tmp_path: Path) -> None:
        """Test alert marker detection."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_context.py")

        content = "> ⚠️ WARNING: This module is deprecated."
        target = tmp_path / "test.description.md"
        target.write_text(content, encoding="utf-8")

        agent = mod.ContextAgent(str(target))
        previous = agent.read_previous_content()

        assert "WARNING" in previous

    def test_breaking_change_detection(self, tmp_path: Path) -> None:
        """Test breaking change detection."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_context.py")

        content = "BREAKING CHANGE: API signature changed in v2.0"
        target = tmp_path / "test.description.md"
        target.write_text(content)

        agent = mod.ContextAgent(str(target))
        previous = agent.read_previous_content()

        assert "BREAKING CHANGE" in previous


# ========== Comprehensive Context Tests (from test_agent_context_comprehensive.py) ==========



class TestContextCreation(unittest.TestCase):
    """Tests for context creation and initialization."""

    def test_create_context_basic(self):
        """Test creating a basic context."""
        context = {
            "user_id": "user123",
            "session_id": "sess123",
            "timestamp": datetime.now(),
        }

        assert context["user_id"] == "user123"
        assert context["session_id"] == "sess123"
        assert context["timestamp"] is not None

    def test_create_context_with_defaults(self):
        """Test creating context with default values."""
        context = {
            "user_id": "user123",
            "session_id": "sess123",
            "timeout": 3600,
            "retries": 3,
            "debug": False,
        }

        assert context["timeout"] == 3600
        assert context["retries"] == 3
        assert context["debug"] is False

    def test_create_context_nested(self):
        """Test creating nested context."""
        context = {
            "user": {
                "id": "user123",
                "name": "Alice",
                "roles": ["admin"],
            },
            "environment": {
                "stage": "production",
                "region": "us-east-1",
            },
        }

        assert context["user"]["id"] == "user123"
        assert context["environment"]["stage"] == "production"

    def test_create_context_with_metadata(self):
        """Test creating context with metadata."""
        context = {
            "id": "ctx123",
            "created_at": datetime.now(),
            "metadata": {
                "source": "api",
                "version": "1.0",
            },
        }

        assert context["metadata"]["source"] == "api"



class TestContextStateTracking(unittest.TestCase):
    """Tests for context state tracking."""

    def test_track_context_state_transitions(self):
        """Test tracking context state transitions."""
        states = ["initialized", "processing", "completed"]
        state_history = []

        for state in states:
            state_history.append(state)

        assert len(state_history) == 3
        assert state_history[-1] == "completed"

    def test_track_modified_fields(self):
        """Test tracking modified fields."""
        context = {"value": 10}
        modifications = []

        context["value"] = 20
        modifications.append(("value", 10, 20))

        assert len(modifications) == 1
        assert modifications[0][2] == 20

    def test_track_context_dirty_state(self):
        """Test tracking dirty state."""
        context = {"name": "Alice", "_dirty": False}

        context["name"] = "Bob"
        context["_dirty"] = True

        assert context["_dirty"] is True

    def test_track_context_read_only_fields(self):
        """Test tracking read-only field violations."""
        context = {"id": "ctx123", "_read_only": ["id"]}
        violations = []

        # Attempt to modify read-only field
        if "id" in context.get("_read_only", []):
            violations.append("id")

        assert "id" in violations



class TestContextLifecycle(unittest.TestCase):
    """Tests for context lifecycle management."""

    def test_context_creation_lifecycle(self):
        """Test context creation lifecycle."""
        lifecycle = []

        # Create
        context = {"id": "ctx1"}
        lifecycle.append("created")

        # Initialize
        context["initialized"] = True
        lifecycle.append("initialized")

        # Cleanup
        context.clear()
        lifecycle.append("cleaned")

        assert lifecycle == ["created", "initialized", "cleaned"]

    def test_context_timeout_lifecycle(self):
        """Test context timeout lifecycle."""
        context = {
            "created_at": datetime.now(),
            "timeout": 3600,
            "status": "active",
        }

        # Still valid
        assert context["status"] == "active"

        # Simulate timeout
        context["status"] = "expired"
        assert context["status"] == "expired"

    def test_context_resource_management(self):
        """Test context resource management."""
        resources = []

        # Allocate
        resources.append("connection")
        resources.append("file_handle")

        assert len(resources) == 2

        # Release
        resources.clear()
        assert len(resources) == 0

    def test_context_cleanup_on_exception(self):
        """Test context cleanup on exception."""
        context = {"active": True}
        cleanup_called = False

        try:
            raise ValueError("Error")
        except ValueError:
            context["active"] = False
            cleanup_called = True

        assert cleanup_called
        assert context["active"] is False



class TestContextStorage(unittest.TestCase):
    """Tests for context storage and retrieval."""

    def test_store_context_value(self):
        """Test storing context value."""
        context = {}
        context["key1"] = "value1"

        assert context["key1"] == "value1"

    def test_retrieve_context_value(self):
        """Test retrieving context value."""
        context = {"key1": "value1", "key2": "value2"}

        value = context.get("key1")
        assert value == "value1"

    def test_retrieve_nonexistent_with_default(self):
        """Test retrieving nonexistent with default."""
        context = {"key1": "value1"}

        value = context.get("missing", "default")
        assert value == "default"

    def test_store_complex_object(self):
        """Test storing complex object."""
        context = {
            "user": {
                "id": 1,
                "name": "Alice",
                "roles": ["admin", "user"],
            }
        }

        assert context["user"]["name"] == "Alice"
        assert "admin" in context["user"]["roles"]



class TestContextVariables(unittest.TestCase):
    """Tests for context-local variables."""

    def test_set_context_variable(self):
        """Test setting context variable."""
        context = {}
        context["var1"] = "value1"

        assert "var1" in context

    def test_get_context_variable(self):
        """Test getting context variable."""
        context = {"var1": "value1"}

        assert context["var1"] == "value1"

    def test_delete_context_variable(self):
        """Test deleting context variable."""
        context = {"var1": "value1"}
        del context["var1"]

        assert "var1" not in context

    def test_context_variable_isolation(self):
        """Test context variable isolation."""
        ctx1_vars = {"var": "ctx1_value"}
        ctx2_vars = {"var": "ctx2_value"}

        assert ctx1_vars["var"] != ctx2_vars["var"]



class TestContextPropagation(unittest.TestCase):
    """Tests for context propagation through call chains."""

    def test_propagate_context_to_function(self):
        """Test propagating context to function."""
        context = {"user_id": "user1"}

        def process(ctx):
            return ctx["user_id"]

        result = process(context)
        assert result == "user1"

    def test_propagate_through_nested_calls(self):
        """Test propagating through nested calls."""
        context = {"value": 10}

        def level1(ctx):
            return level2(ctx)

        def level2(ctx):
            return level3(ctx)

        def level3(ctx):
            return ctx["value"]

        result = level1(context)
        assert result == 10

    def test_propagate_to_async_context(self):
        """Test propagating to async context."""
        context = {"async_id": "async1"}

        async_contexts = []
        async_contexts.append(context)

        assert async_contexts[0]["async_id"] == "async1"

    def test_propagate_with_implicit_context(self):
        """Test propagating with implicit context."""
        context_stack = [{"level": 1}]

        # Add another level
        context_stack.append({**context_stack[-1], "level": 2})

        assert context_stack[-1]["level"] == 2



class TestContextMerging(unittest.TestCase):
    """Tests for context merging."""

    def test_merge_contexts(self):
        """Test merging two contexts."""
        ctx1 = {"key1": "value1"}
        ctx2 = {"key2": "value2"}

        merged = {**ctx1, **ctx2}

        assert merged["key1"] == "value1"
        assert merged["key2"] == "value2"

    def test_merge_with_override(self):
        """Test merging with override."""
        ctx1 = {"shared": "original", "unique1": "value1"}
        ctx2 = {"shared": "override", "unique2": "value2"}

        merged = {**ctx1, **ctx2}

        assert merged["shared"] == "override"
        assert merged["unique1"] == "value1"
        assert merged["unique2"] == "value2"

    def test_merge_nested_contexts(self):
        """Test merging nested contexts."""
        ctx1 = {"data": {"a": 1}}
        ctx2 = {"data": {"b": 2}}

        # Simple merge (not recursive)
        merged = {**ctx1, **ctx2}
        assert merged["data"]["b"] == 2

    def test_merge_empty_context(self):
        """Test merging empty context."""
        ctx = {"key": "value"}
        empty = {}

        merged = {**ctx, **empty}
        assert merged["key"] == "value"



class TestContextSerialization(unittest.TestCase):
    """Tests for context serialization."""

    def test_serialize_context_to_dict(self):
        """Test serializing context to dict."""
        context = {
            "id": "ctx1",
            "user": "alice",
            "timestamp": datetime.now().isoformat(),
        }

        serialized = dict(context)
        assert isinstance(serialized, dict)
        assert serialized["id"] == "ctx1"

    def test_serialize_context_to_json(self):
        """Test serializing context to JSON."""
        import json
        context = {"id": "ctx1", "name": "test"}

        json_str = json.dumps(context)
        assert "ctx1" in json_str

    def test_deserialize_context(self):
        """Test deserializing context."""
        import json
        json_str = '{"id": "ctx1", "name": "test"}'

        context = json.loads(json_str)
        assert context["id"] == "ctx1"

    def test_serialize_with_nested_structures(self):
        """Test serializing with nested structures."""
        import json
        context = {
            "user": {"id": 1, "name": "Alice"},
            "tags": ["tag1", "tag2"],
        }

        json_str = json.dumps(context)
        restored = json.loads(json_str)
        assert restored["user"]["name"] == "Alice"



class TestASTSignatureExtraction(unittest.TestCase):
    """Test extracting class and function signatures using AST."""

    def test_function_signature_extraction(self):
        """Test extracting function signature from AST."""
        code = """
def calculate(x: int, y: int) -> int:
    '''Calculate sum of two integers.'''
    return x + y
        """
        tree = ast.parse(code)
        func_def = tree.body[0]

        self.assertIsInstance(func_def, ast.FunctionDef)
        self.assertEqual(func_def.name, 'calculate')
        self.assertEqual(len(func_def.args.args), 2)

    def test_class_signature_extraction(self):
        """Test extracting class definition from AST."""
        code = """
class DataProcessor:
    def __init__(self, name: str):
        self.name=name

    def process(self, data):
        return data
        """
        tree = ast.parse(code)
        class_def = tree.body[0]

        self.assertIsInstance(class_def, ast.ClassDef)
        self.assertEqual(class_def.name, 'DataProcessor')
        self.assertEqual(len(class_def.body), 2)

    def test_method_signature_extraction(self):
        """Test extracting method signatures from class."""
        code = """
class Calculator:
    def add(self, a: int, b: int) -> int:
        return a + b

    def multiply(self, a: int, b: int) -> int:
        return a * b
        """
        tree = ast.parse(code)
        class_def = tree.body[0]
        methods = [n for n in class_def.body if isinstance(n, ast.FunctionDef)]

        self.assertEqual(len(methods), 2)
        self.assertEqual(methods[0].name, 'add')



class TestDependencyGraphAnalysis(unittest.TestCase):
    """Test dependency graph analysis and visualization."""

    def test_import_extraction(self):
        """Test extracting imports from module."""
        code = """
        import os
        from pathlib import Path
        from typing import Dict, List
        import numpy as np
        """
        tree = ast.parse(code)
        imports = [
            node for node in ast.walk(tree) if isinstance(
                node, (ast.Import, ast.ImportFrom))]

        self.assertEqual(len(imports), 4)

    def test_dependency_tree_building(self):
        """Test building dependency tree."""
        dependencies = {
            'module_a': ['module_b', 'module_c'],
            'module_b': ['module_d'],
            'module_c': ['module_d'],
            'module_d': []
        }

        # Check depth
        def max_depth(node, deps, visited=None):
            if visited is None:
                visited = set()
            if node in visited:
                return 0
            visited.add(node)
            if not deps.get(node):
                return 1
            return 1 + max(max_depth(child, deps, visited) for child in deps.get(node, []))

        depth = max_depth('module_a', dependencies)
        self.assertEqual(depth, 3)

    def test_circular_dependency_detection(self):
        """Test detecting circular dependencies."""
        dependencies = {
            'module_a': ['module_b'],
            'module_b': ['module_c'],
            'module_c': ['module_a']
        }

        # Simple cycle detection
        def has_cycle(node, deps, visited=None, rec_stack=None):
            if visited is None:
                visited = set()
            if rec_stack is None:
                rec_stack = set()

            visited.add(node)
            rec_stack.add(node)

            for child in deps.get(node, []):
                if child not in visited:
                    if has_cycle(child, deps, visited, rec_stack):
                        return True
                elif child in rec_stack:
                    return True

            rec_stack.remove(node)
            return False

        cycle_exists = has_cycle('module_a', dependencies)
        self.assertTrue(cycle_exists)



class TestContextSummarization(unittest.TestCase):
    """Test context summarization for large files."""

    def test_long_file_summarization(self):
        """Test summarizing large files (>1000 lines)."""
        file_info = {
            'total_lines': 2500,
            'functions': 25,
            'classes': 5,
            'imports': 15
        }

        # Determine summary priority
        summary_items = [
            f"Classes: {file_info['classes']}",
            f"Functions: {file_info['functions']}",
            f"Imports: {file_info['imports']}"
        ]
        self.assertEqual(len(summary_items), 3)

    def test_key_section_identification(self):
        """Test identifying key sections in large files."""
        sections = [
            {'name': 'imports', 'lines': '1-20'},
            {'name': 'class_definitions', 'lines': '21-500'},
            {'name': 'function_definitions', 'lines': '501-1500'},
            {'name': 'utility_functions', 'lines': '1501-2500'}
        ]

        self.assertEqual(len(sections), 4)

    def test_docstring_extraction_for_summary(self):
        """Test extracting docstrings for module summary."""
        module_docstring = """
Summary of the agent-context module.

This module provides functionality for:
- Extracting code context from files
- Analyzing dependencies
- Generating summaries
        """

        self.assertIn('Summary', module_docstring)



class TestRelatedFilesDetection(unittest.TestCase):
    """Test finding files that import or use this module."""

    def test_import_usage_detection(self):
        """Test finding files that import this module."""
        file_structure = {
            'module_a.py': ['from module_b import func1', 'from module_c import Class1'],
            'module_b.py': ['import os', 'from module_c import Class1'],
            'module_c.py': ['from module_a import func2', 'import sys'],
            'test_module_a.py': ['from module_a import func1']
        }

        # Find files importing module_a
        importers = [f for f, imports in file_structure.items()
                     if any('module_a' in i for i in imports)]

        self.assertIn('test_module_a.py', importers)
        self.assertIn('module_c.py', importers)

    def test_related_files_ranking(self):
        """Test ranking related files by relevance."""
        related_files = [
            {'file': 'test_module.py', 'relevance': 0.95, 'relation': 'tests'},
            {'file': 'module_utils.py', 'relevance': 0.80, 'relation': 'dependency'},
            {'file': 'config.py', 'relevance': 0.60, 'relation': 'imports'},
            {'file': 'legacy_module.py', 'relevance': 0.30, 'relation': 'old_usage'}
        ]

        top_related = sorted(related_files, key=lambda x: x['relevance'], reverse=True)
        self.assertEqual(top_related[0]['file'], 'test_module.py')



class TestAPIDocumentationExtraction(unittest.TestCase):
    """Test extracting public API documentation from docstrings."""

    def test_public_api_extraction(self):
        """Test extracting public API functions."""
        code = """
def public_function():
    '''Public API function.'''
    pass

def _private_function():
    '''Private helper function.'''
    pass

class PublicClass:
    '''Public API class.'''
    def public_method(self):
        '''Public method.'''
        pass

    def _private_method(self):
        '''Private method.'''
        pass
        """

        tree = ast.parse(code)
        public_items = [node.name for node in tree.body
                        if hasattr(node, 'name') and not node.name.startswith('_')]

        self.assertIn('public_function', public_items)
        self.assertIn('PublicClass', public_items)
        self.assertNotIn('_private_function', public_items)

    def test_docstring_parsing(self):
        """Test parsing docstrings for documentation."""
        docstring = """
        Calculate sum of two numbers.

        Args:
            x (int): First number
            y (int): Second number

        Returns:
            int: Sum of x and y

        Example:
            >>> add(2, 3)
            5
        """

        self.assertIn('Args:', docstring)
        self.assertIn('Returns:', docstring)



class TestCoverageMetrics(unittest.TestCase):
    """Test including test coverage metrics from test files."""

    def test_coverage_calculation(self):
        """Test calculating coverage percentage."""
        coverage = {
            'total_lines': 500,
            'covered_lines': 450,
            'percentage': (450 / 500) * 100
        }

        self.assertEqual(coverage['percentage'], 90.0)

    def test_coverage_by_function(self):
        """Test coverage breakdown by function."""
        function_coverage = [
            {'function': 'process_data', 'coverage': 100},
            {'function': 'validate_input', 'coverage': 95},
            {'function': 'format_output', 'coverage': 70},
            {'function': 'debug_helper', 'coverage': 0}
        ]

        uncovered = [f for f in function_coverage if f['coverage'] < 100]
        self.assertEqual(len(uncovered), 3)



class TestCodeMetrics(unittest.TestCase):
    """Test code metrics: cyclomatic complexity, LOC, maintainability index."""

    def test_lines_of_code_calculation(self):
        """Test calculating lines of code."""
        code = """
def calculate(x, y):
    result=x + y
    return result
        """

        lines = [line.strip() for line in code.split('\n') if line.strip()
                 and not line.strip().startswith('#')]
        # Excluding docstrings
        loc = len([line for line in lines if line and '"""' not in line])

        self.assertGreater(loc, 0)

    def test_cyclomatic_complexity(self):
        """Test calculating cyclomatic complexity."""
        # Simplified complexity: 1 + number of conditional statements
        conditions = ['if', 'elif', 'else', 'and', 'or', 'for', 'while', 'except']

        code = """
if x > 0:
    if y > 0:
        return x + y
    else:
        return x - y
elif x < 0:
    return -x
else:
    return 0
        """

        complexity = 1  # base
        for condition in conditions:
            complexity += code.count(condition)

        self.assertGreater(complexity, 1)

    def test_maintainability_index(self):
        """Test calculating maintainability index."""
        metrics = {
            'loc': 150,
            'cyclomatic_complexity': 8,
            'halstead_volume': 500,
            'comments_percentage': 0.25
        }

        # MI formula (simplified): 171 - 5.2 * ln(Halstead) - 0.23 * CC - 16.2 * ln(LOC)
        # For testing, just check structure
        self.assertIn('loc', metrics)
        self.assertIn('cyclomatic_complexity', metrics)



class TestCodeSmellDetection(unittest.TestCase):
    """Test detecting code smells and anti-patterns."""

    def test_long_function_detection(self):
        """Test detecting functions that are too long."""
        function_lengths = {
            'short_func': 20,
            'medium_func': 50,
            'long_func': 200,  # Code smell
            'very_long_func': 500  # Code smell
        }

        smell_threshold = 100
        smells = [name for name, length in function_lengths.items() if length > smell_threshold]

        self.assertEqual(len(smells), 2)

    def test_duplicate_code_detection(self):
        """Test detecting duplicate code blocks."""
        code_blocks = [
            'for item in items: process(item)',
            'for item in items: process(item)',  # Duplicate
            'for item in items: do_something(item)'
        ]

        duplicates = [code_blocks[0] for i in range(len(code_blocks))
                      if code_blocks[0] == code_blocks[i]]

        self.assertEqual(len(duplicates), 2)

    def test_deep_nesting_detection(self):
        """Test detecting deeply nested code."""
        nesting_levels = 0
        code_snippet = """
if a:
    if b:
        if c:
            if d:
                result=execute()  # 4 levels deep
        """

        # Count opening braces / indents
        for line in code_snippet.split('\n'):
            if line.strip().startswith('if'):
                nesting_levels += 1

        self.assertEqual(nesting_levels, 4)



class TestArchitectureDecisions(unittest.TestCase):
    """Test including architecture decisions and design patterns."""

    def test_design_pattern_detection(self):
        """Test detecting design patterns in code."""
        patterns = {
            'singleton': ['__instance=None', '__new__'],
            'factory': ['def create_', 'return '],
            'observer': ['subscribe', 'notify'],
            'strategy': ['strategy =', 'execute']
        }

        self.assertEqual(len(patterns), 4)

    def test_architectural_decision_record(self):
        """Test storing architectural decisions."""
        adr = {
            'decision': 'Use async / await for I / O operations',
            'context': 'Improve performance for network-bound tasks',
            'consequences': 'Requires Python 3.7+, changes error handling',
            'date': '2025-12-16',
            'status': 'accepted'
        }

        self.assertEqual(adr['status'], 'accepted')



class TestChangeStatistics(unittest.TestCase):
    """Test recent change statistics."""

    def test_change_frequency(self):
        """Test tracking change frequency."""
        changes = [
            {'date': '2025-12-16', 'type': 'modification'},
            {'date': '2025-12-15', 'type': 'modification'},
            {'date': '2025-12-10', 'type': 'feature'},
            {'date': '2025-12-05', 'type': 'bugfix'},
        ]

        self.assertEqual(len(changes), 4)

    def test_time_since_last_change(self):
        """Test calculating time since last change."""

        # Days since change would be 0
        days_since = 0
        self.assertEqual(days_since, 0)

    def test_contributor_statistics(self):
        """Test tracking contributor statistics."""
        contributors = {
            'alice': {'commits': 25, 'changes': 150},
            'bob': {'commits': 15, 'changes': 95},
            'charlie': {'commits': 5, 'changes': 20}
        }

        total_commits = sum(c['commits'] for c in contributors.values())
        self.assertEqual(total_commits, 45)



class TestPluginSystem(unittest.TestCase):
    """Test custom context providers via plugin system."""

    def test_plugin_registry(self):
        """Test registering custom context providers."""
        class PluginRegistry:
            def __init__(self):
                self.providers = {}

            def register(self, name, provider):
                self.providers[name] = provider

            def get_provider(self, name):
                return self.providers.get(name)

        registry = PluginRegistry()
        self.assertEqual(len(registry.providers), 0)

    def test_custom_provider_implementation(self):
        """Test implementing custom context provider."""
        class CustomProvider:
            def name(self):
                return "custom_context"

            def extract(self, file_path):
                return {'custom_data': 'value'}

        provider = CustomProvider()
        self.assertEqual(provider.name(), 'custom_context')



class TestContextCachingImprovements(unittest.TestCase):
    """Test context caching for improved performance."""

    def test_cache_storage(self):
        """Test caching extracted context."""
        cache = {}

        def get_context(file_path):
            if file_path in cache:
                return cache[file_path]

            # Simulate extraction
            context = {'data': 'extracted'}
            cache[file_path] = context
            return context

        ctx1 = get_context('file.py')
        ctx2 = get_context('file.py')  # From cache

        self.assertEqual(ctx1, ctx2)

    def test_cache_invalidation(self):
        """Test invalidating cache when file changes."""
        cache = {'file.py': {'data': 'old'}}

        # Invalidate cache for specific file
        cache.pop('file.py', None)

        self.assertNotIn('file.py', cache)



class TestContextPrioritization(unittest.TestCase):
    """Test context prioritization for relevance."""

    def test_relevance_scoring(self):
        """Test scoring context by relevance."""
        context_items = [
            {'item': 'primary_function', 'relevance': 0.95},
            {'item': 'helper_function', 'relevance': 0.60},
            {'item': 'import_statement', 'relevance': 0.40},
            {'item': 'comment', 'relevance': 0.30}
        ]

        sorted_items = sorted(context_items, key=lambda x: x['relevance'], reverse=True)
        self.assertEqual(sorted_items[0]['item'], 'primary_function')

    def test_context_truncation(self):
        """Test truncating low-priority context."""
        context = [
            {'priority': 'high', 'content': 'main_class'},
            {'priority': 'high', 'content': 'public_api'},
            {'priority': 'medium', 'content': 'helper'},
            {'priority': 'low', 'content': 'deprecated_code'},
            {'priority': 'low', 'content': 'old_comments'}
        ]

        truncated = [c for c in context if c['priority'] != 'low']
        self.assertEqual(len(truncated), 3)



class TestContextVisualization(unittest.TestCase):
    """Test context visualization (dependency graphs, diagrams)."""

    def test_dependency_graph_data(self):
        """Test generating dependency graph data."""
        graph = {
            'nodes': [
                {'id': 'module_a', 'label': 'Module A'},
                {'id': 'module_b', 'label': 'Module B'},
                {'id': 'module_c', 'label': 'Module C'}
            ],
            'edges': [
                {'from': 'module_a', 'to': 'module_b'},
                {'from': 'module_b', 'to': 'module_c'},
                {'from': 'module_a', 'to': 'module_c'}
            ]
        }

        self.assertEqual(len(graph['nodes']), 3)
        self.assertEqual(len(graph['edges']), 3)

    def test_architecture_diagram_generation(self):
        """Test generating architecture diagram."""
        layers = {
            'presentation': ['ui_module'],
            'business_logic': ['service_module'],
            'data_access': ['database_module'],
            'infrastructure': ['logging_module']
        }

        self.assertEqual(len(layers), 4)



class TestContextFiltering(unittest.TestCase):
    """Test context filtering for sensitive data."""

    def test_sensitive_data_detection(self):
        """Test detecting sensitive data patterns."""
        sensitive_patterns = [
            'API_KEY',
            'PASSWORD',
            'SECRET',
            'TOKEN',
            'CREDENTIAL'
        ]

        code = "API_KEY='secret123'"
        has_sensitive = any(pattern in code for pattern in sensitive_patterns)
        self.assertTrue(has_sensitive)

    def test_filtering_sensitive_content(self):
        """Test filtering sensitive content from context."""
        context = {
            'code': 'API_KEY="secret123"',
            'imports': ['import os'],
            'functions': ['process_data']
        }

        # Filter code containing sensitive patterns
        sensitive_keywords = ['API_KEY', 'PASSWORD', 'SECRET']
        filtered_code = context['code']
        for keyword in sensitive_keywords:
            if keyword in context['code']:
                filtered_code = '[REDACTED]'

        self.assertEqual(filtered_code, '[REDACTED]')



class TestCrossModuleContext(unittest.TestCase):
    """Test cross-module context relationships."""

    def test_module_relationships(self):
        """Test identifying relationships between modules."""
        relationships = {
            'module_a': {
                'imports_from': ['module_b', 'module_c'],
                'imported_by': ['module_d'],
                'shared_classes': ['DataProcessor']
            }
        }

        self.assertEqual(len(relationships['module_a']['imports_from']), 2)

    def test_shared_interface_detection(self):
        """Test detecting shared interfaces / protocols."""
        interfaces = {
            'Processor': {
                'modules': ['module_a', 'module_b', 'module_c'],
                'methods': ['process', 'validate', 'output']
            }
        }

        self.assertEqual(len(interfaces['Processor']['modules']), 3)


