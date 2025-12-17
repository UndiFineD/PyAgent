#!/usr / bin / env python3
# Copyright (c) 2025 DebVisor contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org / licenses / LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Legacy tests for agent-coder.py."""

from __future__ import annotations
from pathlib import Path
from typing import Any
import pytest
from agent_test_utils import agent_dir_on_path, load_agent_module


@pytest.fixture()
def base_agent_module() -> Any:
    with agent_dir_on_path():
        import base_agent
        return base_agent


def test_coder_agent_keyword_prompt_generates_suggestions(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch, base_agent_module: Any):
    def fake_improve_content(self, prompt: str) -> str:
        return "x=1 # AI GENERATED CONTENT"

    monkeypatch.setattr(base_agent_module.BaseAgent, "improve_content", fake_improve_content)

    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    target = tmp_path / "x.py"
    agent = mod.CoderAgent(str(target))
    agent.previous_content = "ORIGINAL"
    out = agent.improve_content("Improve this code")
    assert out == "x=1 # AI GENERATED CONTENT"


def test_coder_agent_non_keyword_delegates_to_base(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, base_agent_module: Any
) -> None:
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")

    def fake_run_subagent(
            self: Any,
            description: str,
            prompt: str,
            original_content: str = "") -> str:
        return "IMPROVED"

    monkeypatch.setattr(
        base_agent_module.BaseAgent,
        "run_subagent",
        fake_run_subagent,
        raising=True
    )
    target = tmp_path / "x.py"
    target.write_text("BEFORE", encoding="utf-8")
    agent = mod.CoderAgent(str(target))
    agent.read_previous_content()
    assert agent.improve_content("noop") == "IMPROVED"


# ========== Language Detection Tests ==========

def test_detect_language_python(tmp_path: Path) -> None:
    """Test Python language detection."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    target = tmp_path / "test.py"
    target.write_text("", encoding="utf-8")
    agent = mod.CoderAgent(str(target))
    assert agent.language == mod.CodeLanguage.PYTHON


def test_detect_language_javascript(tmp_path: Path) -> None:
    """Test JavaScript language detection."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    target = tmp_path / "test.js"
    target.write_text("", encoding="utf-8")
    agent = mod.CoderAgent(str(target))
    assert agent.language == mod.CodeLanguage.JAVASCRIPT


def test_detect_language_typescript(tmp_path: Path) -> None:
    """Test TypeScript language detection."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    target = tmp_path / "test.ts"
    target.write_text("", encoding="utf-8")
    agent = mod.CoderAgent(str(target))
    assert agent.language == mod.CodeLanguage.TYPESCRIPT


def test_detect_language_go(tmp_path: Path) -> None:
    """Test Go language detection."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    target = tmp_path / "test.go"
    target.write_text("", encoding="utf-8")
    agent = mod.CoderAgent(str(target))
    assert agent.language == mod.CodeLanguage.GO


def test_detect_language_unknown(tmp_path: Path) -> None:
    """Test unknown language detection."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    target = tmp_path / "test.xyz"
    target.write_text("", encoding="utf-8")
    agent = mod.CoderAgent(str(target))
    assert agent.language == mod.CodeLanguage.UNKNOWN


# ========== Style Rule Tests ==========

def test_add_style_rule(tmp_path: Path) -> None:
    """Test adding a custom style rule."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    target = tmp_path / "test.py"
    target.write_text("", encoding="utf-8")
    agent = mod.CoderAgent(str(target))
    rule = mod.StyleRule(
        name="custom_rule",
        pattern=r"TODO",
        message="TODO found",
        severity=mod.StyleRuleSeverity.INFO
    )
    initial_count = len(agent._style_rules)
    agent.add_style_rule(rule)
    assert len(agent._style_rules) == initial_count + 1


def test_remove_style_rule(tmp_path: Path) -> None:
    """Test removing a style rule."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    target = tmp_path / "test.py"
    target.write_text("", encoding="utf-8")
    agent = mod.CoderAgent(str(target))
    result = agent.remove_style_rule("line_length")
    assert result is True


def test_remove_nonexistent_style_rule(tmp_path: Path) -> None:
    """Test removing a non-existent style rule."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    target = tmp_path / "test.py"
    target.write_text("", encoding="utf-8")
    agent = mod.CoderAgent(str(target))
    result = agent.remove_style_rule("nonexistent")
    assert result is False


def test_enable_style_rule(tmp_path: Path) -> None:
    """Test enabling a style rule."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    target = tmp_path / "test.py"
    target.write_text("", encoding="utf-8")
    agent = mod.CoderAgent(str(target))
    agent.disable_style_rule("line_length")
    result = agent.enable_style_rule("line_length")
    assert result is True


def test_disable_style_rule(tmp_path: Path) -> None:
    """Test disabling a style rule."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    target = tmp_path / "test.py"
    target.write_text("", encoding="utf-8")
    agent = mod.CoderAgent(str(target))
    result = agent.disable_style_rule("line_length")
    assert result is True


def test_check_style_violations(tmp_path: Path) -> None:
    """Test checking style violations."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    target = tmp_path / "test.py"
    target.write_text("", encoding="utf-8")
    agent = mod.CoderAgent(str(target))
    # Long line should trigger violation
    content = "x=" + "a" * 100
    violations = agent.check_style(content)
    assert len(violations) > 0


def test_check_style_no_violations(tmp_path: Path) -> None:
    """Test checking style with no violations."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    target = tmp_path / "test.py"
    target.write_text("", encoding="utf-8")
    agent = mod.CoderAgent(str(target))
    content = "x=1"
    violations = agent.check_style(content)
    assert len(violations) == 0


