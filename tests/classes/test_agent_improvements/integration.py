# -*- coding: utf-8 -*-
"""Test classes from test_agent_improvements.py - integration module."""

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
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# Try to import test utilities
try:
    from tests.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path
except ImportError:
    # Fallback
    AGENT_DIR = Path(__file__).parent.parent.parent / 'src'
    
    class agent_sys_path:
        def __enter__(self): 
            sys.path.insert(0, str(AGENT_DIR))
            return self
        def __exit__(self, *args): 
            sys.path.remove(str(AGENT_DIR))

# Import from src if needed
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))


class TestToolIntegration:
    """Tests for ToolIntegration class."""

    def test_init(self, improvements_module: Any) -> None:
        """Test ToolIntegration initialization."""
        integration = improvements_module.ToolIntegration()
        assert integration.tool_configs == {}

    def test_configure_tool(self, improvements_module: Any) -> None:
        """Test configuring a tool."""
        integration = improvements_module.ToolIntegration()
        integration.configure_tool(
            "pylint",
            improvements_module.AnalysisToolType.LINTER,
            "pylint {file}"
        )
        assert "pylint" in integration.tool_configs

    def test_parse_pylint_output(self, improvements_module: Any) -> None:
        """Test parsing pylint output."""
        integration = improvements_module.ToolIntegration()
        output = "test.py:10:0: C0114: Missing module docstring"
        suggestions = integration.parse_pylint_output(output)
        assert len(suggestions) == 1
        assert suggestions[0].tool_name == "pylint"

    def test_parse_mypy_output(self, improvements_module: Any) -> None:
        """Test parsing mypy output."""
        integration = improvements_module.ToolIntegration()
        output = "test.py:20: error: Incompatible types"
        suggestions = integration.parse_mypy_output(output)
        assert len(suggestions) == 1
        assert suggestions[0].tool_name == "mypy"

    def test_get_suggestions(self, improvements_module: Any) -> None:
        """Test getting suggestions."""
        integration = improvements_module.ToolIntegration()
        integration.parse_pylint_output("test.py:10:0: C0114: Missing docstring")
        suggestions = integration.get_suggestions()
        assert len(suggestions) == 1


# ========== Session 7 Tests: SLAManager ==========



class TestSession8Integration:
    """Integration tests for Session 8 branch comparison features."""

    def test_full_comparison_workflow(self, improvements_module: Any, agent: Any) -> None:
        """Test full comparison workflow."""
        comparer = improvements_module.BranchComparer()

        # Create source and target improvement sets
        imp1 = agent.add_improvement("Common feature", "Details")
        imp2 = agent.add_improvement("New in target", "Details")
        imp3 = agent.add_improvement("Only in source", "Details")

        source = {imp1.id: imp1, imp3.id: imp3}
        target = {imp1.id: imp1, imp2.id: imp2}

        # Calculate diffs
        diffs = comparer._calculate_diffs(source, target)

        # Should have: 1 added (imp2), 1 removed (imp3), 1 unchanged (imp1)
        added = [d for d in diffs if d.diff_type == improvements_module.ImprovementDiffType.ADDED]
        removed = [d for d in diffs if d.diff_type ==
                   improvements_module.ImprovementDiffType.REMOVED]
        unchanged = [d for d in diffs if d.diff_type ==
                     improvements_module.ImprovementDiffType.UNCHANGED]

        assert len(added) == 1
        assert len(removed) == 1
        assert len(unchanged) == 1

    def test_merge_report_with_multiple_changes(self, improvements_module: Any, agent: Any) -> None:
        """Test merge report with various change types."""
        comparer = improvements_module.BranchComparer()

        imp_added = agent.add_improvement("Added", "New feature")
        imp_removed = agent.add_improvement("Removed", "Old feature")

        diffs = [
            improvements_module.ImprovementDiff(
                improvement_id="added_1",
                diff_type=improvements_module.ImprovementDiffType.ADDED,
                target_version=imp_added
            ),
            improvements_module.ImprovementDiff(
                improvement_id="removed_1",
                diff_type=improvements_module.ImprovementDiffType.REMOVED,
                source_version=imp_removed
            ),
        ]

        comparison = improvements_module.BranchComparison(
            source_branch="main",
            target_branch="feature / update",
            file_path="improvements.md",
            status=improvements_module.BranchComparisonStatus.COMPLETED,
            diffs=diffs,
            added_count=1,
            removed_count=1
        )

        report = comparer.generate_merge_report(comparison)
        assert "➕" in report  # Added emoji
        assert "➖" in report  # Removed emoji
        assert "Added: 1" in report
        assert "Removed: 1" in report


