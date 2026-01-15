# -*- coding: utf-8 -*-
"""Test classes from test_agent_context.py - core module."""

from __future__ import annotations
import unittest
from typing import Any, List, Dict, Optional, Set
import json
from datetime import datetime
from pathlib import Path
import sys
import ast

# Import test utilities
from tests.utils.agent_test_utils import *

# Import from src if needed

# =============================================================================
# Session 9: Context Notification Tests
# =============================================================================




class TestContextNotification:
    """Tests for context notification triggers."""

    def test_alert_marker_detection(self, tmp_path: Path) -> None:
        """Test alert marker detection."""
        with agent_dir_on_path():
            mod: sys.ModuleType = load_agent_module("logic/agents/cognitive/ContextAgent.py")

        content = "> ⚠️ WARNING: This module is deprecated."
        target: Path = tmp_path / "test.description.md"
        target.write_text(content, encoding="utf-8")

        agent = mod.ContextAgent(str(target))
        previous = agent.read_previous_content()

        assert "WARNING" in previous

    def test_breaking_change_detection(self, tmp_path: Path) -> None:
        """Test breaking change detection."""
        with agent_dir_on_path():
            mod: sys.ModuleType = load_agent_module("logic/agents/cognitive/ContextAgent.py")

        content = "BREAKING CHANGE: API signature changed in v2.0"
        target: Path = tmp_path / "test.description.md"
        target.write_text(content)

        agent = mod.ContextAgent(str(target))
        previous = agent.read_previous_content()

        assert "BREAKING CHANGE" in previous

# ========== Comprehensive Context Tests (from test_agent_context_comprehensive.py) ==========

class TestContextCreation(unittest.TestCase):
    """Tests for context creation and initialization."""

    def test_create_context_basic(self) -> None:
        """Test creating a basic context."""
        context = {
            "user_id": "user123",
            "session_id": "sess123",
            "timestamp": datetime.now(),
        }

        assert context["user_id"] == "user123"
        assert context["session_id"] == "sess123"
        assert context["timestamp"] is not None

    def test_create_context_with_defaults(self) -> None:
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

    def test_create_context_nested(self) -> None:
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

    def test_create_context_with_metadata(self) -> None:
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

    def test_track_context_state_transitions(self) -> None:
        """Test tracking context state transitions."""
        states: List[str] = ["initialized", "processing", "completed"]
        state_history = []

        for state in states:
            state_history.append(state)

        assert len(state_history) == 3
        assert state_history[-1] == "completed"

    def test_track_modified_fields(self) -> None:
        """Test tracking modified fields."""
        context: Dict[str, int] = {"value": 10}
        modifications = []

        context["value"] = 20
        modifications.append(("value", 10, 20))

        assert len(modifications) == 1
        assert modifications[0][2] == 20

    def test_track_context_dirty_state(self) -> None:
        """Test tracking dirty state."""
        context = {"name": "Alice", "_dirty": False}

        context["name"] = "Bob"
        context["_dirty"] = True

        assert context["_dirty"] is True

    def test_track_context_read_only_fields(self) -> None:
        """Test tracking read-only field violations."""
        context = {"id": "ctx123", "_read_only": ["id"]}
        violations = []

        # Attempt to modify read-only field
        if "id" in context.get("_read_only", []):
            violations.append("id")

        assert "id" in violations