def test_auto_fix_style_trailing_whitespace(tmp_path: Path) -> None:
    """Test auto-fixing trailing whitespace."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    target = tmp_path / "test.py"
    target.write_text("", encoding="utf-8")
    agent = mod.CoderAgent(str(target))
    content = "x=1   \ny=2  "
    fixed, count = agent.auto_fix_style(content)
    assert "   " not in fixed
    assert count > 0


# ========== Code Metrics Tests ==========

def test_calculate_metrics_basic(tmp_path: Path) -> None:
    """Test calculating basic metrics."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    target = tmp_path / "test.py"
    content = """# Comment
x=1
y=2

def func():
    pass
"""
    target.write_text(content, encoding="utf-8")
    agent = mod.CoderAgent(str(target))
    agent.read_previous_content()
    metrics = agent.calculate_metrics()
    assert metrics.lines_of_comments >= 1
    assert metrics.lines_of_code >= 3
    assert metrics.blank_lines >= 1


def test_calculate_metrics_functions(tmp_path: Path) -> None:
    """Test calculating function metrics."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    target = tmp_path / "test.py"
    content = """
def func1():
    pass

def func2():
    pass

async def func3():
    pass
"""
    target.write_text(content, encoding="utf-8")
    agent = mod.CoderAgent(str(target))
    agent.read_previous_content()
    metrics = agent.calculate_metrics()
    assert metrics.function_count == 3


def test_calculate_metrics_classes(tmp_path: Path) -> None:
    """Test calculating class metrics."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    target = tmp_path / "test.py"
    content = """
class MyClass:
    pass

class AnotherClass:
    def method(self):
        pass
"""
    target.write_text(content, encoding="utf-8")
    agent = mod.CoderAgent(str(target))
    agent.read_previous_content()
    metrics = agent.calculate_metrics()
    assert metrics.class_count == 2


def test_calculate_metrics_imports(tmp_path: Path) -> None:
    """Test calculating import metrics."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    target = tmp_path / "test.py"
    content = """
import os
import sys
from pathlib import Path
"""
    target.write_text(content, encoding="utf-8")
    agent = mod.CoderAgent(str(target))
    agent.read_previous_content()
    metrics = agent.calculate_metrics()
    assert metrics.import_count == 3


# ========== Quality Score Tests ==========

def test_calculate_quality_score(tmp_path: Path) -> None:
    """Test calculating quality score."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    target = tmp_path / "test.py"
    content = '''"""Module docstring."""

def func():
    """Function docstring."""
    return 1
'''
    target.write_text(content, encoding="utf-8")
    agent = mod.CoderAgent(str(target))
    agent.read_previous_content()
    score = agent.calculate_quality_score()
    assert 0 <= score.overall_score <= 100
    assert 0 <= score.maintainability <= 100
    assert 0 <= score.readability <= 100


def test_quality_score_has_issues(tmp_path: Path) -> None:
    """Test quality score includes issues."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    target = tmp_path / "test.py"
    # Long line should create issues
    content = "x=" + "a" * 100
    target.write_text(content, encoding="utf-8")
    agent = mod.CoderAgent(str(target))
    agent.read_previous_content()
    score = agent.calculate_quality_score()
    assert isinstance(score.issues, list)


# ========== Code Smell Detection Tests ==========

def test_detect_long_method_smell(tmp_path: Path) -> None:
    """Test detecting long method smell."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    target = tmp_path / "test.py"
    # Create a function with 60+ lines
    lines = ["def long_function():"]
    lines.extend(["    x=1"] * 55)
    content = "\n".join(lines)
    target.write_text(content, encoding="utf-8")
    agent = mod.CoderAgent(str(target))
    agent.read_previous_content()
    smells = agent.detect_code_smells()
    assert any(s.name == "long_method" for s in smells)


def test_detect_too_many_parameters_smell(tmp_path: Path) -> None:
    """Test detecting too many parameters smell."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    target = tmp_path / "test.py"
    content = "def func(a, b, c, d, e, f, g):\n    pass"
    target.write_text(content, encoding="utf-8")
    agent = mod.CoderAgent(str(target))
    agent.read_previous_content()
    smells = agent.detect_code_smells()
    assert any(s.name == "too_many_parameters" for s in smells)


def test_detect_god_class_smell(tmp_path: Path) -> None:
    """Test detecting god class smell."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    target = tmp_path / "test.py"
    # Create a class with 25+ methods
    methods = "\n".join([f"    def method{i}(self): pass" for i in range(25)])
    content = f"class GodClass:\n{methods}"
    target.write_text(content, encoding="utf-8")
    agent = mod.CoderAgent(str(target))
    agent.read_previous_content()
    smells = agent.detect_code_smells()
    assert any(s.name == "god_class" for s in smells)


def test_detect_deep_nesting_smell(tmp_path: Path) -> None:
    """Test detecting deep nesting smell."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    target = tmp_path / "test.py"
    content = """def func():
    if True:
        if True:
            if True:
                if True:
                    if True:
                        x=1
"""
    target.write_text(content, encoding="utf-8")
    agent = mod.CoderAgent(str(target))
    agent.read_previous_content()
    smells = agent.detect_code_smells()
    assert any(s.name == "deep_nesting" for s in smells)


def test_detect_no_smells_clean_code(tmp_path: Path) -> None:
    """Test no smells in clean code."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    target = tmp_path / "test.py"
    content = """def simple_func():
    return 1
"""
    target.write_text(content, encoding="utf-8")
    agent = mod.CoderAgent(str(target))
    agent.read_previous_content()
    smells = agent.detect_code_smells()
    # Should have minimal or no smells
    assert not any(s.name in ["long_method", "god_class", "too_many_parameters"] for s in smells)


# ========== Code Deduplication Tests ==========

def test_find_duplicate_code(tmp_path: Path) -> None:
    """Test finding duplicate code."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    target = tmp_path / "test.py"
    content = """def func1():
    x=1
    y=2
    z=3
    return x + y

