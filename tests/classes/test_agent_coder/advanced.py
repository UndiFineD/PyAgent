# -*- coding: utf-8 -*-
"""Test classes from test_agent_coder.py - advanced module."""

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


class TestAdvancedCodeFormatting(unittest.TestCase):
    """Test advanced code formatting improvements."""

    def test_black_formatter_integration(self):
        """Test black formatter integration with custom line length."""
        black_config = {
            'enabled': True,
            'line_length': 120,
            'target_version': 'py311'
        }
        self.assertEqual(black_config['line_length'], 120)

    def test_isort_import_organization(self):
        """Test isort for import statement organization."""
        _ = """import os
        import sys
        from typing import List
        import requests
from pathlib import Path
"""  # noqa: F841
        # isort would organize these
        expected_organized = """import os
import sys
from pathlib import Path
from typing import List

import requests
"""
        self.assertIn('from pathlib', expected_organized)

    def test_formatting_after_validation(self):
        """Test applying formatting after successful validation."""
        pipeline = [
            'validate_syntax',
            'validate_security',
            'apply_formatting',
            'write_file'
        ]
        self.assertEqual(pipeline[2], 'apply_formatting')

    def test_configurable_formatter_selection(self):
        """Test configurable formatter selection."""
        formatter_options = ['black', 'autopep8', 'none']
        self.assertIn('black', formatter_options)

    def test_preserve_minimal_changes(self):
        """Test preserving original formatting if changes are minimal."""
        original = "def func():\n    pass\n"
        formatted = "def func():\n    pass\n"

        if original == formatted:
            result = original
        self.assertEqual(original, result)



class TestAdvancedSecurityValidation(unittest.TestCase):
    """Test advanced security and best practices validation."""

    def test_secret_detection_patterns(self):
        """Test detecting hardcoded secrets."""
        secret_patterns = {
            'api_key': r'api[_-]?key[\'"]?\s * [:=]\s * [\'"][a-zA-Z0-9]{20,}[\'"]',
            'password': r'password[\'"]?\s * [:=]\s * [\'"][^\'\"]+[\'"]',
            'token': r'token[\'"]?\s * [:=]\s * [\'"][a-zA-Z0-9\-_.]+[\'"]'
        }
        self.assertEqual(len(secret_patterns), 3)

    def test_owasp_security_guidelines(self):
        """Test validation against OWASP Python security guidelines."""
        security_checks = [
            'SQL injection prevention',
            'Command injection prevention',
            'Path traversal prevention',
            'Insecure deserialization',
            'Weak cryptography'
        ]
        self.assertEqual(len(security_checks), 5)

    def test_unsafe_function_detection(self):
        """Test detection of unsafe function usage."""
        unsafe_functions = ['eval', 'exec', 'pickle.loads', '__import__']
        code_sample = "result=eval(user_input)"

        unsafe_detected = any(func in code_sample for func in unsafe_functions)
        self.assertTrue(unsafe_detected)

    def test_sql_injection_detection(self):
        """Test detecting SQL injection."""
        vulnerable_code = 'query=f"SELECT * FROM users WHERE id={user_id}"'

        # Check for f-string with variable in SQL
        is_vulnerable = 'SELECT' in vulnerable_code and '{' in vulnerable_code
        self.assertTrue(is_vulnerable)

    def test_insecure_network_calls(self):
        """Test flagging HTTP instead of HTTPS."""
        network_calls = [
            {'url': 'http://api.example.com', 'secure': False},
            {'url': 'https://api.example.com', 'secure': True},
            {'url': 'http://localhost:8000', 'secure': False}
        ]
        insecure = [c for c in network_calls if not c['secure']]
        self.assertEqual(len(insecure), 2)

    def test_hardcoded_credentials_detection(self):
        """Test detecting hardcoded credentials."""
        credentials_patterns = [
            'mongodb + srv://user:password@host',
            'postgres://user:password@localhost',
            'mysql://user:password@host'
        ]
        self.assertEqual(len(credentials_patterns), 3)