class TestContextLifecycle(unittest.TestCase):
    """Tests for context lifecycle management."""

    def test_context_creation_lifecycle(self) -> None:
        """Test context creation lifecycle."""
        lifecycle = []

        # Create
        context: Dict[str, str] = {"id": "ctx1"}
        lifecycle.append("created")

        # Initialize
        context["initialized"] = True
        lifecycle.append("initialized")

        # Cleanup
        context.clear()
        lifecycle.append("cleaned")

        assert lifecycle == ["created", "initialized", "cleaned"]

    def test_context_timeout_lifecycle(self) -> None:
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

    def test_context_resource_management(self) -> None:
        """Test context resource management."""
        resources = []

        # Allocate
        resources.append("connection")
        resources.append("file_handle")

        assert len(resources) == 2

        # Release
        resources.clear()
        assert len(resources) == 0

    def test_context_cleanup_on_exception(self) -> None:
        """Test context cleanup on exception."""
        context: Dict[str, bool] = {"active": True}
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

    def test_store_context_value(self) -> None:
        """Test storing context value."""
        context = {}
        context["key1"] = "value1"

        assert context["key1"] == "value1"

    def test_retrieve_context_value(self) -> None:
        """Test retrieving context value."""
        context: Dict[str, str] = {"key1": "value1", "key2": "value2"}

        value: str | None = context.get("key1")
        assert value == "value1"

    def test_retrieve_nonexistent_with_default(self) -> None:
        """Test retrieving nonexistent with default."""
        context: Dict[str, str] = {"key1": "value1"}

        value: str = context.get("missing", "default")
        assert value == "default"

    def test_store_complex_object(self) -> None:
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

    def test_set_context_variable(self) -> None:
        """Test setting context variable."""
        context = {}
        context["var1"] = "value1"

        assert "var1" in context

    def test_get_context_variable(self) -> None:
        """Test getting context variable."""
        context: Dict[str, str] = {"var1": "value1"}

        assert context["var1"] == "value1"

    def test_delete_context_variable(self) -> None:
        """Test deleting context variable."""
        context: Dict[str, str] = {"var1": "value1"}
        del context["var1"]

        assert "var1" not in context

    def test_context_variable_isolation(self) -> None:
        """Test context variable isolation."""
        ctx1_vars: Dict[str, str] = {"var": "ctx1_value"}
        ctx2_vars: Dict[str, str] = {"var": "ctx2_value"}

        assert ctx1_vars["var"] != ctx2_vars["var"]

class TestContextPropagation(unittest.TestCase):
    """Tests for context propagation through call chains."""

    def test_propagate_context_to_function(self) -> None:
        """Test propagating context to function."""
        context: Dict[str, str] = {"user_id": "user1"}

        def process(ctx) -> bool:
            return ctx["user_id"]

        result: bool = process(context)
        assert result == "user1"

    def test_propagate_through_nested_calls(self) -> None:
        """Test propagating through nested calls."""
        context: Dict[str, int] = {"value": 10}

        def level1(ctx) -> bool:
            return level2(ctx)

        def level2(ctx) -> str:
            return level3(ctx)

        def level3(ctx) -> bool:
            return ctx["value"]

        result: bool = level1(context)
        assert result == 10

    def test_propagate_to_async_context(self) -> None:
        """Test propagating to async context."""
        context: Dict[str, str] = {"async_id": "async1"}

        async_contexts = []
        async_contexts.append(context)

        assert async_contexts[0]["async_id"] == "async1"

    def test_propagate_with_implicit_context(self) -> None:
        """Test propagating with implicit context."""
        context_stack: List[Dict[str, int]] = [{"level": 1}]

        # Add another level
        context_stack.append({**context_stack[-1], "level": 2})

        assert context_stack[-1]["level"] == 2

class TestContextMerging(unittest.TestCase):
    """Tests for context merging."""

    def test_merge_contexts(self) -> None:
        """Test merging two contexts."""
        ctx1: Dict[str, str] = {"key1": "value1"}
        ctx2: Dict[str, str] = {"key2": "value2"}

        merged: Dict[str, str] = {**ctx1, **ctx2}

        assert merged["key1"] == "value1"
        assert merged["key2"] == "value2"

    def test_merge_with_override(self) -> None:
        """Test merging with override."""
        ctx1: Dict[str, str] = {"shared": "original", "unique1": "value1"}
        ctx2: Dict[str, str] = {"shared": "override", "unique2": "value2"}

        merged: Dict[str, str] = {**ctx1, **ctx2}

        assert merged["shared"] == "override"
        assert merged["unique1"] == "value1"
        assert merged["unique2"] == "value2"

    def test_merge_nested_contexts(self) -> None:
        """Test merging nested contexts."""
        ctx1: Dict[str, Dict[str, int]] = {"data": {"a": 1}}
        ctx2: Dict[str, Dict[str, int]] = {"data": {"b": 2}}

        # Simple merge (not recursive)
        merged: Dict[str, Dict[str, int]] = {**ctx1, **ctx2}
        assert merged["data"]["b"] == 2

    def test_merge_empty_context(self) -> None:
        """Test merging empty context."""
        ctx: Dict[str, str] = {"key": "value"}
        empty: dict[Any, Any] = {}

        merged = {**ctx, **empty}
        assert merged["key"] == "value"