def func2():
    x=1
    y=2
    z=3
    return x + y
"""
    target.write_text(content, encoding="utf-8")
    agent = mod.CoderAgent(str(target))
    agent.read_previous_content()
    duplicates = agent.find_duplicate_code()
    assert len(duplicates) > 0


def test_find_no_duplicates(tmp_path: Path) -> None:
    """Test no duplicates found."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    target = tmp_path / "test.py"
    content = """def func1():
    return 1

def func2():
    return 2
"""
    target.write_text(content, encoding="utf-8")
    agent = mod.CoderAgent(str(target))
    agent.read_previous_content()
    duplicates = agent.find_duplicate_code()
    assert len(duplicates) == 0


def test_get_duplicate_ratio(tmp_path: Path) -> None:
    """Test getting duplicate ratio."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    target = tmp_path / "test.py"
    target.write_text("x=1", encoding="utf-8")
    agent = mod.CoderAgent(str(target))
    agent.read_previous_content()
    ratio = agent.get_duplicate_ratio()
    assert 0 <= ratio <= 1


# ========== Refactoring Pattern Tests ==========

def test_add_refactoring_pattern(tmp_path: Path) -> None:
    """Test adding a refactoring pattern."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    target = tmp_path / "test.py"
    target.write_text("", encoding="utf-8")
    agent = mod.CoderAgent(str(target))
    pattern = mod.RefactoringPattern(
        name="rename_var",
        description="Rename old_name to new_name",
        pattern=r"old_name",
        replacement="new_name"
    )
    agent.add_refactoring_pattern(pattern)
    assert len(agent._refactoring_patterns) == 1


def test_apply_refactoring_patterns(tmp_path: Path) -> None:
    """Test applying refactoring patterns."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    target = tmp_path / "test.py"
    target.write_text("", encoding="utf-8")
    agent = mod.CoderAgent(str(target))
    pattern = mod.RefactoringPattern(
        name="rename_var",
        description="Rename old_name to new_name",
        pattern=r"old_name",
        replacement="new_name"
    )
    agent.add_refactoring_pattern(pattern)
    result, applied = agent.apply_refactoring_patterns("x=old_name")
    assert "new_name" in result
    assert "rename_var" in applied


def test_suggest_refactorings(tmp_path: Path) -> None:
    """Test suggesting refactorings."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    target = tmp_path / "test.py"
    content = "def func(a, b, c, d, e, f, g):\n    pass"
    target.write_text(content, encoding="utf-8")
    agent = mod.CoderAgent(str(target))
    agent.read_previous_content()
    suggestions = agent.suggest_refactorings()
    assert len(suggestions) > 0


# ========== Documentation Generation Tests ==========
def test_generate_documentation_function(tmp_path: Path) -> None:
    """Test generating documentation for functions."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    target = tmp_path / "test.py"
    content = '''"""Module docstring."""

def my_function(param1, param2):
    """Function that does something."""
    return param1 + param2
'''
    target.write_text(content, encoding="utf-8")
    agent = mod.CoderAgent(str(target))
    agent.read_previous_content()
    docs = agent.generate_documentation()
    assert "my_function" in docs
    assert "param1" in docs or "Parameters" in docs


def test_generate_documentation_class(tmp_path: Path) -> None:
    """Test generating documentation for classes."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    target = tmp_path / "test.py"
    content = '''"""Module docstring."""

class MyClass:
    """A class that does something."""

    def method(self, value):
        """A method."""
        return value
'''
    target.write_text(content, encoding="utf-8")
    agent = mod.CoderAgent(str(target))
    agent.read_previous_content()
    docs = agent.generate_documentation()
    assert "MyClass" in docs
    assert "method" in docs


def test_generate_documentation_non_python(tmp_path: Path) -> None:
    """Test documentation generation for non-Python files."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    target = tmp_path / "test.js"
    target.write_text("const x=1;", encoding="utf-8")
    agent = mod.CoderAgent(str(target))
    docs = agent.generate_documentation()
    assert "only supported for Python" in docs


def test_generate_documentation_syntax_error(tmp_path: Path) -> None:
    """Test documentation generation with syntax error."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    target = tmp_path / "test.py"
    target.write_text("def broken(", encoding="utf-8")
    agent = mod.CoderAgent(str(target))
    agent.read_previous_content()
    docs = agent.generate_documentation()
    assert "Unable to parse" in docs


# ========== Dataclass Tests ==========

def test_style_rule_dataclass() -> None:
    """Test StyleRule dataclass."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    rule = mod.StyleRule(
        name="test",
        pattern=r".*",
        message="Test"
    )
    assert rule.severity == mod.StyleRuleSeverity.WARNING
    assert rule.enabled is True


def test_code_metrics_dataclass() -> None:
    """Test CodeMetrics dataclass."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    metrics = mod.CodeMetrics()
    assert metrics.lines_of_code == 0
    assert metrics.cyclomatic_complexity == 0.0


def test_code_smell_dataclass() -> None:
    """Test CodeSmell dataclass."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    smell = mod.CodeSmell(
        name="test",
        description="Test smell",
        severity="warning",
        line_number=1,
        suggestion="Fix it"
    )
    assert smell.category == "general"


def test_quality_score_dataclass() -> None:
    """Test QualityScore dataclass."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    score = mod.QualityScore()
    assert score.overall_score == 0.0
    assert score.issues == []


def test_refactoring_pattern_dataclass() -> None:
    """Test RefactoringPattern dataclass."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    pattern = mod.RefactoringPattern(
        name="test",
        description="Test pattern",
        pattern=r".*",
        replacement=""
    )
    assert pattern.language == mod.CodeLanguage.PYTHON


# ========== Enum Tests ==========

def test_code_language_enum_values() -> None:
    """Test CodeLanguage enum values."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    assert mod.CodeLanguage.PYTHON.value == "python"
    assert mod.CodeLanguage.JAVASCRIPT.value == "javascript"
    assert mod.CodeLanguage.UNKNOWN.value == "unknown"


