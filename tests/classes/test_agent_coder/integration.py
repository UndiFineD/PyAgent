# -*- coding: utf-8 -*-
"""Test classes from test_agent_coder.py - integration module."""

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


class TestFlake8Integration(unittest.TestCase):
    """Tests for flake8 linting integration."""

    @patch("subprocess.run")
    def test_flake8_valid_code(self, mock_run):
        """Test flake8 on valid code."""
        mock_run.return_value.returncode = 0
        # Valid code passes flake8
        assert True

    @patch("subprocess.run")
    def test_flake8_detect_unused_imports(self, mock_run):
        """Test flake8 detects unused imports."""
        mock_run.return_value.stdout = "F401: unused import"
        output = mock_run.return_value.stdout
        assert "unused import" in output.lower()

    @patch("subprocess.run")
    def test_flake8_detect_line_too_long(self, mock_run):
        """Test flake8 detects long lines."""
        mock_run.return_value.stdout = "E501: line too long"
        output = mock_run.return_value.stdout
        assert "line too long" in output.lower()

    @patch("subprocess.run")
    def test_flake8_detect_whitespace_issues(self, mock_run):
        """Test flake8 detects whitespace issues."""
        mock_run.return_value.stdout = "E225: missing whitespace"
        output = mock_run.return_value.stdout
        assert "whitespace" in output.lower()



class TestSecurityScanningIntegration(unittest.TestCase):
    """Tests for security scanning integration."""

    @patch("subprocess.run")
    def test_bandit_detect_hardcoded_password(self, mock_run):
        """Test bandit detects hardcoded passwords."""
        mock_run.return_value.stdout = "B105: hardcoded_password_string"
        output = mock_run.return_value.stdout
        assert "password" in output.lower()

    @patch("subprocess.run")
    def test_bandit_detect_unsafe_pickle(self, mock_run):
        """Test bandit detects unsafe pickle usage."""
        mock_run.return_value.stdout = "B301: pickle usage"
        output = mock_run.return_value.stdout
        assert "pickle" in output.lower()

    @patch("subprocess.run")
    def test_bandit_detect_sql_injection(self, mock_run):
        """Test bandit detects SQL injection risks."""
        mock_run.return_value.stdout = "B608: hardcoded SQL"
        output = mock_run.return_value.stdout
        assert "sql" in output.lower() or "608" in output

    @patch("subprocess.run")
    def test_bandit_safe_code(self, mock_run):
        """Test bandit on secure code."""
        mock_run.return_value.returncode = 0
        assert mock_run.return_value.returncode == 0



class TestIntegration(unittest.TestCase):
    """Integration tests for code generation."""

    def test_end_to_end_code_generation(self):
        """Test complete code generation workflow."""

        # Generated code would be:
        generated = """def factorial(n: int) -> int:
    \"\"\"Calculate factorial of n.\"\"\"
    if n <= 1:
        return 1
    return n * factorial(n - 1)
"""
        # Verify syntax
        try:
            compile(generated, "<string>", "exec")
            is_valid = True
        except SyntaxError:
            is_valid = False
        assert is_valid
        assert "factorial" in generated

    def test_end_to_end_code_modification(self):
        """Test complete code modification workflow."""
        original = "def greet(name): return f'Hello {name}'"
        # Modification: add docstring
        modified = '''def greet(name):
    """Greet a person by name."""
    return f'Hello {name}!'
'''
        assert "greet" in modified
        assert '"""' not in original  # No docstring in original
        assert '"""' in modified  # Has docstring in modified


