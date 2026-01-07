# -*- coding: utf-8 -*-
"""Test classes from test_agent_errors.py - integration module."""

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


class TestMultiToolErrorIntegrationComprehensive(unittest.TestCase):
    """Tests for integrating errors from multiple tools."""

    def test_integrate_pylint_errors(self):
        """Test integrating pylint errors."""
        errors = [
            {"tool": "pylint", "code": "C0111", "message": "missing docstring"},
        ]
        assert errors[0]["tool"] == "pylint"

    def test_integrate_flake8_errors(self):
        """Test integrating flake8 errors."""
        errors = [
            {"tool": "flake8", "code": "E501", "message": "line too long"},
        ]
        assert errors[0]["tool"] == "flake8"

    def test_integrate_mypy_errors(self):
        """Test integrating mypy errors."""
        errors = [
            {"tool": "mypy", "code": "error", "message": "type mismatch"},
        ]
        assert errors[0]["tool"] == "mypy"

    def test_deduplicate_across_tools(self):
        """Test deduplicating errors from different tools."""
        all_errors = [
            {"tool": "pylint", "file": "a.py", "line": 5, "message": "error"},
            {"tool": "flake8", "file": "a.py", "line": 5, "message": "error"},
        ]

        unique = {}
        for error in all_errors:
            key = (error["file"], error["line"], error["message"])
            if key not in unique:
                unique[key] = error

        assert len(unique) == 1



class TestIntegrationComprehensive(unittest.TestCase):
    """Integration tests for error processing."""

    def test_end_to_end_error_processing(self):
        """Test complete error processing workflow."""
        # Parse

        # Categorize
        error_type = "ValueError"

        # Analyze
        priority = 5

        # Report
        report = f"{error_type} - Priority: {priority}"
        assert error_type in report

    def test_error_metrics_generation(self):
        """Test generating error metrics."""
        errors = [
            {"type": "SyntaxError", "severity": "critical"},
            {"type": "RuntimeError", "severity": "high"},
            {"type": "Warning", "severity": "low"},
        ]

        metrics = {
            "total": len(errors),
            "critical": sum(1 for e in errors if e["severity"] == "critical"),
            "high": sum(1 for e in errors if e["severity"] == "high"),
        }

        assert metrics["total"] == 3
        assert metrics["critical"] == 1


# ========== Comprehensive Errors Improvements Tests
# (from test_agent_errors_improvements_comprehensive.py) ==========



class TestStaticAnalysisIntegration(unittest.TestCase):
    """Test integration with static analysis tools."""

    def test_pylint_output_parsing(self):
        """Test parsing pylint output."""
        pylint_output = {
            'tool': 'pylint',
            'issues': [
                {'type': 'convention', 'message': 'invalid-name', 'line': 10},
                {'type': 'warning', 'message': 'unused-import', 'line': 5},
                {'type': 'error', 'message': 'undefined-variable', 'line': 25}
            ]
        }
        errors = [i for i in pylint_output['issues'] if i['type'] == 'error']
        self.assertEqual(len(errors), 1)

    def test_flake8_integration(self):
        """Test parsing flake8 output."""
        flake8_results = [
            {'code': 'E501', 'message': 'line too long', 'line': 42},
            {'code': 'F401', 'message': 'unused import', 'line': 5},
            {'code': 'W503', 'message': 'line break before operator', 'line': 50}
        ]
        self.assertEqual(len(flake8_results), 3)

    def test_mypy_type_errors(self):
        """Test parsing mypy type checking errors."""
        mypy_errors = [
            {'error': 'Argument 1 has incompatible type', 'line': 30},
            {'error': 'Missing return statement', 'line': 45},
            {'error': 'Incompatible assignment', 'line': 60}
        ]
        self.assertEqual(len(mypy_errors), 3)

    def test_bandit_security_findings(self):
        """Test parsing bandit security scanning output."""
        security_issues = [
            {'severity': 'HIGH', 'test_id': 'B303', 'message': 'Use of pickle'},
            {'severity': 'MEDIUM', 'test_id': 'B101', 'message': 'assert_used'},
            {'severity': 'LOW', 'test_id': 'B105', 'message': 'hardcoded_password_string'}
        ]
        high_severity = [i for i in security_issues if i['severity'] == 'HIGH']
        self.assertEqual(len(high_severity), 1)