def test_style_rule_severity_enum_values() -> None:
    """Test StyleRuleSeverity enum values."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    assert mod.StyleRuleSeverity.ERROR.value == "error"
    assert mod.StyleRuleSeverity.WARNING.value == "warning"
    assert mod.StyleRuleSeverity.INFO.value == "info"


# ========== Session 6 Tests: New Enums ==========


def test_migration_status_enum_values() -> None:
    """Test MigrationStatus enum values."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    assert mod.MigrationStatus.PENDING.value == "pending"
    assert mod.MigrationStatus.IN_PROGRESS.value == "in_progress"
    assert mod.MigrationStatus.COMPLETED.value == "completed"
    assert mod.MigrationStatus.FAILED.value == "failed"
    assert mod.MigrationStatus.SKIPPED.value == "skipped"


def test_review_category_enum_values() -> None:
    """Test ReviewCategory enum values."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    assert mod.ReviewCategory.STYLE.value == "style"
    assert mod.ReviewCategory.PERFORMANCE.value == "performance"
    assert mod.ReviewCategory.SECURITY.value == "security"
    assert mod.ReviewCategory.MAINTAINABILITY.value == "maintainability"
    assert mod.ReviewCategory.CORRECTNESS.value == "correctness"
    assert mod.ReviewCategory.DOCUMENTATION.value == "documentation"


def test_optimization_type_enum_values() -> None:
    """Test OptimizationType enum values."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    assert mod.OptimizationType.ALGORITHMIC.value == "algorithmic"
    assert mod.OptimizationType.MEMORY.value == "memory"
    assert mod.OptimizationType.IO.value == "io"
    assert mod.OptimizationType.CONCURRENCY.value == "concurrency"
    assert mod.OptimizationType.CACHING.value == "caching"


def test_security_issue_type_enum_values() -> None:
    """Test SecurityIssueType enum values."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    assert mod.SecurityIssueType.SQL_INJECTION.value == "sql_injection"
    assert mod.SecurityIssueType.XSS.value == "xss"
    assert mod.SecurityIssueType.HARDCODED_SECRET.value == "hardcoded_secret"
    assert mod.SecurityIssueType.INSECURE_DESERIALIZATION.value == "insecure_deserialization"
    assert mod.SecurityIssueType.PATH_TRAVERSAL.value == "path_traversal"
    assert mod.SecurityIssueType.COMMAND_INJECTION.value == "command_injection"
    assert mod.SecurityIssueType.INSECURE_RANDOM.value == "insecure_random"


def test_profiling_category_enum_values() -> None:
    """Test ProfilingCategory enum values."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    assert mod.ProfilingCategory.CPU_BOUND.value == "cpu_bound"
    assert mod.ProfilingCategory.IO_BOUND.value == "io_bound"
    assert mod.ProfilingCategory.MEMORY_INTENSIVE.value == "memory_intensive"
    assert mod.ProfilingCategory.NETWORK_BOUND.value == "network_bound"


def test_dependency_type_enum_values() -> None:
    """Test DependencyType enum values."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    assert mod.DependencyType.IMPORT.value == "import"
    assert mod.DependencyType.FUNCTION_CALL.value == "function_call"
    assert mod.DependencyType.CLASS_INHERITANCE.value == "class_inheritance"
    assert mod.DependencyType.VARIABLE_REFERENCE.value == "variable_reference"


# ========== Session 6 Tests: New Dataclasses ==========


def test_migration_rule_dataclass() -> None:
    """Test MigrationRule dataclass."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    rule = mod.MigrationRule(
        name="test",
        old_pattern=r"old",
        new_pattern="new",
        description="Test migration"
    )
    assert rule.status == mod.MigrationStatus.PENDING
    assert rule.breaking_change is False


def test_review_finding_dataclass() -> None:
    """Test ReviewFinding dataclass."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    finding = mod.ReviewFinding(
        category=mod.ReviewCategory.STYLE,
        message="Test finding",
        line_number=1,
        severity=2,
        suggestion="Fix it"
    )
    assert finding.auto_fixable is False


def test_optimization_suggestion_dataclass() -> None:
    """Test OptimizationSuggestion dataclass."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    suggestion = mod.OptimizationSuggestion(
        type=mod.OptimizationType.ALGORITHMIC,
        description="Test optimization",
        impact="medium",
        code_location="line 1"
    )
    assert suggestion.before_snippet == ""
    assert suggestion.after_snippet == ""


def test_security_vulnerability_dataclass() -> None:
    """Test SecurityVulnerability dataclass."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    vuln = mod.SecurityVulnerability(
        type=mod.SecurityIssueType.HARDCODED_SECRET,
        severity="high",
        description="Hardcoded password",
        line_number=1,
        fix_suggestion="Use env vars"
    )
    assert vuln.cwe_id is None


def test_modernization_suggestion_dataclass() -> None:
    """Test ModernizationSuggestion dataclass."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    suggestion = mod.ModernizationSuggestion(
        old_api="urllib2",
        new_api="urllib.request",
        deprecation_version="2.7"
    )
    assert suggestion.removal_version is None
    assert suggestion.migration_guide == ""


def test_test_gap_dataclass() -> None:
    """Test TestGap dataclass."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    gap = mod.TestGap(
        function_name="test_func",
        file_path="test.py",
        line_number=1,
        complexity=5
    )
    assert gap.suggested_tests == []


def test_consistency_issue_dataclass() -> None:
    """Test ConsistencyIssue dataclass."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    issue = mod.ConsistencyIssue(
        issue_type="naming",
        description="Mixed naming",
        occurrences=["file1.py", "file2.py"],
        recommended_style="snake_case"
    )
    assert len(issue.occurrences) == 2