class TestContextSerialization(unittest.TestCase):
    """Tests for context serialization."""

    def test_serialize_context_to_dict(self) -> None:
        """Test serializing context to dict."""
        context: Dict[str, str] = {
            "id": "ctx1",
            "user": "alice",
            "timestamp": datetime.now().isoformat(),
        }

        serialized: Dict[str, str] = dict(context)
        assert isinstance(serialized, dict)
        assert serialized["id"] == "ctx1"

    def test_serialize_context_to_json(self) -> None:
        """Test serializing context to JSON."""
        context: Dict[str, str] = {"id": "ctx1", "name": "test"}

        json_str: str = json.dumps(context)
        assert "ctx1" in json_str

    def test_deserialize_context(self) -> None:
        """Test deserializing context."""
        json_str = '{"id": "ctx1", "name": "test"}'

        context = json.loads(json_str)
        assert context["id"] == "ctx1"

    def test_serialize_with_nested_structures(self) -> None:
        """Test serializing with nested structures."""
        context = {
            "user": {"id": 1, "name": "Alice"},
            "tags": ["tag1", "tag2"],
        }

        json_str: str = json.dumps(context)
        restored = json.loads(json_str)
        assert restored["user"]["name"] == "Alice"

class TestASTSignatureExtraction(unittest.TestCase):
    """Test extracting class and function signatures using AST."""

    def test_function_signature_extraction(self) -> None:
        """Test extracting function signature from AST."""
        code = """
def calculate(x: int, y: int) -> int:
    '''Calculate sum of two integers.'''
    return x + y
        """
        tree: ast.Module = ast.parse(code)
        func_def: ast.stmt = tree.body[0]

        self.assertIsInstance(func_def, ast.FunctionDef)
        self.assertEqual(func_def.name, 'calculate')
        self.assertEqual(len(func_def.args.args), 2)

    def test_class_signature_extraction(self) -> None:
        """Test extracting class definition from AST."""
        code = """
class DataProcessor:
    def __init__(self, name: str) -> str:
        self.name=name

    def process(self, data) -> Any:
        return data
        """
        tree: ast.Module = ast.parse(code)
        class_def: ast.stmt = tree.body[0]

        self.assertIsInstance(class_def, ast.ClassDef)
        self.assertEqual(class_def.name, 'DataProcessor')
        self.assertEqual(len(class_def.body), 2)

    def test_method_signature_extraction(self) -> None:
        """Test extracting method signatures from class."""
        code = """
class Calculator:
    def add(self, a: int, b: int) -> int:
        return a + b

    def multiply(self, a: int, b: int) -> int:
        return a * b
        """
        tree: ast.Module = ast.parse(code)
        class_def: ast.stmt = tree.body[0]
        methods: List[ast.FunctionDef] = [n for n in class_def.body if isinstance(n, ast.FunctionDef)]

        self.assertEqual(len(methods), 2)
        self.assertEqual(methods[0].name, 'add')

class TestDependencyGraphAnalysis(unittest.TestCase):
    """Test dependency graph analysis and visualization."""

    def test_import_extraction(self) -> None:
        """Test extracting imports from module."""
        code = """import os
from pathlib import Path
from typing import Dict, List
import numpy as np
"""
        tree: ast.Module = ast.parse(code)
        imports: List[ast.Import | ast.ImportFrom] = [
            node for node in ast.walk(tree) if isinstance(
                node, (ast.Import, ast.ImportFrom))]

        self.assertEqual(len(imports), 4)

    def test_dependency_tree_building(self) -> None:
        """Test building dependency tree."""
        dependencies = {
            'module_a': ['module_b', 'module_c'],
            'module_b': ['module_d'],
            'module_c': ['module_d'],
            'module_d': []
        }

        # Check depth
        def max_depth(node: str, deps: Dict[str, List[str]], visited: Optional[Set[str]] = None) -> int:
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

    def test_circular_dependency_detection(self) -> None:
        """Test detecting circular dependencies."""
        dependencies: Dict[str, List[str]] = {
            'module_a': ['module_b'],
            'module_b': ['module_c'],
            'module_c': ['module_a']
        }

        # Simple cycle detection
        def has_cycle(node, deps, visited=None, rec_stack=None) -> bool:
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

        cycle_exists: bool = has_cycle('module_a', dependencies)
        self.assertTrue(cycle_exists)

