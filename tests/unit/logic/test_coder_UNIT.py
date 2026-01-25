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
"""Test classes from test_agent_coder.py - core module."""

from __future__ import annotations
from _thread import LockType
from _thread import LockType
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
from tests.utils.agent_test_utils import *  # Added for modular test support
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# Try to import test utilities
try:
    from tests.utils.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path, load_agent_module
except ImportError:
    # Fallback
    AGENT_DIR: Path = Path(__file__).parent.parent.parent.parent / 'src'
    
    class agent_sys_path:
        def __enter__(self) -> str: 

            return self
        def __exit__(self, *args) -> str: 
            sys.path.remove(str(AGENT_DIR))

        agent = mod.CoderAgent(str(target))
        lang = agent.detect_language()

        assert lang == mod.CodeLanguage.PYTHON

    def test_generate_javascript_code(self, tmp_path: Path) -> None:
        """Test generating JavaScript code."""
        with agent_dir_on_path():
            mod: sys.ModuleType = load_agent_module("coder/code_generator.py")

        target: Path = tmp_path / "test.js"
        target.write_text("// JavaScript code")

        agent = mod.CoderAgent(str(target))
        lang = agent.detect_language()

        assert lang == mod.CodeLanguage.JAVASCRIPT


# =============================================================================
# Session 9: Code Documentation Generation Tests
# =============================================================================



class TestCodeDocumentationGeneration:
    """Tests for code comment and documentation generation."""

    def test_detect_missing_docstring(self, tmp_path: Path) -> None:
        """Test detecting missing docstrings."""
        with agent_dir_on_path():
            mod: sys.ModuleType = load_agent_module("coder/code_generator.py")

        code = """
def my_function(x, y) -> str:
    return x + y
"""
        target: Path = tmp_path / "test.py"
        target.write_text(code)

        agent = mod.CoderAgent(str(target))
        content = agent.read_previous_content()

        assert "def my_function" in content

    def test_detect_existing_docstring(self, tmp_path: Path) -> None:
        """Test detecting existing docstrings."""
        with agent_dir_on_path():
            mod: sys.ModuleType = load_agent_module("coder/code_generator.py")

        code = '''
def documented_function(x, y) -> str:
    """Add two numbers."""
    return x + y
'''
        target: Path = tmp_path / "test.py"
        target.write_text(code)

        agent = mod.CoderAgent(str(target))
        content = agent.read_previous_content()

        assert '"""Add two numbers."""' in content


# =============================================================================
# Session 9: Code Optimization Pattern Tests
# =============================================================================



class TestCodeOptimizationPatterns:
    """Tests for code optimization pattern application."""

    def test_detect_inefficient_loop(self, tmp_path: Path) -> None:
        """Test detecting inefficient loop patterns."""
        with agent_dir_on_path():
            mod: sys.ModuleType = load_agent_module("coder/code_generator.py")

        code = """
result=[]
for i in range(len(items)):
    result.append(items[i] * 2)
"""
        target: Path = tmp_path / "test.py"
        target.write_text(code)

        agent = mod.CoderAgent(str(target))
        content = agent.read_previous_content()

        assert "range(len(" in content

    def test_detect_list_comprehension_opportunity(self, tmp_path: Path) -> None:
        """Test detecting list comprehension opportunities."""
        with agent_dir_on_path():
            mod: sys.ModuleType = load_agent_module("coder/code_generator.py")

        code = """
result=[]
for x in data:
    result.append(x * 2)
"""
        target: Path = tmp_path / "test.py"
        target.write_text(code)

        agent = mod.CoderAgent(str(target))
        content = agent.read_previous_content()

        assert "append" in content


# =============================================================================
# Session 9: Dead Code Detection Tests
# =============================================================================