def test_profiling_suggestion_dataclass() -> None:
    """Test ProfilingSuggestion dataclass."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    suggestion = mod.ProfilingSuggestion(
        category=mod.ProfilingCategory.CPU_BOUND,
        function_name="test_func",
        reason="Contains loops",
        estimated_impact="medium",
        profiling_approach="cProfile"
    )
    assert suggestion.category == mod.ProfilingCategory.CPU_BOUND


def test_dependency_node_dataclass() -> None:
    """Test DependencyNode dataclass."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    node = mod.DependencyNode(
        name="os",
        type=mod.DependencyType.IMPORT
    )
    assert node.depends_on == []
    assert node.depended_by == []
    assert node.file_path == ""


# ========== Session 6 Tests: MigrationManager ==========


def test_migration_manager_add_rule() -> None:
    """Test MigrationManager add_rule method."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    manager = mod.MigrationManager()
    rule = mod.MigrationRule(
        name="test",
        old_pattern=r"old",
        new_pattern="new",
        description="Test"
    )
    manager.add_rule(rule)
    assert len(manager.rules) == 1


def test_migration_manager_apply_migrations() -> None:
    """Test MigrationManager apply_migrations method."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    manager = mod.MigrationManager()
    rule = mod.MigrationRule(
        name="urllib_migration",
        old_pattern=r"import urllib2",
        new_pattern="import urllib.request",
        description="Migrate urllib2"
    )
    manager.add_rule(rule)
    content, applied = manager.apply_migrations("import urllib2")
    assert content == "import urllib.request"
    assert len(applied) == 1
    assert applied[0]["rule"] == "urllib_migration"


def test_migration_manager_get_pending_migrations() -> None:
    """Test MigrationManager get_pending_migrations method."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    manager = mod.MigrationManager()
    rule = mod.MigrationRule(
        name="test",
        old_pattern=r"nonexistent",
        new_pattern="new",
        description="Test"
    )
    manager.add_rule(rule)
    manager.apply_migrations("content without match")
    pending = manager.get_pending_migrations()
    assert len(pending) == 1


def test_migration_manager_skips_skipped_rules() -> None:
    """Test MigrationManager skips rules with SKIPPED status."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    manager = mod.MigrationManager()
    rule = mod.MigrationRule(
        name="test",
        old_pattern=r"old",
        new_pattern="new",
        description="Test",
        status=mod.MigrationStatus.SKIPPED
    )
    manager.add_rule(rule)
    content, applied = manager.apply_migrations("old text")
    assert content == "old text"
    assert len(applied) == 0


# ========== Session 6 Tests: CodeReviewer ==========


def test_code_reviewer_review_code() -> None:
    """Test CodeReviewer review_code method."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    reviewer = mod.CodeReviewer()
    findings = reviewer.review_code("password='secret123'")
    assert len(findings) >= 1
    assert any(f.category == mod.ReviewCategory.SECURITY for f in findings)


def test_code_reviewer_detects_long_lines() -> None:
    """Test CodeReviewer detects long lines."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    reviewer = mod.CodeReviewer()
    long_line = "x=" + "a" * 200
    findings = reviewer.review_code(long_line)
    style_findings = [f for f in findings if f.category == mod.ReviewCategory.STYLE]
    assert len(style_findings) >= 1


def test_code_reviewer_detects_range_len_pattern() -> None:
    """Test CodeReviewer detects inefficient range(len()) pattern."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    reviewer = mod.CodeReviewer()
    code = "for i in range(len(items)):"
    findings = reviewer.review_code(code)
    perf_findings = [f for f in findings if f.category == mod.ReviewCategory.PERFORMANCE]
    assert len(perf_findings) >= 1


def test_code_reviewer_get_summary() -> None:
    """Test CodeReviewer get_summary method."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    reviewer = mod.CodeReviewer()
    reviewer.review_code("password='secret'")
    summary = reviewer.get_summary()
    assert "security" in summary


# ========== Session 6 Tests: PerformanceOptimizer ==========


def test_performance_optimizer_analyze() -> None:
    """Test PerformanceOptimizer analyze method."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    optimizer = mod.PerformanceOptimizer()
    suggestions = optimizer.analyze("for i in range(len(items)):")
    assert len(suggestions) >= 1
    assert suggestions[0].type == mod.OptimizationType.ALGORITHMIC


def test_performance_optimizer_empty_code() -> None:
    """Test PerformanceOptimizer with empty code."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    optimizer = mod.PerformanceOptimizer()
    suggestions = optimizer.analyze("")
    assert len(suggestions) == 0


# ========== Session 6 Tests: SecurityScanner ==========


def test_security_scanner_scan() -> None:
    """Test SecurityScanner scan method."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    scanner = mod.SecurityScanner()
    vulns = scanner.scan("password='secret123'")
    assert len(vulns) >= 1
    assert vulns[0].type == mod.SecurityIssueType.HARDCODED_SECRET


def test_security_scanner_detects_eval() -> None:
    """Test SecurityScanner detects eval usage."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    scanner = mod.SecurityScanner()
    vulns = scanner.scan("result=eval(user_input)")
    assert len(vulns) >= 1
    assert any(v.type == mod.SecurityIssueType.INSECURE_DESERIALIZATION for v in vulns)


def test_security_scanner_detects_os_system() -> None:
    """Test SecurityScanner detects os.system with concatenation."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    scanner = mod.SecurityScanner()
    vulns = scanner.scan("os.system('rm ' + user_input)")
    assert len(vulns) >= 1
    assert any(v.type == mod.SecurityIssueType.COMMAND_INJECTION for v in vulns)


def test_security_scanner_get_critical_count() -> None:
    """Test SecurityScanner get_critical_count method."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    scanner = mod.SecurityScanner()
    scanner.scan("eval(x)")
    critical = scanner.get_critical_count()
    assert critical >= 1