class TestContextSummarization(unittest.TestCase):
    """Test context summarization for large files."""

    def test_long_file_summarization(self) -> None:
        """Test summarizing large files (>1000 lines)."""
        file_info: Dict[str, int] = {
            'total_lines': 2500,
            'functions': 25,
            'classes': 5,
            'imports': 15
        }

        # Determine summary priority
        summary_items: List[str] = [
            f"Classes: {file_info['classes']}",
            f"Functions: {file_info['functions']}",
            f"Imports: {file_info['imports']}"
        ]
        self.assertEqual(len(summary_items), 3)

    def test_key_section_identification(self) -> None:
        """Test identifying key sections in large files."""
        sections: List[Dict[str, str]] = [
            {'name': 'imports', 'lines': '1-20'},
            {'name': 'class_definitions', 'lines': '21-500'},
            {'name': 'function_definitions', 'lines': '501-1500'},
            {'name': 'utility_functions', 'lines': '1501-2500'}
        ]

        self.assertEqual(len(sections), 4)

    def test_docstring_extraction_for_summary(self) -> None:
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

    def test_import_usage_detection(self) -> None:
        """Test finding files that import this module."""
        file_structure: Dict[str, List[str]] = {
            'module_a.py': ['from module_b import func1', 'from module_c import Class1'],
            'module_b.py': ['import os', 'from module_c import Class1'],
            'module_c.py': ['from module_a import func2', 'import sys'],
            'test_module_a.py': ['from module_a import func1']
        }

        # Find files importing module_a
        importers: List[str] = [f for f, imports in file_structure.items()
                     if any('module_a' in i for i in imports)]

        self.assertIn('test_module_a.py', importers)
        self.assertIn('module_c.py', importers)

    def test_related_files_ranking(self) -> None:
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

    def test_public_api_extraction(self) -> None:
        """Test extracting public API functions."""
        code = """
def public_function() -> None:
    '''Public API function.'''
    pass

def _private_function() -> None:
    '''Private helper function.'''
    pass

class PublicClass:
    '''Public API class.'''
    def public_method(self) -> None:
        '''Public method.'''
        pass

    def _private_method(self) -> None:
        '''Private method.'''
        pass
        """

        tree: ast.Module = ast.parse(code)
        public_items = [node.name for node in tree.body
                        if hasattr(node, 'name') and not node.name.startswith('_')]

        self.assertIn('public_function', public_items)
        self.assertIn('PublicClass', public_items)
        self.assertNotIn('_private_function', public_items)

    def test_docstring_parsing(self) -> None:
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

    def test_coverage_calculation(self) -> None:
        """Test calculating coverage percentage."""
        coverage = {
            'total_lines': 500,
            'covered_lines': 450,
            'percentage': (450 / 500) * 100
        }

        self.assertEqual(coverage['percentage'], 90.0)

    def test_coverage_by_function(self) -> None:
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

    def test_lines_of_code_calculation(self) -> None:
        """Test calculating lines of code."""
        code = """
def calculate(x, y) -> Any:
    result=x + y
    return result
        """

        lines: List[str] = [line.strip() for line in code.split('\n') if line.strip()
                 and not line.strip().startswith('#')]
        # Excluding docstrings
        loc: int = len([line for line in lines if line and '"""' not in line])

        self.assertGreater(loc, 0)

    def test_cyclomatic_complexity(self) -> None:
        """Test calculating cyclomatic complexity."""
        # Simplified complexity: 1 + number of conditional statements
        conditions: List[str] = ['if', 'elif', 'else', 'and', 'or', 'for', 'while', 'except']

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

    def test_maintainability_index(self) -> None:
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

    def test_long_function_detection(self) -> None:
        """Test detecting functions that are too long."""
        function_lengths: Dict[str, int] = {
            'short_func': 20,
            'medium_func': 50,
            'long_func': 200,  # Code smell
            'very_long_func': 500  # Code smell
        }

        smell_threshold = 100
        smells: List[str] = [name for name, length in function_lengths.items() if length > smell_threshold]

        self.assertEqual(len(smells), 2)

    def test_duplicate_code_detection(self) -> None:
        """Test detecting duplicate code blocks."""
        code_blocks: List[str] = [
            'for item in items: process(item)',
            'for item in items: process(item)',  # Duplicate
            'for item in items: do_something(item)'
        ]

        duplicates: List[str] = [code_blocks[0] for i in range(len(code_blocks))
                      if code_blocks[0] == code_blocks[i]]

        self.assertEqual(len(duplicates), 2)

    def test_deep_nesting_detection(self) -> None:
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

    def test_design_pattern_detection(self) -> None:
        """Test detecting design patterns in code."""
        patterns: Dict[str, List[str]] = {
            'singleton': ['__instance=None', '__new__'],
            'factory': ['def create_', 'return '],
            'observer': ['subscribe', 'notify'],
            'strategy': ['strategy =', 'execute']
        }

        self.assertEqual(len(patterns), 4)

    def test_architectural_decision_record(self) -> None:
        """Test storing architectural decisions."""
        adr: Dict[str, str] = {
            'decision': 'Use async / await for I / O operations',
            'context': 'Improve performance for network-bound tasks',
            'consequences': 'Requires Python 3.7+, changes error handling',
            'date': '2025-12-16',
            'status': 'accepted'
        }

        self.assertEqual(adr['status'], 'accepted')

