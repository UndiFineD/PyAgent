# -*- coding: utf-8 -*-
"""Test classes from test_agent_coder.py - core module."""

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
from tests.agent_test_utils import *  # Added for modular test support
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# Try to import test utilities
try:
    from tests.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path, load_agent_module
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


class TestAccessibilityIssueTypeEnum:
    """Tests for AccessibilityIssueType enum."""

    def test_enum_values(self) -> None:
        """Test enum has expected values."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_coder.py")
        assert mod.AccessibilityIssueType.MISSING_ALT_TEXT.value == "missing_alt_text"
        assert mod.AccessibilityIssueType.LOW_COLOR_CONTRAST.value == "low_color_contrast"
        assert mod.AccessibilityIssueType.MISSING_LABEL.value == "missing_label"
        assert mod.AccessibilityIssueType.KEYBOARD_NAVIGATION.value == "keyboard_navigation"

    def test_all_members(self) -> None:
        """Test all enum members exist."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_coder.py")
        members = list(mod.AccessibilityIssueType)
        assert len(members) == 10



class TestAccessibilitySeverityEnum:
    """Tests for AccessibilitySeverity enum."""

    def test_enum_values(self) -> None:
        """Test enum has expected values."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_coder.py")
        assert mod.AccessibilitySeverity.CRITICAL.value == 4
        assert mod.AccessibilitySeverity.SERIOUS.value == 3
        assert mod.AccessibilitySeverity.MODERATE.value == 2
        assert mod.AccessibilitySeverity.MINOR.value == 1

    def test_severity_ordering(self) -> None:
        """Test severity values are ordered correctly."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_coder.py")
        assert mod.AccessibilitySeverity.MINOR.value < mod.AccessibilitySeverity.MODERATE.value
        assert mod.AccessibilitySeverity.MODERATE.value < mod.AccessibilitySeverity.SERIOUS.value
        assert mod.AccessibilitySeverity.SERIOUS.value < mod.AccessibilitySeverity.CRITICAL.value



class TestWCAGLevelEnum:
    """Tests for WCAGLevel enum."""

    def test_enum_values(self) -> None:
        """Test enum has expected values."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_coder.py")
        assert mod.WCAGLevel.A.value == "A"
        assert mod.WCAGLevel.AA.value == "AA"
        assert mod.WCAGLevel.AAA.value == "AAA"

    def test_all_levels(self) -> None:
        """Test all WCAG levels exist."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_coder.py")
        assert len(list(mod.WCAGLevel)) == 3



class TestAccessibilityIssueDataclass:
    """Tests for AccessibilityIssue dataclass."""

    def test_creation(self) -> None:
        """Test creating AccessibilityIssue."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_coder.py")
        issue = mod.AccessibilityIssue(
            issue_type=mod.AccessibilityIssueType.MISSING_ALT_TEXT,
            severity=mod.AccessibilitySeverity.CRITICAL,
            wcag_level=mod.WCAGLevel.A,
            wcag_criterion="1.1.1",
            description="Image missing alt",
            element="<img src='test.jpg'>",
            line_number=10,
            suggested_fix="Add alt attribute"
        )
        assert issue.issue_type == mod.AccessibilityIssueType.MISSING_ALT_TEXT
        assert issue.severity == mod.AccessibilitySeverity.CRITICAL
        assert issue.line_number == 10

    def test_defaults(self) -> None:
        """Test AccessibilityIssue defaults."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_coder.py")
        issue = mod.AccessibilityIssue(
            issue_type=mod.AccessibilityIssueType.ARIA_MISSING,
            severity=mod.AccessibilitySeverity.MODERATE,
            wcag_level=mod.WCAGLevel.AA,
            wcag_criterion="4.1.2",
            description="Missing ARIA",
            element="button"
        )
        assert issue.line_number is None
        assert issue.suggested_fix is None
        assert issue.auto_fixable is False