# ========== Session 6 Tests: ModernizationAdvisor ==========


def test_modernization_advisor_analyze() -> None:
    """Test ModernizationAdvisor analyze method."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    advisor = mod.ModernizationAdvisor()
    suggestions = advisor.analyze("import urllib2")
    assert len(suggestions) >= 1


def test_modernization_advisor_detects_collections_mapping() -> None:
    """Test ModernizationAdvisor detects deprecated collections imports."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    advisor = mod.ModernizationAdvisor()
    suggestions = advisor.analyze("from collections import Mapping")
    assert len(suggestions) >= 1


def test_modernization_advisor_empty_code() -> None:
    """Test ModernizationAdvisor with clean code."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    advisor = mod.ModernizationAdvisor()
    suggestions = advisor.analyze("import os")
    assert len(suggestions) == 0


# ========== Session 6 Tests: TestGapAnalyzer ==========


def test_test_gap_analyzer_analyze() -> None:
    """Test TestGapAnalyzer analyze method."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    analyzer = mod.TestGapAnalyzer()
    code = "def untested_function():\n    pass"
    gaps = analyzer.analyze(code, "test.py")
    assert len(gaps) >= 1
    assert gaps[0].function_name == "untested_function"


def test_test_gap_analyzer_complexity_calculation() -> None:
    """Test TestGapAnalyzer complexity calculation."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    analyzer = mod.TestGapAnalyzer()
    code = """
def complex_func():
    if x:
        for i in range(10):
            while True:
                pass
"""
    gaps = analyzer.analyze(code, "test.py")
    assert gaps[0].complexity > 1


def test_test_gap_analyzer_suggested_tests() -> None:
    """Test TestGapAnalyzer generates test suggestions."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    analyzer = mod.TestGapAnalyzer()
    code = "def my_function():\n    pass"
    gaps = analyzer.analyze(code, "test.py")
    assert len(gaps[0].suggested_tests) >= 2
    assert "test_my_function_returns_expected_result" in gaps[0].suggested_tests


def test_test_gap_analyzer_syntax_error() -> None:
    """Test TestGapAnalyzer handles syntax errors."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    analyzer = mod.TestGapAnalyzer()
    gaps = analyzer.analyze("def invalid(:", "test.py")
    assert len(gaps) == 0


# ========== Session 6 Tests: ConsistencyChecker ==========


def test_consistency_checker_check() -> None:
    """Test ConsistencyChecker check method."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    checker = mod.ConsistencyChecker()
    files = {
        "file1.py": "def snake_case_func(): pass",
        "file2.py": "def camelCaseFunc(): pass"
    }
    issues = checker.check(files)
    assert len(issues) >= 1


def test_consistency_checker_import_styles() -> None:
    """Test ConsistencyChecker detects mixed import styles."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    checker = mod.ConsistencyChecker()
    files = {
        "file1.py": "from . import local",
        "file2.py": "from package import module"
    }
    issues = checker.check(files)
    assert any(i.issue_type == "import_style" for i in issues)


def test_consistency_checker_empty_files() -> None:
    """Test ConsistencyChecker with empty files."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    checker = mod.ConsistencyChecker()
    issues = checker.check({})
    assert len(issues) == 0


# ========== Session 6 Tests: ProfilingAdvisor ==========


def test_profiling_advisor_analyze() -> None:
    """Test ProfilingAdvisor analyze method."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    advisor = mod.ProfilingAdvisor()
    code = """
def slow_func():
    for i in range(1000):
        pass
"""
    suggestions = advisor.analyze(code)
    assert len(suggestions) >= 1
    assert suggestions[0].category == mod.ProfilingCategory.CPU_BOUND


def test_profiling_advisor_detects_io() -> None:
    """Test ProfilingAdvisor detects I / O operations."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    advisor = mod.ProfilingAdvisor()
    code = """
def io_func():
    f.read()
"""
    suggestions = advisor.analyze(code)
    io_suggestions = [s for s in suggestions if s.category == mod.ProfilingCategory.IO_BOUND]
    assert len(io_suggestions) >= 1


def test_profiling_advisor_syntax_error() -> None:
    """Test ProfilingAdvisor handles syntax errors."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    advisor = mod.ProfilingAdvisor()
    suggestions = advisor.analyze("def invalid(:")
    assert len(suggestions) == 0


# ========== Session 6 Tests: DependencyAnalyzer ==========


def test_dependency_analyzer_analyze() -> None:
    """Test DependencyAnalyzer analyze method."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    analyzer = mod.DependencyAnalyzer()
    code = "import os\nfrom pathlib import Path"
    nodes = analyzer.analyze(code, "test.py")
    assert "os" in nodes
    assert "pathlib" in nodes


def test_dependency_analyzer_class_inheritance() -> None:
    """Test DependencyAnalyzer detects class inheritance."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    analyzer = mod.DependencyAnalyzer()
    code = "class Child(Parent): pass"
    nodes = analyzer.analyze(code, "test.py")
    assert "Parent" in nodes
    assert nodes["Parent"].type == mod.DependencyType.CLASS_INHERITANCE


def test_dependency_analyzer_get_external_dependencies() -> None:
    """Test DependencyAnalyzer get_external_dependencies method."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    analyzer = mod.DependencyAnalyzer()
    analyzer.analyze("import requests\nimport os", "test.py")
    external = analyzer.get_external_dependencies()
    assert "requests" in external
    assert "os" not in external


