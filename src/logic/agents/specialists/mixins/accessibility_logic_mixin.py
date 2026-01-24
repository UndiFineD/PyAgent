
"""
Accessibility logic mixin.py module.
"""
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from src.core.base.common.types.accessibility_report import AccessibilityReport

if TYPE_CHECKING:
    from src.logic.agents.specialists.accessibility_agent import \
        AccessibilityAgent


class AccessibilityLogicMixin:
    """Mixin for entry-point analysis logic and rule management in AccessibilityAgent."""

    def analyze_file(self: AccessibilityAgent, file_path: str) -> AccessibilityReport:
        """Analyze a file for accessibility issues."""
        self.issues.clear()
        path = Path(file_path)
        if not path.exists():
            return AccessibilityReport(file_path=file_path)
        content = path.read_text(encoding="utf-8")
        # Analyze based on file type
        if path.suffix in (".html", ".htm"):
            self._analyze_html(content)
        elif path.suffix == ".py":
            self._analyze_python_ui(content)
        elif path.suffix in (".js", ".jsx", ".ts", ".tsx"):
            self._analyze_javascript_ui(content)
        return self._generate_report(file_path)

    def analyze_content(self: AccessibilityAgent, content: str, file_type: str = "html") -> AccessibilityReport:
        """Analyze content string for accessibility issues."""
        self.issues.clear()
        if file_type == "html":
            self._analyze_html(content)
        elif file_type == "python":
            self._analyze_python_ui(content)
        elif file_type in ("javascript", "react"):
            self._analyze_javascript_ui(content)
        return self._generate_report("content")

    def enable_rule(self: AccessibilityAgent, wcag_criterion: str) -> None:
        """Enable a specific WCAG rule."""
        if wcag_criterion in self.rules:
            self.rules[wcag_criterion] = True

    def disable_rule(self: AccessibilityAgent, wcag_criterion: str) -> None:
        """Disable a specific WCAG rule."""
        if wcag_criterion in self.rules:
            self.rules[wcag_criterion] = False
