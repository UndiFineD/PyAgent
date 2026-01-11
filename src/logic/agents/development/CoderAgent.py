#!/usr/bin/env python3

"""Auto-extracted class from agent_coder.py"""

from __future__ import annotations

from src.core.base.types.CodeLanguage import CodeLanguage
from src.core.base.types.CodeMetrics import CodeMetrics
from src.core.base.types.CodeSmell import CodeSmell
from src.core.base.types.QualityScore import QualityScore
from src.core.base.types.RefactoringPattern import RefactoringPattern
from src.core.base.types.StyleRule import StyleRule
from src.core.base.types.StyleRuleSeverity import StyleRuleSeverity

from src.logic.agents.development.CoderCore import CoderCore, DEFAULT_PYTHON_STYLE_RULES, CODE_SMELL_PATTERNS
from src.core.base.BaseAgent import BaseAgent
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple
import ast
import hashlib
import logging
import math
import re
import shutil
import subprocess
import tempfile

class CoderAgent(BaseAgent):
    """Updates code files using AI assistance.

    Invariants:
    - self.file_path must point to a valid file path.

    - Supports Python files (.py) with syntax validation.
    - Supports multi - language code improvements.
    """

    # Language extension mappings
    LANGUAGE_EXTENSIONS: Dict[str, CodeLanguage] = {
        ".py": CodeLanguage.PYTHON,
        ".js": CodeLanguage.JAVASCRIPT,
        ".ts": CodeLanguage.TYPESCRIPT,
        ".java": CodeLanguage.JAVA,
        ".cpp": CodeLanguage.CPP,
        ".cc": CodeLanguage.CPP,
        ".cxx": CodeLanguage.CPP,
        ".go": CodeLanguage.GO,
        ".rs": CodeLanguage.RUST,
        ".rb": CodeLanguage.RUBY,
    }

    def __init__(self, file_path: str) -> None:
        self.file_path = Path(file_path)
        self._language = self._detect_language()
        super().__init__(file_path)
        
        # New: Delegate core logic to CoderCore (Rust-ready component)
        self.core = CoderCore(self._language)
        
        # Create copies of style rules to avoid cross-instance state leakage
        self._style_rules: List[StyleRule] = [
            StyleRule(
                name=r.name,
                pattern=r.pattern,
                message=r.message,
                severity=r.severity,
                enabled=r.enabled,
                language=r.language,
                auto_fix=r.auto_fix
            ) for r in DEFAULT_PYTHON_STYLE_RULES
        ]
        self._metrics: Optional[CodeMetrics] = None
        self._quality_score: Optional[QualityScore] = None
        self._code_smells: List[CodeSmell] = []
        self._refactoring_patterns: List[RefactoringPattern] = []
        self._duplicate_hashes: Dict[str, List[int]] = {}

    def _detect_language(self) -> CodeLanguage:
        """Detect the programming language from file extension."""
        ext = self.file_path.suffix.lower()
        return self.LANGUAGE_EXTENSIONS.get(ext, CodeLanguage.UNKNOWN)

    def detect_language(self) -> CodeLanguage:
        """Public wrapper to detect and return the file language.

        Returns:
            The detected CodeLanguage based on file extension.
        """
        self._language = self._detect_language()
        self.core.language = self._language  # Sync core
        return self._language

    @property
    def language(self) -> CodeLanguage:
        """Get the detected language."""
        return self._language

    @property
    def _is_python_file(self) -> bool:
        """Check if the file is a Python file."""
        return self._language == CodeLanguage.PYTHON

    # ========== Style Enforcement ==========
    def add_style_rule(self, rule: StyleRule) -> None:
        """Add a custom style rule."""
        self._style_rules.append(rule)

    def remove_style_rule(self, rule_name: str) -> bool:
        """Remove a style rule by name."""
        for i, rule in enumerate(self._style_rules):
            if rule.name == rule_name:
                del self._style_rules[i]
                return True
        return False

    def enable_style_rule(self, rule_name: str) -> bool:
        """Enable a style rule."""
        for rule in self._style_rules:
            if rule.name == rule_name:
                rule.enabled = True
                return True
        return False

    def disable_style_rule(self, rule_name: str) -> bool:
        """Disable a style rule."""
        for rule in self._style_rules:
            if rule.name == rule_name:
                rule.enabled = False
                return True
        return False

    def check_style(self, content: str) -> List[Dict[str, Any]]:
        """Check code against all enabled style rules."""
        return self.core.check_style(content, self._style_rules)

    def auto_fix_style(self, content: str) -> Tuple[str, int]:
        """Apply auto-fixes for style violations."""
        return self.core.auto_fix_style(content, self._style_rules)

    # ========== Code Metrics ==========
    def calculate_metrics(self, content: Optional[str] = None) -> CodeMetrics:
        """Calculate code metrics for the content."""
        if content is None:
            content = self.current_content or self.previous_content or ""
        self._metrics = self.core.calculate_metrics(content)
        return self._metrics

    def _get_test_coverage(self) -> float:
        """Attempt to calculate test coverage for the current file."""
        if not self._is_python_file or not self.file_path.exists():
            return 0.0

        # Heuristic: Check common test locations
        test_file = self.file_path.parent / f"test_{self.file_path.name}"
        if not test_file.exists():
            # Try tests/test_filename.py
            test_file = self.file_path.parent.parent / "tests" / f"test_{self.file_path.name}"

        if not test_file.exists():
            return 0.0

        # If pytest is available, try to run it with coverage
        if shutil.which('pytest'):
            try:
                # Run coverage for just this file
                # Use --cov-fail-under=0 to avoid exit code 1 if coverage is low
                result = subprocess.run(
                    [sys.executable, '-m', 'pytest', '--cov=' + str(self.file_path), '--cov-report=term-missing', str(test_file)],
                    capture_output=True,
                    text=True,
                    timeout=30,
                    check=False
                )
                # Parse output for percentage (e.g., TOTAL 10 2 80%)
                match = re.search(r'TOTAL.*?\s+(\d+)%', result.stdout)
                
                # Phase 108: Record coverage intelligence
                self._record(f"pytest --cov on {self.file_path.name}", 
                             f"Coverage: {match.group(1)}%" if match else "No match",
                             provider="Shell", model="pytest")
                
                if match:
                    return float(match.group(1))
            except Exception as e:
                logging.debug(f"Coverage calculation failed: {e}")

        return 0.0

    # ========== Code Quality Scoring ==========
    def calculate_quality_score(self, content: Optional[str] = None) -> QualityScore:
        """Calculate an overall code quality score."""
        if content is None:
            content = self.current_content or self.previous_content or ""
        metrics = self.calculate_metrics(content)
        style_violations = self.check_style(content)
        code_smells = self.detect_code_smells(content)
        coverage = self._get_test_coverage()
        
        self._quality_score = self.core.calculate_quality_score(metrics, style_violations, code_smells, coverage)
        return self._quality_score

    # ========== Code Smell Detection ==========
    def detect_code_smells(self, content: Optional[str] = None) -> List[CodeSmell]:
        """Detect code smells in the content."""
        if content is None:
            content = self.current_content or self.previous_content or ""
        self._code_smells = self.core.detect_code_smells(content)
        return self._code_smells

    # ========== Code Deduplication ==========
    def find_duplicate_code(
        self,
        content: Optional[str] = None,
        min_lines: int = 4
    ) -> List[Dict[str, Any]]:
        """Find duplicate code blocks."""
        if content is None:
            content = self.current_content or self.previous_content or ""
        return self.core.find_duplicate_code(content, min_lines)

    def get_duplicate_ratio(self, content: Optional[str] = None) -> float:
        """Calculate the ratio of duplicate code."""
        if content is None:
            content = self.current_content or self.previous_content or ""
        duplicates = self.find_duplicate_code(content)
        total_lines = len(content.split('\n'))
        if total_lines == 0:
            return 0.0
        duplicate_lines = sum(
            (d["occurrences"] - 1) * 4  # min_lines default
            for d in duplicates
        )
        return min(1.0, duplicate_lines / total_lines)

    # ========== Refactoring Patterns ==========
    def add_refactoring_pattern(self, pattern: RefactoringPattern) -> None:
        """Add a refactoring pattern."""
        self._refactoring_patterns.append(pattern)

    def apply_refactoring_patterns(self, content: str) -> Tuple[str, List[str]]:
        """Apply all registered refactoring patterns."""
        result = content
        applied: List[str] = []
        for pattern in self._refactoring_patterns:
            if pattern.language != self._language:
                continue
            new_result = re.sub(pattern.pattern, pattern.replacement, result)
            if new_result != result:
                applied.append(pattern.name)
                result = new_result
        return result, applied

    def suggest_refactorings(self, content: Optional[str] = None) -> List[Dict[str, str]]:
        """Suggest possible refactorings based on code analysis."""
        if content is None:
            content = self.current_content or self.previous_content or ""
        return self.core.suggest_refactorings(content)

    # ========== Documentation Generation ==========
    def generate_documentation(self, content: Optional[str] = None) -> str:
        """Generate documentation from code."""
        if content is None:
            content = self.current_content or self.previous_content or ""
        return self.core.generate_documentation(content)

    # ========== Core Methods ==========
    def _get_default_content(self) -> str:
        """Return default content for new code files."""
        return "# Code file\n\n# Add code here\n"

    def _get_fallback_response(self) -> str:
        """Return fallback response when Copilot is unavailable."""
        return ("# AI Improvement Unavailable\n"
                "# GitHub CLI not found. Install from https://cli.github.com/\n\n"
                "# Original code preserved below:\n\n")

    def _validate_syntax(self, content: str) -> bool:
        """Validate Python syntax using ast."""
        return self.core.validate_syntax(content)

    def _validate_flake8(self, content: str) -> bool:
        """Validate Python code using flake8 if available."""
        return self.core.validate_flake8(content)

    def improve_content(self, prompt: str) -> str:
        """Use AI to improve the code with specific coding suggestions."""
        logging.info(f"Improving content for {self.file_path}")
        # Call base implementation directly to use AI backend
        new_content = super().improve_content(prompt)
        # Validate syntax
        if not self._validate_syntax(new_content):
            logging.error("Generated code failed syntax validation. Reverting.")
            self.current_content = self.previous_content
            return self.previous_content
        logging.debug("Syntax validation passed")
        # Validate style (flake8)
        if not self._validate_flake8(new_content):
            logging.warning("Generated code failed style validation (flake8). Proceeding anyway.")
        else:
            logging.debug("Style validation passed")
        return new_content