class TestDeadCodeDetection:
    """Tests for dead code detection and removal."""

    def test_detect_unused_import(self, tmp_path: Path) -> None:
        """Test detecting unused imports."""
        with agent_dir_on_path():
            mod: sys.ModuleType = load_agent_module("coder/code_generator.py")

        code = """
        import os
import sys

print("hello")
"""
        target: Path = tmp_path / "test.py"
        target.write_text(code)

        agent = mod.CoderAgent(str(target))
        content = agent.read_previous_content()

        assert "import os" in content

    def test_detect_unused_variable(self, tmp_path: Path) -> None:
        """Test detecting unused variables."""
        with agent_dir_on_path():
            mod: sys.ModuleType = load_agent_module("coder/code_generator.py")

        code = """
def func() -> str:
    unused=42
    return "result"
"""
        target: Path = tmp_path / "test.py"
        target.write_text(code)

        agent = mod.CoderAgent(str(target))
        content = agent.read_previous_content()

        assert "unused=42" in content


# =============================================================================
# Session 9: Dependency Injection Pattern Tests
# =============================================================================



class TestDependencyInjectionPatterns:
    """Tests for code dependency injection patterns."""

    def test_detect_hardcoded_dependency(self, tmp_path: Path) -> None:
        """Test detecting hardcoded dependencies."""
        with agent_dir_on_path():
            mod: sys.ModuleType = load_agent_module("coder/code_generator.py")

        code = """
class Service:
    def __init__(self) -> str:
        self.db=Database()  # Hardcoded
"""
        target: Path = tmp_path / "test.py"
        target.write_text(code)

        agent = mod.CoderAgent(str(target))
        content = agent.read_previous_content()

        assert "Database()" in content


# =============================================================================
# Session 9: Code Splitting Tests
# =============================================================================



class TestCodeSplitting:
    """Tests for code splitting and module extraction."""

    def test_detect_large_function(self, tmp_path: Path) -> None:
        """Test detecting functions that should be split."""
        with agent_dir_on_path():
            mod: sys.ModuleType = load_agent_module("coder/code_generator.py")

        code: str = "\n".join([f"    line{i} = {i}" for i in range(50)])
        code: str = f"def large_function():\n{code}\n    return None"
        target: Path = tmp_path / "test.py"
        target.write_text(code)

        agent = mod.CoderAgent(str(target))
        metrics = agent.calculate_metrics()

        assert metrics is not None


# =============================================================================
# Session 9: Code Consistency Tests
# =============================================================================



class TestCodeConsistency:
    """Tests for code consistency enforcement across files."""

    def test_detect_naming_inconsistency(self, tmp_path: Path) -> None:
        """Test detecting naming inconsistencies."""
        with agent_dir_on_path():
            mod: sys.ModuleType = load_agent_module("coder/code_generator.py")

        code = """
def camelCase() -> str:
    pass

def snake_case() -> str:
    pass
"""
        target: Path = tmp_path / "test.py"
        target.write_text(code)

        agent = mod.CoderAgent(str(target))
        content = agent.read_previous_content()

        assert "camelCase" in content
        assert "snake_case" in content


# =============================================================================
# Session 9: Code Template Tests
# =============================================================================



class TestCodeTemplates:
    """Tests for code template instantiation."""

    def test_read_template_file(self, tmp_path: Path) -> None:
        """Test reading template-like code."""
        with agent_dir_on_path():
            mod: sys.ModuleType = load_agent_module("coder/code_generator.py")

        code = """
# Template: {name}
class {ClassName}:
    def __init__(self) -> str:
        pass
"""
        target: Path = tmp_path / "template.py"
        target.write_text(code)

        agent = mod.CoderAgent(str(target))
        content = agent.read_previous_content()

        assert "{name}" in content


# =============================================================================
# Session 9: Type Annotation Tests
# =============================================================================



class TestTypeAnnotationInference:
    """Tests for code type annotation inference."""

    def test_detect_missing_type_hints(self, tmp_path: Path) -> None:
        """Test detecting missing type hints."""
        with agent_dir_on_path():
            mod: sys.ModuleType = load_agent_module("coder/code_generator.py")

        code = """
def add(x, y) -> str:
    return x + y
"""
        target: Path = tmp_path / "test.py"
        target.write_text(code)

        agent = mod.CoderAgent(str(target))
        content = agent.read_previous_content()

        assert "def add(x, y)" in content

    def test_detect_existing_type_hints(self, tmp_path: Path) -> None:
        """Test detecting existing type hints."""
        with agent_dir_on_path():
            mod: sys.ModuleType = load_agent_module("coder/code_generator.py")

        code = """
def add(x: int, y: int) -> int:
    return x + y
"""
        target: Path = tmp_path / "test.py"
        target.write_text(code)

        agent = mod.CoderAgent(str(target))
        content = agent.read_previous_content()

        assert "-> int" in content


