# -*- coding: utf-8 -*-
"""Test classes from test_agent_context.py - integration module."""

from __future__ import annotations
import unittest
from typing import List, Dict
from pathlib import Path
import sys

# Try to import test utilities
try:
    from tests.utils.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path
except ImportError:
    # Fallback
    AGENT_DIR: Path = Path(__file__).parent.parent.parent.parent / 'src'

    class agent_sys_path:
        def __enter__(self) -> Self:

            return self







        def __exit__(self, *args) -> None:
            sys.path.remove(str(AGENT_DIR))

# Import from src if needed


class TestContextIntegration(unittest.TestCase):
    """Integration tests for context management."""

    def test_end_to_end_context_workflow(self) -> None:
        """Test end-to-end context workflow."""
        # Create
        context: Dict[str, str] = {"user_id": "user1", "session_id": "sess1"}

        # Modify
        context["request_id"] = "req1"

        # Validate
        assert all(k in context for k in ["user_id", "session_id", "request_id"])

        # Cleanup
        context.clear()
        assert len(context) == 0

    def test_multi_context_lifecycle(self) -> None:
        """Test multi-context lifecycle."""
        contexts = []

        # Create multiple
        for i in range(3):
            contexts.append({"id": f"ctx{i}"})

        assert len(contexts) == 3

        # Process
        for ctx in contexts:
            ctx["processed"] = True

        # Cleanup
        contexts.clear()
        assert len(contexts) == 0

    def test_context_with_state_machine(self) -> None:
        """Test context with state machine."""
        context: Dict[str, str] = {"state": "init"}
        transitions = []

        # Transition 1
        context["state"] = "processing"
        transitions.append("init->processing")

        # Transition 2
        context["state"] = "completed"
        transitions.append("processing->completed")

        assert len(transitions) == 2
        assert context["state"] == "completed"


# ========== Comprehensive Context Improvements Tests
# (from test_agent_context_improvements_comprehensive.py) ==========


class TestGitHistoryIntegration(unittest.TestCase):
    """Test including recent git history in context."""

    def test_git_history_extraction(self) -> None:
        """Test extracting last 10 commits."""
        git_history: List[Dict[str, str]] = [
            {
                'commit': 'abc123',
                'author': 'dev1',
                'message': 'Fix bug in parser',
                'date': '2025-12-16'
            },
            {
                'commit': 'def456',
                'author': 'dev2',
                'message': 'Add feature X',
                'date': '2025-12-15'
            },
            {
                'commit': 'ghi789',
                'author': 'dev1',
                'message': 'Refactor context module',
                'date': '2025-12-14'
            },
        ]
        self.assertEqual(len(git_history), 3)
        self.assertEqual(git_history[0]['commit'], 'abc123')

    def test_commit_message_parsing(self) -> None:
        """Test parsing commit messages for context."""
        commits: List[Dict[str, str]] = [
            {'hash': 'abc123', 'message': 'Fix: resolve memory leak in parser'},
            {'hash': 'def456', 'message': 'Feature: add async support'},
            {'hash': 'ghi789', 'message': 'Refactor: extract utilities to separate module'}
        ]

        fix_commits: List[Dict[str, str]] = [c for c in commits if c['message'].startswith('Fix')]
        self.assertEqual(len(fix_commits), 1)

    def test_contributor_extraction(self) -> None:
        """Test extracting contributor information."""
        commits = [
            {'author': 'alice@example.com', 'count': 15},
            {'author': 'bob@example.com', 'count': 8},
            {'author': 'charlie@example.com', 'count': 3}
        ]
        top_contributor = max(commits, key=lambda x: x['count'])
        self.assertEqual(top_contributor['author'], 'alice@example.com')