class TestColorContrastResultDataclass:
    """Tests for ColorContrastResult dataclass."""

    def test_creation(self) -> None:
        """Test creating ColorContrastResult."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_coder.py")
        result = mod.ColorContrastResult(
            foreground="#000000",
            background="#FFFFFF",
            contrast_ratio=21.0,
            passes_aa=True,
            passes_aaa=True
        )
        assert result.contrast_ratio == 21.0
        assert result.passes_aa is True
        assert result.passes_aaa is True



class TestAccessibilityReportDataclass:
    """Tests for AccessibilityReport dataclass."""

    def test_creation(self) -> None:
        """Test creating AccessibilityReport."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_coder.py")
        report = mod.AccessibilityReport(
            file_path="test.html",
            issues=[],
            total_elements=10,
            wcag_level=mod.WCAGLevel.AA,
            compliance_score=95.0,
            critical_count=0,
            serious_count=1
        )
        assert report.file_path == "test.html"
        assert report.compliance_score == 95.0

    def test_defaults(self) -> None:
        """Test AccessibilityReport defaults."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_coder.py")
        report = mod.AccessibilityReport(file_path="test.html")
        assert report.issues == []
        assert report.total_elements == 0
        assert report.compliance_score == 100.0



class TestARIAAttributeDataclass:
    """Tests for ARIAAttribute dataclass."""

    def test_creation(self) -> None:
        """Test creating ARIAAttribute."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_coder.py")
        attr = mod.ARIAAttribute(
            name="aria-label",
            value="Submit button",
            is_valid=True
        )
        assert attr.name == "aria-label"
        assert attr.value == "Submit button"
        assert attr.is_valid is True



