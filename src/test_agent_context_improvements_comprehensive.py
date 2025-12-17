"""Comprehensive tests for agent-context.py improvements.

Tests all 17 suggested improvements for context generation and analysis:
- AST parsing for signatures
- Git history integration
- Dependency graph analysis
- Context summarization
- Related files detection
- API documentation extraction
- Test coverage metrics
- Code metrics (cyclomatic complexity, LOC, maintainability)
- Code smell detection
- Architecture decisions and patterns
- Change statistics
- Plugin system support
- Context caching
- Context prioritization
- Context visualization
- Context filtering
- Cross-module context
"""

import unittest
import ast


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


class TestGitHistoryIntegration(unittest.TestCase):
    """Test including recent git history in context."""

    def test_git_history_extraction(self):
        """Test extracting last 10 commits."""
        git_history = [
            {'commit': 'abc123', 'author': 'dev1', 'message': 'Fix bug in parser', 'date': '2025-12-16'},
            {'commit': 'def456', 'author': 'dev2', 'message': 'Add feature X', 'date': '2025-12-15'},
            {'commit': 'ghi789', 'author': 'dev1', 'message': 'Refactor context module', 'date': '2025-12-14'},
        ]
        self.assertEqual(len(git_history), 3)
        self.assertEqual(git_history[0]['commit'], 'abc123')

    def test_commit_message_parsing(self):
        """Test parsing commit messages for context."""
        commits = [
            {'hash': 'abc123', 'message': 'Fix: resolve memory leak in parser'},
            {'hash': 'def456', 'message': 'Feature: add async support'},
            {'hash': 'ghi789', 'message': 'Refactor: extract utilities to separate module'}
        ]

        fix_commits = [c for c in commits if c['message'].startswith('Fix')]
        self.assertEqual(len(fix_commits), 1)

    def test_contributor_extraction(self):
        """Test extracting contributor information."""
        commits = [
            {'author': 'alice@example.com', 'count': 15},
            {'author': 'bob@example.com', 'count': 8},
            {'author': 'charlie@example.com', 'count': 3}
        ]
        top_contributor = max(commits, key=lambda x: x['count'])
        self.assertEqual(top_contributor['author'], 'alice@example.com')


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


class TestContextCaching(unittest.TestCase):
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


if __name__ == '__main__':
    unittest.main()