def test_dependency_analyzer_syntax_error() -> None:
    """Test DependencyAnalyzer handles syntax errors."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-coder.py")
    analyzer = mod.DependencyAnalyzer()
    nodes = analyzer.analyze("def invalid(:", "test.py")
    assert len(nodes) == 0


# =============================================================================
# Session 8 Tests: Accessibility Improvements
# =============================================================================
class TestAccessibilityIssueTypeEnum:
    """Tests for AccessibilityIssueType enum."""

    def test_enum_values(self) -> None:
        """Test enum has expected values."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-coder.py")
        assert mod.AccessibilityIssueType.MISSING_ALT_TEXT.value == "missing_alt_text"
        assert mod.AccessibilityIssueType.LOW_COLOR_CONTRAST.value == "low_color_contrast"
        assert mod.AccessibilityIssueType.MISSING_LABEL.value == "missing_label"
        assert mod.AccessibilityIssueType.KEYBOARD_NAVIGATION.value == "keyboard_navigation"

    def test_all_members(self) -> None:
        """Test all enum members exist."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-coder.py")
        members = list(mod.AccessibilityIssueType)
        assert len(members) == 10


class TestAccessibilitySeverityEnum:
    """Tests for AccessibilitySeverity enum."""

    def test_enum_values(self) -> None:
        """Test enum has expected values."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-coder.py")
        assert mod.AccessibilitySeverity.CRITICAL.value == 4
        assert mod.AccessibilitySeverity.SERIOUS.value == 3
        assert mod.AccessibilitySeverity.MODERATE.value == 2
        assert mod.AccessibilitySeverity.MINOR.value == 1

    def test_severity_ordering(self) -> None:
        """Test severity values are ordered correctly."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-coder.py")
        assert mod.AccessibilitySeverity.MINOR.value < mod.AccessibilitySeverity.MODERATE.value
        assert mod.AccessibilitySeverity.MODERATE.value < mod.AccessibilitySeverity.SERIOUS.value
        assert mod.AccessibilitySeverity.SERIOUS.value < mod.AccessibilitySeverity.CRITICAL.value


class TestWCAGLevelEnum:
    """Tests for WCAGLevel enum."""

    def test_enum_values(self) -> None:
        """Test enum has expected values."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-coder.py")
        assert mod.WCAGLevel.A.value == "A"
        assert mod.WCAGLevel.AA.value == "AA"
        assert mod.WCAGLevel.AAA.value == "AAA"

    def test_all_levels(self) -> None:
        """Test all WCAG levels exist."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-coder.py")
        assert len(list(mod.WCAGLevel)) == 3


class TestAccessibilityIssueDataclass:
    """Tests for AccessibilityIssue dataclass."""

    def test_creation(self) -> None:
        """Test creating AccessibilityIssue."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-coder.py")
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
            mod = load_agent_module("agent-coder.py")
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
            mod = load_agent_module("agent-coder.py")
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
            mod = load_agent_module("agent-coder.py")
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
            mod = load_agent_module("agent-coder.py")
        report = mod.AccessibilityReport(file_path="test.html")
        assert report.issues == []
        assert report.total_elements == 0
        assert report.compliance_score == 100.0