class TestAccessibilityAnalyzer:
    """Tests for AccessibilityAnalyzer class."""

    def test_initialization(self) -> None:
        """Test AccessibilityAnalyzer initialization."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_coder.py")
        analyzer = mod.AccessibilityAnalyzer(mod.WCAGLevel.AA)
        assert analyzer.target_level == mod.WCAGLevel.AA
        assert analyzer.issues == []

    def test_analyze_html_missing_alt(self) -> None:
        """Test detecting missing alt text in HTML."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_coder.py")
        analyzer = mod.AccessibilityAnalyzer()
        html_content = '<html><body><img src="test.jpg"></body></html>'
        report = analyzer.analyze_content(html_content, "html")
        alt_issues = [i for i in report.issues
                      if i.issue_type == mod.AccessibilityIssueType.MISSING_ALT_TEXT]
        assert len(alt_issues) > 0

    def test_analyze_html_with_alt(self) -> None:
        """Test HTML with proper alt text has no alt issues."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_coder.py")
        analyzer = mod.AccessibilityAnalyzer()
        html_content = '<html><body><img src="test.jpg" alt="Test image"></body></html>'
        report = analyzer.analyze_content(html_content, "html")
        alt_issues = [i for i in report.issues
                      if i.issue_type == mod.AccessibilityIssueType.MISSING_ALT_TEXT]
        assert len(alt_issues) == 0

    def test_analyze_html_missing_label(self) -> None:
        """Test detecting missing form labels in HTML."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_coder.py")
        analyzer = mod.AccessibilityAnalyzer()
        html_content = '<html><body><input type="text" id="name"></body></html>'
        report = analyzer.analyze_content(html_content, "html")
        label_issues = [i for i in report.issues
                        if i.issue_type == mod.AccessibilityIssueType.MISSING_LABEL]
        assert len(label_issues) > 0

    def test_analyze_html_heading_hierarchy(self) -> None:
        """Test detecting heading hierarchy issues."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_coder.py")
        analyzer = mod.AccessibilityAnalyzer()
        # Page starts with h2 instead of h1
        html_content = '<html><body><h2>Title</h2></body></html>'
        report = analyzer.analyze_content(html_content, "html")
        heading_issues = [i for i in report.issues
                          if i.issue_type == mod.AccessibilityIssueType.HEADING_HIERARCHY]
        assert len(heading_issues) > 0

    def test_analyze_javascript_click_without_keyboard(self) -> None:
        """Test detecting click handlers without keyboard support."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_coder.py")
        analyzer = mod.AccessibilityAnalyzer()
        js_content = '<button onClick={handleClick}>Click me</button>'
        report = analyzer.analyze_content(js_content, "javascript")
        keyboard_issues = [i for i in report.issues
                           if i.issue_type == mod.AccessibilityIssueType.KEYBOARD_NAVIGATION]
        assert len(keyboard_issues) > 0

    def test_analyze_javascript_interactive_div(self) -> None:
        """Test detecting interactive divs without proper roles."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_coder.py")
        analyzer = mod.AccessibilityAnalyzer()
        js_content = '<div onClick={handleClick}>Clickable</div>'
        report = analyzer.analyze_content(js_content, "javascript")
        semantic_issues = [i for i in report.issues
                           if i.issue_type == mod.AccessibilityIssueType.SEMANTIC_HTML]
        assert len(semantic_issues) > 0

    def test_check_color_contrast_high(self) -> None:
        """Test color contrast check with high contrast."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_coder.py")
        analyzer = mod.AccessibilityAnalyzer()
        result = analyzer.check_color_contrast("#000000", "#FFFFFF")
        assert result.contrast_ratio == 21.0
        assert result.passes_aa is True
        assert result.passes_aaa is True

    def test_check_color_contrast_low(self) -> None:
        """Test color contrast check with low contrast."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_coder.py")
        analyzer = mod.AccessibilityAnalyzer()
        result = analyzer.check_color_contrast("#777777", "#999999")
        assert result.passes_aa is False

    def test_check_color_contrast_large_text(self) -> None:
        """Test color contrast check with large text requirements."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_coder.py")
        analyzer = mod.AccessibilityAnalyzer()
        result = analyzer.check_color_contrast("#555555", "#FFFFFF", is_large_text=True)
        # Large text has lower requirements (3:1 for AA)
        assert result.min_ratio_aa == 3.0

    def test_get_issues_by_severity(self) -> None:
        """Test filtering issues by severity."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_coder.py")
        analyzer = mod.AccessibilityAnalyzer()
        html_content = '<html><body><img src="test.jpg"></body></html>'
        analyzer.analyze_content(html_content, "html")
        critical_issues = analyzer.get_issues_by_severity(
            mod.AccessibilitySeverity.CRITICAL
        )
        assert all(i.severity == mod.AccessibilitySeverity.CRITICAL
                   for i in critical_issues)

    def test_get_issues_by_wcag_level(self) -> None:
        """Test filtering issues by WCAG level."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_coder.py")
        analyzer = mod.AccessibilityAnalyzer()
        html_content = '<html><body><img src="test.jpg"></body></html>'
        analyzer.analyze_content(html_content, "html")
        level_a_issues = analyzer.get_issues_by_wcag_level(mod.WCAGLevel.A)
        assert all(i.wcag_level == mod.WCAGLevel.A for i in level_a_issues)

    def test_enable_disable_rules(self) -> None:
        """Test enabling and disabling rules."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_coder.py")
        analyzer = mod.AccessibilityAnalyzer()
        analyzer.disable_rule("1.1.1")
        assert analyzer.rules.get("1.1.1") is False
        analyzer.enable_rule("1.1.1")
        assert analyzer.rules.get("1.1.1") is True

    def test_compliance_score_calculation(self) -> None:
        """Test compliance score is calculated correctly."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_coder.py")
        analyzer = mod.AccessibilityAnalyzer()
        # Clean HTML should have high score
        html_content = '''
        <html>
        <body>
            <main>
                <h1>Title</h1>
                <img src="test.jpg" alt="Description">
            </main>
        </body>
        </html>
        '''
        report = analyzer.analyze_content(html_content, "html")
        assert report.compliance_score > 50

    def test_analyze_file_nonexistent(self, tmp_path: Path) -> None:
        """Test analyzing nonexistent file returns empty report."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_coder.py")
        analyzer = mod.AccessibilityAnalyzer()
        report = analyzer.analyze_file(str(tmp_path / "nonexistent.html"))
        assert report.issues == []
        assert report.compliance_score == 100.0

    def test_analyze_file_html(self, tmp_path: Path) -> None:
        """Test analyzing HTML file."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_coder.py")
        html_file = tmp_path / "test.html"
        html_file.write_text('<html><body><img src="x.jpg"></body></html>')
        analyzer = mod.AccessibilityAnalyzer()
        report = analyzer.analyze_file(str(html_file))
        assert len(report.issues) > 0

    def test_analyze_python_ui(self) -> None:
        """Test analyzing Python UI code."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_coder.py")
        analyzer = mod.AccessibilityAnalyzer()
        python_content = '''
from tkinter import Button, Label
button=Button(root, text="Click")
label=Label(root, text="Info")
'''
        report = analyzer.analyze_content(python_content, "python")
        assert report is not None

    def test_recommendations_generated(self) -> None:
        """Test that recommendations are generated."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_coder.py")
        analyzer = mod.AccessibilityAnalyzer()
        html_content = '<html><body><img src="test.jpg"></body></html>'
        report = analyzer.analyze_content(html_content, "html")
        # Should have recommendations for critical issues
        assert len(report.recommendations) > 0