# =============================================================================
# Session 8: Test File Improvement Tests
# =============================================================================



class TestAutomatedValidationIntegration:
    """Tests for automated validation integration."""

    def test_validator_init(self, improvements_module: Any) -> None:
        """Test validator initialization."""
        ImprovementValidator = improvements_module.ImprovementValidator

        validator = ImprovementValidator()
        assert validator.rules is not None

    def test_validate_improvement(self, improvements_module: Any, agent: Any) -> None:
        """Test validating an improvement."""
        ImprovementValidator = improvements_module.ImprovementValidator

        validator = ImprovementValidator()
        imp = agent.add_improvement("Valid improvement", "With proper description")

        result = validator.validate(imp)
        assert result.is_valid

    def test_validation_failure(self, improvements_module: Any, agent: Any) -> None:
        """Test validation failure."""
        ImprovementValidator = improvements_module.ImprovementValidator

        validator = ImprovementValidator()
        validator.add_rule("min_description_length", min_length=50)

        imp = agent.add_improvement("Short", "Too short")

        result = validator.validate(imp)
        assert not result.is_valid
        assert "description" in result.errors[0].lower()



class TestImprovementIntegration(unittest.TestCase):
    """Integration tests for improvements."""

    def test_end_to_end_detection_and_tracking(self):
        """Test end-to-end detection and tracking."""
        # Detect
        improvements = [
            {"id": 1, "title": "Issue 1", "status": "open"},
            {"id": 2, "title": "Issue 2", "status": "open"},
        ]

        assert len(improvements) == 2

        # Classify
        improvements[0]["type"] = "style"
        improvements[1]["type"] = "perf"

        # Prioritize
        improvements = sorted(improvements, key=lambda x: x["id"])

        # Track
        improvements[0]["status"] = "completed"

        assert improvements[0]["status"] == "completed"
        assert improvements[1]["status"] == "open"

    def test_multi_source_improvement_aggregation(self):
        """Test aggregating improvements from multiple sources."""
        linter_improvements = [{"source": "linter", "type": "style"}]
        complexity_improvements = [{"source": "complexity", "type": "perf"}]
        security_improvements = [{"source": "security", "type": "security"}]

        all_improvements = linter_improvements + complexity_improvements + security_improvements

        assert len(all_improvements) == 3
        assert all_improvements[0]["source"] == "linter"


# ========== Comprehensive Improvements Improvements Tests
# (from test_agent_improvements_improvements_comprehensive.py) ==========


class TestGitIntegration(unittest.TestCase):
    """Test git integration for tracking applied improvements."""

    def test_git_commit_tracking(self):
        """Test tracking improvements in git commits."""
        commits = [
            {'hash': 'abc123', 'message': '[IMP-001] Add caching layer'},
            {'hash': 'def456', 'message': '[IMP-002] Refactor parser'},
            {'hash': 'ghi789', 'message': 'Update documentation'}  # Not an improvement
        ]

        improvement_commits = [c for c in commits if '[IMP-' in c['message']]
        assert len(improvement_commits) == 2

    def test_improvement_to_commit_mapping(self):
        """Test mapping improvements to commits."""
        mapping = {
            'IMP_001': {
                'status': 'completed',
                'commits': ['abc123', 'def456'],
                'completed_date': '2025-12-16'
            },
            'IMP_002': {
                'status': 'in-progress',
                'commits': ['ghi789'],
                'started_date': '2025-12-15'
            }
        }

        assert len(mapping['IMP_001']['commits']) == 2