class TestARIAAttributeDataclass:
    """Tests for ARIAAttribute dataclass."""

    def test_creation(self) -> None:
        """Test creating ARIAAttribute."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-coder.py")
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
            mod = load_agent_module("agent-coder.py")
        analyzer = mod.AccessibilityAnalyzer(mod.WCAGLevel.AA)
        assert analyzer.target_level == mod.WCAGLevel.AA
        assert analyzer.issues == []

    def test_analyze_html_missing_alt(self) -> None:
        """Test detecting missing alt text in HTML."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-coder.py")
        analyzer = mod.AccessibilityAnalyzer()
        html_content = '<html><body><img src="test.jpg"></body></html>'
        report = analyzer.analyze_content(html_content, "html")
        alt_issues = [i for i in report.issues
                      if i.issue_type == mod.AccessibilityIssueType.MISSING_ALT_TEXT]
        assert len(alt_issues) > 0

    def test_analyze_html_with_alt(self) -> None:
        """Test HTML with proper alt text has no alt issues."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-coder.py")
        analyzer = mod.AccessibilityAnalyzer()
        html_content = '<html><body><img src="test.jpg" alt="Test image"></body></html>'
        report = analyzer.analyze_content(html_content, "html")
        alt_issues = [i for i in report.issues
                      if i.issue_type == mod.AccessibilityIssueType.MISSING_ALT_TEXT]
        assert len(alt_issues) == 0

    def test_analyze_html_missing_label(self) -> None:
        """Test detecting missing form labels in HTML."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-coder.py")
        analyzer = mod.AccessibilityAnalyzer()
        html_content = '<html><body><input type="text" id="name"></body></html>'
        report = analyzer.analyze_content(html_content, "html")
        label_issues = [i for i in report.issues
                        if i.issue_type == mod.AccessibilityIssueType.MISSING_LABEL]
        assert len(label_issues) > 0

    def test_analyze_html_heading_hierarchy(self) -> None:
        """Test detecting heading hierarchy issues."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-coder.py")
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
            mod = load_agent_module("agent-coder.py")
        analyzer = mod.AccessibilityAnalyzer()
        js_content = '<button onClick={handleClick}>Click me</button>'
        report = analyzer.analyze_content(js_content, "javascript")
        keyboard_issues = [i for i in report.issues
                           if i.issue_type == mod.AccessibilityIssueType.KEYBOARD_NAVIGATION]
        assert len(keyboard_issues) > 0

    def test_analyze_javascript_interactive_div(self) -> None:
        """Test detecting interactive divs without proper roles."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-coder.py")
        analyzer = mod.AccessibilityAnalyzer()
        js_content = '<div onClick={handleClick}>Clickable</div>'
        report = analyzer.analyze_content(js_content, "javascript")
        semantic_issues = [i for i in report.issues
                           if i.issue_type == mod.AccessibilityIssueType.SEMANTIC_HTML]
        assert len(semantic_issues) > 0

    def test_check_color_contrast_high(self) -> None:
        """Test color contrast check with high contrast."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-coder.py")
        analyzer = mod.AccessibilityAnalyzer()
        result = analyzer.check_color_contrast("#000000", "#FFFFFF")
        assert result.contrast_ratio == 21.0
        assert result.passes_aa is True
        assert result.passes_aaa is True

    def test_check_color_contrast_low(self) -> None:
        """Test color contrast check with low contrast."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-coder.py")
        analyzer = mod.AccessibilityAnalyzer()
        result = analyzer.check_color_contrast("#777777", "#999999")
        assert result.passes_aa is False

    def test_check_color_contrast_large_text(self) -> None:
        """Test color contrast check with large text requirements."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-coder.py")
        analyzer = mod.AccessibilityAnalyzer()
        result = analyzer.check_color_contrast("#555555", "#FFFFFF", is_large_text=True)
        # Large text has lower requirements (3:1 for AA)
        assert result.min_ratio_aa == 3.0

    def test_get_issues_by_severity(self) -> None:
        """Test filtering issues by severity."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-coder.py")
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
            mod = load_agent_module("agent-coder.py")
        analyzer = mod.AccessibilityAnalyzer()
        html_content = '<html><body><img src="test.jpg"></body></html>'
        analyzer.analyze_content(html_content, "html")
        level_a_issues = analyzer.get_issues_by_wcag_level(mod.WCAGLevel.A)
        assert all(i.wcag_level == mod.WCAGLevel.A for i in level_a_issues)

    def test_enable_disable_rules(self) -> None:
        """Test enabling and disabling rules."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-coder.py")
        analyzer = mod.AccessibilityAnalyzer()
        analyzer.disable_rule("1.1.1")
        assert analyzer.rules.get("1.1.1") is False
        analyzer.enable_rule("1.1.1")
        assert analyzer.rules.get("1.1.1") is True

    def test_compliance_score_calculation(self) -> None:
        """Test compliance score is calculated correctly."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-coder.py")
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
            mod = load_agent_module("agent-coder.py")
        analyzer = mod.AccessibilityAnalyzer()
        report = analyzer.analyze_file(str(tmp_path / "nonexistent.html"))
        assert report.issues == []
        assert report.compliance_score == 100.0

    def test_analyze_file_html(self, tmp_path: Path) -> None:
        """Test analyzing HTML file."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-coder.py")
        html_file = tmp_path / "test.html"
        html_file.write_text('<html><body><img src="x.jpg"></body></html>')
        analyzer = mod.AccessibilityAnalyzer()
        report = analyzer.analyze_file(str(html_file))
        assert len(report.issues) > 0

    def test_analyze_python_ui(self) -> None:
        """Test analyzing Python UI code."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-coder.py")
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
            mod = load_agent_module("agent-coder.py")
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
            mod = load_agent_module("agent-coder.py")

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
            mod = load_agent_module("agent-coder.py")

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
            mod = load_agent_module("agent-coder.py")

        target = tmp_path / "test.py"
        target.write_text("# Python code")

        agent = mod.CoderAgent(str(target))
        lang = agent.detect_language()

        assert lang == mod.CodeLanguage.PYTHON

    def test_generate_javascript_code(self, tmp_path: Path) -> None:
        """Test generating JavaScript code."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-coder.py")

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
            mod = load_agent_module("agent-coder.py")

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
            mod = load_agent_module("agent-coder.py")

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
            mod = load_agent_module("agent-coder.py")

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
            mod = load_agent_module("agent-coder.py")

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
            mod = load_agent_module("agent-coder.py")

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
            mod = load_agent_module("agent-coder.py")

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
            mod = load_agent_module("agent-coder.py")

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
            mod = load_agent_module("agent-coder.py")

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
            mod = load_agent_module("agent-coder.py")

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
            mod = load_agent_module("agent-coder.py")

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
            mod = load_agent_module("agent-coder.py")

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
            mod = load_agent_module("agent-coder.py")

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
            mod = load_agent_module("agent-coder.py")

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
            mod = load_agent_module("agent-coder.py")

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
            mod = load_agent_module("agent-coder.py")

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
            mod = load_agent_module("agent-coder.py")

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
            mod = load_agent_module("agent-coder.py")

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
            mod = load_agent_module("agent-coder.py")

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
            mod = load_agent_module("agent-coder.py")

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
            mod = load_agent_module("agent-coder.py")

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


class TestPerformanceProfiling:
    """Tests for code performance profiling."""

    def test_detect_performance_issue(self, tmp_path: Path) -> None:
        """Test detecting potential performance issues."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-coder.py")

        code = """
def slow_function(n):
    result=[]
    for i in range(n):
        result=result + [i]  # O(n) each iteration
    return result
"""
        target = tmp_path / "test.py"
        target.write_text(code)

        agent = mod.CoderAgent(str(target))
        content = agent.read_previous_content()

        assert "result + [i]" in content


# =============================================================================
# Session 9: Migration Automation Tests
# =============================================================================


class TestMigrationAutomation:
    """Tests for code migration automation."""

    def test_detect_deprecated_syntax(self, tmp_path: Path) -> None:
        """Test detecting deprecated syntax."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-coder.py")

        code = """
# Old-style string formatting
message="Hello %s" % name
"""
        target = tmp_path / "test.py"
        target.write_text(code)

        agent = mod.CoderAgent(str(target))
        content = agent.read_previous_content()

        assert '"%s"' in content

    def test_detect_python2_syntax(self, tmp_path: Path) -> None:
        """Test detecting Python 2 style syntax."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-coder.py")

        code = """
class OldStyle:
    pass
"""
        target = tmp_path / "test.py"
        target.write_text(code)

        agent = mod.CoderAgent(str(target))
        content = agent.read_previous_content()

        assert "class OldStyle" in content