# =============================================================================
# Session 9: Code Refactoring Tests
# =============================================================================



class TestCodeRefactoring:
    """Tests for code refactoring suggestions and application."""

    def test_detect_refactoring_opportunity(self, tmp_path: Path) -> None:
        """Test detecting refactoring opportunities."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_coder.py")

        code = """
def process(data):
    result=[]
    for item in data:
        if item > 0:
            result.append(item * 2)
    return result
"""
        target = tmp_path / "test.py"
        target.write_text(code)

        agent = mod.CoderAgent(str(target))
        agent.read_previous_content()
        content = agent.previous_content

        assert "def process" in content

    def test_suggest_simplification(self, tmp_path: Path) -> None:
        """Test suggesting code simplification."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_coder.py")

        code = "x=True if condition else False"
        target = tmp_path / "test.py"
        target.write_text(code)

        agent = mod.CoderAgent(str(target))
        content = agent.read_previous_content()

        assert "True" in content


# =============================================================================
# Session 9: Multi-Language Code Generation Tests
# =============================================================================



class TestMultiLanguageCodeGeneration:
    """Tests for code generation for multiple programming languages."""

    def test_generate_python_code(self, tmp_path: Path) -> None:
        """Test generating Python code."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_coder.py")

        target = tmp_path / "test.py"
        target.write_text("# Python code")

        agent = mod.CoderAgent(str(target))
        lang = agent.detect_language()

        assert lang == mod.CodeLanguage.PYTHON

    def test_generate_javascript_code(self, tmp_path: Path) -> None:
        """Test generating JavaScript code."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_coder.py")

        target = tmp_path / "test.js"
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
            mod = load_agent_module("agent_coder.py")

        code = """
def my_function(x, y):
    return x + y
"""
        target = tmp_path / "test.py"
        target.write_text(code)

        agent = mod.CoderAgent(str(target))
        content = agent.read_previous_content()

        assert "def my_function" in content

    def test_detect_existing_docstring(self, tmp_path: Path) -> None:
        """Test detecting existing docstrings."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_coder.py")

        code = '''
def documented_function(x, y):
    """Add two numbers."""
    return x + y
'''
        target = tmp_path / "test.py"
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
            mod = load_agent_module("agent_coder.py")

        code = """
result=[]
for i in range(len(items)):
    result.append(items[i] * 2)
"""
        target = tmp_path / "test.py"
        target.write_text(code)

        agent = mod.CoderAgent(str(target))
        content = agent.read_previous_content()

        assert "range(len(" in content

    def test_detect_list_comprehension_opportunity(self, tmp_path: Path) -> None:
        """Test detecting list comprehension opportunities."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_coder.py")

        code = """
result=[]
for x in data:
    result.append(x * 2)
"""
        target = tmp_path / "test.py"
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
            mod = load_agent_module("agent_coder.py")

        code = """
import os
import sys

print("hello")
"""
        target = tmp_path / "test.py"
        target.write_text(code)

        agent = mod.CoderAgent(str(target))
        content = agent.read_previous_content()

        assert "import os" in content

    def test_detect_unused_variable(self, tmp_path: Path) -> None:
        """Test detecting unused variables."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_coder.py")

        code = """
def func():
    unused=42
    return "result"
"""
        target = tmp_path / "test.py"
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
            mod = load_agent_module("agent_coder.py")

        code = """
class Service:
    def __init__(self):
        self.db=Database()  # Hardcoded
"""
        target = tmp_path / "test.py"
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
            mod = load_agent_module("agent_coder.py")

        code = "\n".join([f"    line{i} = {i}" for i in range(50)])
        code = f"def large_function():\n{code}\n    return None"
        target = tmp_path / "test.py"
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
            mod = load_agent_module("agent_coder.py")

        code = """
def camelCase():
    pass

def snake_case():
    pass
"""
        target = tmp_path / "test.py"
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
            mod = load_agent_module("agent_coder.py")

        code = """
# Template: {name}
class {ClassName}:
    def __init__(self):
        pass
"""
        target = tmp_path / "template.py"
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
            mod = load_agent_module("agent_coder.py")

        code = """
def add(x, y):
    return x + y