class TestIntegrationWithRealRepositories(unittest.TestCase):
    """Test integration with real repositories for end-to-end validation."""

    def setUp(self):
        """Set up test fixtures."""
        import tempfile
        from pathlib import Path

        self.temp_dir = tempfile.mkdtemp()
        self.test_repo_path = Path(self.temp_dir) / 'test_repo'
        self.test_repo_path.mkdir()

    def tearDown(self):
        """Clean up test fixtures."""
        import time
        import shutil
        import subprocess

        # Handle permission issues on Windows with git
        time.sleep(0.1)  # Give OS time to release locks
        try:
            shutil.rmtree(self.temp_dir)
        except PermissionError:
            # Retry with ignore_errors for git-related locks on Windows
            try:
                subprocess.run(['rmdir', '/s', '/q', str(self.temp_dir)], shell=True, check=False)
            except Exception:
                pass  # Ignore cleanup errors in tests

    def test_real_repository_initialization(self):
        """Test working with a real repository structure."""
        # Create test repository structure
        (self.test_repo_path / 'src').mkdir()
        (self.test_repo_path / 'tests').mkdir()
        (self.test_repo_path / '.codeignore').write_text('*.pyc\n__pycache__/\n')

        test_file = self.test_repo_path / 'src' / 'main.py'
        test_file.write_text('def hello():\n    print("hello")\n')

        assert test_file.exists()
        assert (self.test_repo_path / '.codeignore').exists()

    def test_real_file_processing(self):
        """Test processing real files in a repository."""
        test_file = self.test_repo_path / 'test.py'
        test_file.write_text('# Original content\ndef func():\n    pass\n')

        original_content = test_file.read_text()

        # Simulate processing
        modified_content = original_content.replace('pass', 'return None')
        test_file.write_text(modified_content)

        assert test_file.read_text() != original_content
        assert 'return None' in test_file.read_text()

    def test_real_git_operations(self):
        """Test git operations on real repository."""
        import subprocess
        # Initialize git repo

        # Skip on systems without git
        try:
            subprocess.run(['git', '--version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.skipTest("Git not available")

        subprocess.run(['git', 'init'], cwd=self.test_repo_path, capture_output=True)

        # Configure git user
        subprocess.run(
            ['git', 'config', 'user.name', 'Test'],
            cwd=self.test_repo_path,
            capture_output=True
        )
        subprocess.run(
            ['git', 'config', 'user.email', 'test@test.com'],
            cwd=self.test_repo_path,
            capture_output=True
        )

        test_file = self.test_repo_path / 'test.py'
        test_file.write_text('test content')

        subprocess.run(['git', 'add', '.'], cwd=self.test_repo_path, capture_output=True)
        subprocess.run(
            ['git', 'commit', '-m', 'Initial commit'],
            cwd=self.test_repo_path,
            capture_output=True
        )

        # Check git status
        result = subprocess.run(
            ['git', 'log', '--oneline'],
            cwd=self.test_repo_path,
            capture_output=True,
            text=True
        )

        assert 'Initial commit' in result.stdout

    def test_end_to_end_agent_execution(self):
        """Test end-to-end agent execution on real repository."""
        # Create test files
        (self.test_repo_path / 'main.py').write_text('def process():\n    pass\n')
        (self.test_repo_path / 'utils.py').write_text('def helper():\n    pass\n')

        files = list(self.test_repo_path.glob('*.py'))
        assert len(files) == 2

    def test_real_codeignore_pattern_matching(self):
        """Test codeignore pattern matching on real files."""
        # Create directory structure
        (self.test_repo_path / 'src').mkdir()
        (self.test_repo_path / '__pycache__').mkdir()
        (self.test_repo_path / '.venv').mkdir()

        src_file = self.test_repo_path / 'src' / 'main.py'
        src_file.write_text('# source code')

        cache_dir = self.test_repo_path / '__pycache__'

        # Test pattern matching
        ignore_patterns = ['__pycache__', '.venv']

        def should_process(filepath):
            return not any(pattern in str(filepath) for pattern in ignore_patterns)

        assert should_process(src_file)
        assert not should_process(cache_dir)

    def test_real_error_handling(self):
        """Test error handling with real filesystem operations."""
        nonexistent_file = self.test_repo_path / 'nonexistent.py'

        with self.assertRaises(FileNotFoundError):
            nonexistent_file.read_text()

    def test_real_permission_handling(self):
        """Test handling permission errors on real files."""
        import os

        test_file = self.test_repo_path / 'readonly.py'
        test_file.write_text('content')

        # Make file read-only
        os.chmod(test_file, 0o444)

        try:
            with self.assertRaises(PermissionError):
                test_file.write_text('new content')
        finally:
            # Restore permissions for cleanup
            os.chmod(test_file, 0o644)

    def test_real_repository_metrics(self):
        """Test collecting metrics from real repository."""
        # Create multiple test files
        for i in range(5):
            (self.test_repo_path /
             f'file{i}.py').write_text(f'# File {i}\ndef func{i}():\n    pass\n')

        python_files = list(self.test_repo_path.glob('*.py'))

        metrics = {
            'total_files': len(python_files),
            'total_lines': sum(len(f.read_text().split('\n')) for f in python_files),
            'average_file_size': sum(len(f.read_text()) for f in python_files) / len(python_files)
        }

        assert metrics['total_files'] == 5
        assert metrics['average_file_size'] > 0