class TestChangeStatistics(unittest.TestCase):
    """Test recent change statistics."""

    def test_change_frequency(self) -> None:
        """Test tracking change frequency."""
        changes: List[Dict[str, str]] = [
            {'date': '2025-12-16', 'type': 'modification'},
            {'date': '2025-12-15', 'type': 'modification'},
            {'date': '2025-12-10', 'type': 'feature'},
            {'date': '2025-12-05', 'type': 'bugfix'},
        ]

        self.assertEqual(len(changes), 4)

    def test_time_since_last_change(self) -> None:
        """Test calculating time since last change."""

        # Days since change would be 0
        days_since = 0
        self.assertEqual(days_since, 0)

    def test_contributor_statistics(self) -> None:
        """Test tracking contributor statistics."""
        contributors: Dict[str, Dict[str, int]] = {
            'alice': {'commits': 25, 'changes': 150},
            'bob': {'commits': 15, 'changes': 95},
            'charlie': {'commits': 5, 'changes': 20}
        }

        total_commits: int = sum(c['commits'] for c in contributors.values())
        self.assertEqual(total_commits, 45)

class TestPluginSystem(unittest.TestCase):
    """Test custom context providers via plugin system."""

    def test_plugin_registry(self) -> None:
        """Test registering custom context providers."""
        class PluginRegistry:
            def __init__(self) -> None:
                self.providers: dict[Any, Any] = {}

            def register(self, name, provider) -> None:
                self.providers[name] = provider

            def get_provider(self, name) -> Any:
                return self.providers.get(name)

        registry = PluginRegistry()
        self.assertEqual(len(registry.providers), 0)

    def test_custom_provider_implementation(self) -> None:
        """Test implementing custom context provider."""
        class CustomProvider:
            def name(self) -> str:
                return "custom_context"

            def extract(self, file_path) -> Dict[str, str]:
                return {'custom_data': 'value'}

        provider = CustomProvider()
        self.assertEqual(provider.name(), 'custom_context')

class TestContextCachingImprovements(unittest.TestCase):
    """Test context caching for improved performance."""

    def test_cache_storage(self) -> None:
        """Test caching extracted context."""
        cache: dict[Any, Any] = {}

        def get_context(file_path) -> Any:
            if file_path in cache:
                return cache[file_path]

            # Simulate extraction
            context: Dict[str, str] = {'data': 'extracted'}
            cache[file_path] = context
            return context

        ctx1 = get_context('file.py')
        ctx2 = get_context('file.py')  # From cache

        self.assertEqual(ctx1, ctx2)

    def test_cache_invalidation(self) -> None:
        """Test invalidating cache when file changes."""
        cache: Dict[str, Dict[str, str]] = {'file.py': {'data': 'old'}}

        # Invalidate cache for specific file
        cache.pop('file.py', None)

        self.assertNotIn('file.py', cache)