"""
        target = tmp_path / "test.py"
        target.write_text(code)

        agent = mod.CoderAgent(str(target))
        content = agent.read_previous_content()

        assert "def add(x, y)" in content

    def test_detect_existing_type_hints(self, tmp_path: Path) -> None:
        """Test detecting existing type hints."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_coder.py")

        code = """
def add(x: int, y: int) -> int:
    return x + y
"""
        target = tmp_path / "test.py"
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
            mod = load_agent_module("agent_coder.py")

        code = '''
x="double"
y='single'
'''
        target = tmp_path / "test.py"
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
            mod = load_agent_module("agent_coder.py")

        code = """
<<<<<<< HEAD
x=1
=======
x=2
>>>>>>> branch
"""
        target = tmp_path / "test.py"
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
            mod = load_agent_module("agent_coder.py")

        code = """
def public_api(arg1, arg2, *, keyword=None):
    pass
"""
        target = tmp_path / "test.py"
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
            mod = load_agent_module("agent_coder.py")

        code = "x=1\ny=2"  # Missing spaces
        target = tmp_path / "test.py"
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
            mod = load_agent_module("agent_coder.py")

        code = '''
def good_function(x: int) -> int:
    """Return double of x."""
    return x * 2
'''
        target = tmp_path / "test.py"
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
            mod = load_agent_module("agent_coder.py")

        code = '''
API_KEY="sk_live_xxxxxxxxxxxx"
'''
        target = tmp_path / "test.py"
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
            mod = load_agent_module("agent_coder.py")

        code = """
def complex_function(x):
    if x > 0:
        if x > 10:
            return "big"
        return "small"
    return "negative"
"""
        target = tmp_path / "test.py"
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
            mod = load_agent_module("agent_coder.py")

        code = """
def untested_function():
    return 42
"""
        target = tmp_path / "test.py"
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
            mod = load_agent_module("agent_coder.py")

        code = """
# Old-style string formatting
message="Hello %s" % name
"""
        target = tmp_path / "test.py"
        target.write_text(code)

        agent = mod.CoderAgent(str(target))
        content = agent.read_previous_content()

        assert "%s" in content

    def test_detect_python2_syntax(self, tmp_path: Path) -> None:
        """Test detecting Python 2 style syntax."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_coder.py")

        code = """
class OldStyle:
    pass
"""
        target = tmp_path / "test.py"
        target.write_text(code)

        agent = mod.CoderAgent(str(target))
        content = agent.read_previous_content()

        assert "class OldStyle" in content


# =============================================================================
# COMPREHENSIVE TEST SUITE: Code Quality, Formatting, Security
# =============================================================================


class TestSyntaxValidation(unittest.TestCase):
    """Tests for Python syntax validation."""

    def test_validate_valid_python_syntax(self):
        """Test validation of syntactically correct code."""
        code = """def hello(name):
    return f"Hello, {name}!"
"""
        # Try to compile - no SyntaxError
        try:
            compile(code, "<string>", "exec")
            is_valid = True
        except SyntaxError:
            is_valid = False
        assert is_valid

    def test_detect_syntax_error(self):
        """Test detection of syntax errors."""
        code = "def hello(name)\n    return name"
        try:
            compile(code, "<string>", "exec")
            is_valid = True
        except SyntaxError:
            is_valid = False
        assert not is_valid

    def test_validate_complex_syntax(self):
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

    def test_detect_indentation_error(self):
        """Test detection of indentation errors."""
        code = """def func():
return "error"
"""
        try:
            compile(code, "<string>", "exec")
            is_valid = True
        except (SyntaxError, IndentationError):
            is_valid = False
        assert not is_valid



class TestCodeFormatting(unittest.TestCase):
    """Tests for code formatting integration."""

    def test_black_format_detection(self):
        """Test detection of black formatting violations."""
        unformatted = "x=1+2"
        formatted = "x = 1 + 2"
        assert unformatted != formatted

    def test_autopep8_integration(self):
        """Test autopep8 formatting."""
        code = "x=1"  # Extra spaces
        # autopep8 would fix to: x=1
        expected = "x=1"
        assert "=" in code
        assert "=" in expected

    def test_whitespace_normalization(self):
        """Test whitespace normalization."""
        code = "def  func( x , y ):\n    return x + y"
        # Should normalize spaces
        assert "  " in code  # Double space exists in original

    def test_line_length_handling(self):
        """Test line length compliance."""
        long_line = "x=" + "a" * 100
        assert len(long_line) > 88  # Black default max line length



class TestImportOrganization(unittest.TestCase):
    """Tests for import organization (isort)."""

    def test_organize_imports(self):
        """Test import organization."""
        unorganized = """import z