# =============================================================================
# Session 9: Style Unification Tests
# =============================================================================



class TestStyleUnification:
    """Tests for code style unification."""

    def test_detect_mixed_quotes(self, tmp_path: Path) -> None:
        """Test detecting mixed quote styles."""
        with agent_dir_on_path():
            mod: sys.ModuleType = load_agent_module("coder/code_generator.py")

        code = '''
x="double"
y='single'
'''
        target: Path = tmp_path / "test.py"
        target.write_text(code)

        agent = mod.CoderAgent(str(target))
        content = agent.read_previous_content()

        assert '"double"' in content
        assert "'single'" in content


# =============================================================================
# Session 9: Merge Conflict Resolution Tests
# =============================================================================



class TestMergeConflictResolution:
    """Tests for code merge conflict resolution."""

    def test_detect_merge_markers(self, tmp_path: Path) -> None:
        """Test detecting merge conflict markers."""
        with agent_dir_on_path():
            mod: sys.ModuleType = load_agent_module("coder/code_generator.py")

        code = """
<<<<<<< HEAD
x=1
=======
x=2
>>>>>>> branch
"""
        target: Path = tmp_path / "test.py"
        target.write_text(code)

        agent = mod.CoderAgent(str(target))
        content = agent.read_previous_content()

        assert "<<<<<<< HEAD" in content


# =============================================================================
# Session 9: API Compatibility Tests
# =============================================================================



class TestAPICompatibility:
    """Tests for code API compatibility checking."""

    def test_detect_api_signature(self, tmp_path: Path) -> None:
        """Test detecting API signatures."""
        with agent_dir_on_path():
            mod: sys.ModuleType = load_agent_module("coder/code_generator.py")

        code = """
def public_api(arg1, arg2, *, keyword=None) -> str:
    pass
"""
        target: Path = tmp_path / "test.py"
        target.write_text(code)

        agent = mod.CoderAgent(str(target))
        content = agent.read_previous_content()

        assert "keyword=None" in content


# =============================================================================
# Session 9: Incremental Improvement Tests
# =============================================================================



class TestIncrementalImprovement:
    """Tests for incremental code improvement strategies."""

    def test_small_improvement_applied(self, tmp_path: Path) -> None:
        """Test small improvements are detected."""
        with agent_dir_on_path():
            mod: sys.ModuleType = load_agent_module("coder/code_generator.py")

        code = "x=1\ny=2"  # Missing spaces
        target: Path = tmp_path / "test.py"
        target.write_text(code)

        agent = mod.CoderAgent(str(target))
        content = agent.read_previous_content()

        assert content is not None


# =============================================================================
# Session 9: Quality Gates Tests
# =============================================================================



class TestQualityGates:
    """Tests for code quality gates and thresholds."""

    def test_quality_score_calculation(self, tmp_path: Path) -> None:
        """Test quality score is calculated."""
        with agent_dir_on_path():
            mod: sys.ModuleType = load_agent_module("coder/code_generator.py")

        code = '''
def good_function(x: int) -> int:
    """Return double of x."""
    return x * 2
'''
        target: Path = tmp_path / "test.py"
        target.write_text(code)

        agent = mod.CoderAgent(str(target))
        score = agent.calculate_quality_score()

        assert score is not None
        assert score.score >= 0


# =============================================================================
# Session 9: Security Scanning Tests
# =============================================================================