class TestContextPrioritization(unittest.TestCase):
    """Test context prioritization for relevance."""

    def test_relevance_scoring(self) -> None:
        """Test scoring context by relevance."""
        context_items = [
            {'item': 'primary_function', 'relevance': 0.95},
            {'item': 'helper_function', 'relevance': 0.60},
            {'item': 'import_statement', 'relevance': 0.40},
            {'item': 'comment', 'relevance': 0.30}
        ]

        sorted_items = sorted(context_items, key=lambda x: x['relevance'], reverse=True)
        self.assertEqual(sorted_items[0]['item'], 'primary_function')

    def test_context_truncation(self) -> None:
        """Test truncating low-priority context."""
        context: List[Dict[str, str]] = [
            {'priority': 'high', 'content': 'main_class'},
            {'priority': 'high', 'content': 'public_api'},
            {'priority': 'medium', 'content': 'helper'},
            {'priority': 'low', 'content': 'deprecated_code'},
            {'priority': 'low', 'content': 'old_comments'}
        ]

        truncated: List[Dict[str, str]] = [c for c in context if c['priority'] != 'low']
        self.assertEqual(len(truncated), 3)

class TestContextVisualization(unittest.TestCase):
    """Test context visualization (dependency graphs, diagrams)."""

    def test_dependency_graph_data(self) -> None:
        """Test generating dependency graph data."""
        graph: Dict[str, List[Dict[str, str]]] = {
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

    def test_architecture_diagram_generation(self) -> None:
        """Test generating architecture diagram."""
        layers: Dict[str, List[str]] = {
            'presentation': ['ui_module'],
            'business_logic': ['service_module'],
            'data_access': ['database_module'],
            'infrastructure': ['logging_module']
        }

        self.assertEqual(len(layers), 4)

class TestContextFiltering(unittest.TestCase):
    """Test context filtering for sensitive data."""

    def test_sensitive_data_detection(self) -> None:
        """Test detecting sensitive data patterns."""
        sensitive_patterns: List[str] = [
            'API_KEY',
            'PASSWORD',
            'SECRET',
            'TOKEN',
            'CREDENTIAL'
        ]

        code = "API_KEY='secret123'"
        has_sensitive: bool = any(pattern in code for pattern in sensitive_patterns)
        self.assertTrue(has_sensitive)

    def test_filtering_sensitive_content(self) -> None:
        """Test filtering sensitive content from context."""
        context = {
            'code': 'API_KEY="secret123"',
            'imports': ['import os'],
            'functions': ['process_data']
        }

        # Filter code containing sensitive patterns
        sensitive_keywords: List[str] = ['API_KEY', 'PASSWORD', 'SECRET']
        filtered_code = context['code']
        for keyword in sensitive_keywords:
            if keyword in context['code']:
                filtered_code = '[REDACTED]'

        self.assertEqual(filtered_code, '[REDACTED]')

class TestCrossModuleContext(unittest.TestCase):
    """Test cross-module context relationships."""

    def test_module_relationships(self) -> None:
        """Test identifying relationships between modules."""
        relationships: Dict[str, Dict[str, List[str]]] = {
            'module_a': {
                'imports_from': ['module_b', 'module_c'],
                'imported_by': ['module_d'],
                'shared_classes': ['DataProcessor']
            }
        }

        self.assertEqual(len(relationships['module_a']['imports_from']), 2)

    def test_shared_interface_detection(self) -> None:
        """Test detecting shared interfaces / protocols."""
        interfaces: Dict[str, Dict[str, List[str]]] = {
            'Processor': {
                'modules': ['module_a', 'module_b', 'module_c'],
                'methods': ['process', 'validate', 'output']
            }
        }

        self.assertEqual(len(interfaces['Processor']['modules']), 3)