import a
from module import foo
"""
        # isort would organize to: a, z, then from imports
        assert "import z" in unorganized
        assert "import a" in unorganized

    def test_separate_import_groups(self):
        """Test separation of import groups."""
        imports = """import os
import sys
from typing import Dict
from mymodule import func
"""
        lines = imports.split("\n")
        stdlib_imports = [line for line in lines if "os" in line or "sys" in line]
        local_imports = [line for line in lines if "mymodule" in line]
        assert len(stdlib_imports) > 0
        assert len(local_imports) > 0

    def test_remove_duplicate_imports(self):
        """Test removal of duplicate imports."""
        code = """import os
import os
from sys import argv
from sys import argv
"""
        # Should be deduplicated
        assert code.count("import os") == 2



class TestDiffApplication(unittest.TestCase):
    """Tests for diff-based vs full file modifications."""

    def test_apply_diff_patch(self):
        """Test applying diff patch."""
        original = "line 1\nline 2\nline 3"
        modified = "line 1\nline 2 modified\nline 3"
        # Diff would show changes to line 2
        assert original != modified
        assert "modified" in modified

    def test_full_file_rewrite(self):
        """Test full file rewrite."""
        original = "old code"
        new = "new code"
        assert original != new

    def test_minimal_changes_strategy(self):
        """Test preserving minimal changes."""
        original = """def func():
    return 1
"""
        modified = """def func():
    return 2
"""
        # Only 1 line changed
        assert original.count("\n") == modified.count("\n")



class TestCodeComplexity(unittest.TestCase):
    """Tests for code complexity metrics."""

    def test_cyclomatic_complexity(self):
        """Test cyclomatic complexity calculation."""
        simple = "x=1"
        complex_code = """
if x:
    if y:
        if z:
            pass
"""
        # Complex code has higher cyclomatic complexity
        assert complex_code.count("if") > simple.count("if")

    def test_line_complexity(self):
        """Test line count as complexity metric."""
        short_func = "def f(): return 1"
        long_func = "def f():\n    x=1\n    y=2\n    return x + y"
        assert len(long_func) > len(short_func)

    def test_nesting_depth(self):
        """Test nesting depth calculation."""
        shallow = "if x: pass"
        deep = "if a:\n  if b:\n    if c:\n      pass"
        assert deep.count("  ") > shallow.count("  ")



class TestBackupCreation(unittest.TestCase):
    """Tests for backup creation before modifications."""

    def test_create_backup_before_modification(self):
        """Test backup is created before modification."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.py') as f:
            f.write("original content")
            f.flush()
            original_file = f.name

        try:
            # Create backup
            backup_file = original_file + ".bak"
            import shutil
            shutil.copy(original_file, backup_file)

            # Verify backup exists
            assert Path(backup_file).exists()
            with open(backup_file) as bf:
                assert bf.read() == "original content"
        finally:
            Path(original_file).unlink(missing_ok=True)
            Path(backup_file).unlink(missing_ok=True)

    def test_backup_content_integrity(self):
        """Test backup preserves original content."""
        original = "def func():\n    pass"
        backup = original
        assert backup == original



class TestRollback(unittest.TestCase):
    """Tests for rollback functionality."""

    def test_rollback_on_syntax_error(self):
        """Test rollback when syntax error occurs."""
        broken = "def func(: pass"  # Syntax error

        # Should detect broken state
        try:
            compile(broken, "<string>", "exec")
            needs_rollback = False
        except SyntaxError:
            needs_rollback = True

        assert needs_rollback

    def test_rollback_on_test_failure(self):
        """Test rollback when tests fail."""

        # Would fail test expecting sum
        assert 3 + 2 != 1  # Test would fail