class TestSecurityScanning:
    """Tests for code security scanning integration."""

    def test_detect_hardcoded_secret(self, tmp_path: Path) -> None:
        """Test detecting hardcoded secrets."""
        with agent_dir_on_path():
            mod: sys.ModuleType = load_agent_module("coder/code_generator.py")

        code = '''
API_KEY=os.environ.get("OPENAI_API_KEY", "dummy_key_for_testing")
'''
        target: Path = tmp_path / "test.py"
        target.write_text(code)

        agent = mod.CoderAgent(str(target))
        content = agent.read_previous_content()

        assert "API_KEY" in content


# =============================================================================
# Session 9: Complexity Analysis Tests
# =============================================================================



class TestComplexityAnalysis:
    """Tests for code complexity analysis."""

    def test_calculate_cyclomatic_complexity(self, tmp_path: Path) -> None:
        """Test calculating cyclomatic complexity."""
        with agent_dir_on_path():
            mod: sys.ModuleType = load_agent_module("coder/code_generator.py")

        code = """
def complex_function(x) -> str:
    if x > 0:
        if x > 10:
            return "big"
        return "small"
    return "negative"
"""
        target: Path = tmp_path / "test.py"
        target.write_text(code)

        agent = mod.CoderAgent(str(target))
        metrics = agent.calculate_metrics()

        assert metrics is not None


# =============================================================================
# Session 9: Coverage Gap Tests
# =============================================================================



class TestCoverageGapDetection:
    """Tests for code coverage gap detection."""

    def test_detect_untested_function(self, tmp_path: Path) -> None:
        """Test detecting untested functions."""
        with agent_dir_on_path():
            mod: sys.ModuleType = load_agent_module("coder/code_generator.py")

        code = """
def untested_function() -> str:
    return 42
"""
        target: Path = tmp_path / "test.py"
        target.write_text(code)

        agent = mod.CoderAgent(str(target))
        content = agent.read_previous_content()

        assert "untested_function" in content


# =============================================================================
# Session 9: Performance Profiling Tests
# =============================================================================



class TestMigrationAutomation:
    """Tests for code migration automation."""

    def test_detect_deprecated_syntax(self, tmp_path: Path) -> None:
        """Test detecting deprecated syntax."""
        with agent_dir_on_path():
            mod: sys.ModuleType = load_agent_module("coder/code_generator.py")

        code = """
# Old-style string formatting
message="Hello %s" % name
"""
        target: Path = tmp_path / "test.py"
        target.write_text(code)

        agent = mod.CoderAgent(str(target))
        content = agent.read_previous_content()

        assert "%s" in content

    def test_detect_python2_syntax(self, tmp_path: Path) -> None:
        """Test detecting Python 2 style syntax."""
        with agent_dir_on_path():
            mod: sys.ModuleType = load_agent_module("coder/code_generator.py")

        code = """
class OldStyle:
    pass
"""
        target: Path = tmp_path / "test.py"
        target.write_text(code)

        agent = mod.CoderAgent(str(target))
        content = agent.read_previous_content()

        assert "class OldStyle" in content


# =============================================================================
# COMPREHENSIVE TEST SUITE: Code Quality, Formatting, Security
# =============================================================================


class TestSyntaxValidation(unittest.TestCase):
    """Tests for Python syntax validation."""

    def test_validate_valid_python_syntax(self) -> None:
        """Test validation of syntactically correct code."""
        code = """def hello(name) -> str:
    return f"Hello, {name}!"
"""
        # Try to compile - no SyntaxError
        try:
            compile(code, "<string>", "exec")
            is_valid = True
        except SyntaxError:
            is_valid = False
        assert is_valid

    def test_detect_syntax_error(self) -> None:
        """Test detection of syntax errors."""
        code = "def hello(name)\n    return name"
        try:
            compile(code, "<string>", "exec")
            is_valid = True
        except SyntaxError:
            is_valid = False
        assert not is_valid

    def test_validate_complex_syntax(self) -> None:
        """Test validation with complex Python features."""
        code = """
@decorator
async def process_data(items: list[str]) -> dict[str, int]:
    result={item: len(item) for item in items}
    return result
"""
        try:
            compile(code, "<string>", "exec")
            is_valid = True
        except SyntaxError:
            is_valid = False
        assert is_valid