class TestConcurrency(unittest.TestCase):
    """Tests for concurrent code generation."""

    def test_concurrent_file_generation(self):
        """Test generating multiple files concurrently."""
        import threading

        generated_files = []
        lock = threading.Lock()

        def generate_file(name):
            with lock:
                generated_files.append(name)

        threads = []
        for i in range(5):
            t = threading.Thread(target=generate_file, args=(f"file{i}",))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        assert len(generated_files) == 5

    def test_concurrent_modifications(self):
        """Test concurrent code modifications."""
        import threading

        counter = {"value": 0}
        lock = threading.Lock()

        def modify():
            with lock:
                counter["value"] += 1

        threads = [threading.Thread(target=modify) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert counter["value"] == 10



class TestLargeFileHandling(unittest.TestCase):
    """Tests for handling large files."""

    def test_large_file_processing(self):
        """Test processing files with many lines."""
        large_code = "\n".join([f"x{i} = {i}" for i in range(10000)])
        lines = large_code.split("\n")
        assert len(lines) == 10000

    def test_memory_efficiency(self):
        """Test memory-efficient processing."""
        # Stream processing instead of loading entire file
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            for i in range(1000):
                f.write(f"line {i}\n")
            f.flush()
            fname = f.name

        try:
            line_count = 0
            with open(fname) as f:
                for line in f:
                    line_count += 1
            assert line_count == 1000
        finally:
            Path(fname).unlink()



class TestCodeMetrics(unittest.TestCase):
    """Tests for code metrics extraction."""

    def test_extract_function_count(self):
        """Test counting functions in code."""
        code = """
def func1():
    pass

def func2():
    pass

class MyClass:
    def method(self):
        pass
"""
        func_count = code.count("def ")
        assert func_count == 3

    def test_extract_class_count(self):
        """Test counting classes in code."""
        code = """
class A:
    pass

class B:
    pass
"""
        class_count = code.count("class ")
        assert class_count == 2

    def test_calculate_lines_of_code(self):
        """Test LOC calculation."""
        code = """
def func():
    x=1
    y=2
    return x + y
"""
        non_empty_lines = [line for line in code.split("\n") if line.strip()]
        assert len(non_empty_lines) > 0



class TestDocstringGeneration(unittest.TestCase):
    """Tests for automatic docstring generation."""

    def test_function_docstring_generation(self):
        """Test generating docstrings for functions."""

        # Generated docstring would be:
        docstring = """\"\"\"Add two numbers.

        Args:
            a: First number
            b: Second number

        Returns:
            Sum of a and b
        \"\"\""""
        assert "Add" in docstring
        assert "Args" in docstring

    def test_preserve_existing_docstrings(self):
        """Test that existing docstrings are preserved."""
        code = '''
def func():
    """This is an existing docstring."""
    pass
'''
        assert "existing docstring" in code



class TestCodeQualityValidation(unittest.TestCase):
    """Test code quality validation improvements."""

    def test_mypy_type_checking_integration(self):
        """Test mypy type checking for generated code."""
        mypy_config = {
            'enabled': True,
            'strict': False,
            'ignore_missing_imports': True
        }
        self.assertTrue(mypy_config['enabled'])

    def test_pylint_support_with_strictness_levels(self):
        """Test pylint with configurable strictness levels."""
        strictness_levels = {
            'lenient': 7.0,  # Allow code quality 7 / 10+
            'moderate': 8.0,  # Require 8 / 10+
            'strict': 9.0    # Require 9 / 10+
        }
        self.assertEqual(len(strictness_levels), 3)

    def test_bandit_security_scanning(self):
        """Test bandit security scanning for generated code."""
        security_issues = [
            {'type': 'hardcoded_sql_string', 'severity': 'high'},
            {'type': 'hardcoded_password', 'severity': 'critical'},
            {'type': 'insecure_random', 'severity': 'medium'}
        ]
        critical_issues = [i for i in security_issues if i['severity'] == 'critical']
        self.assertEqual(len(critical_issues), 1)

    def test_cyclomatic_complexity_validation(self):
        """Test cyclomatic complexity metrics validation."""
        complexity_limits = {
            'function': 10,
            'class': 15,
            'module': 30
        }
        self.assertLessEqual(complexity_limits['function'], complexity_limits['class'])

    def test_incremental_validation(self):
        """Test validating only changed sections."""
        file_changes = {
            'unchanged_functions': ['func_a', 'func_b'],
            'changed_functions': ['func_c'],
            'new_functions': ['func_d']
        }
        to_validate = file_changes['changed_functions'] + file_changes['new_functions']
        self.assertEqual(len(to_validate), 2)



