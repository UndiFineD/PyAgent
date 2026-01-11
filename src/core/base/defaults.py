#!/usr/bin/env python3
"""Standard default configurations and templates for BaseAgent."""

from __future__ import annotations
from typing import List
from .models import PromptTemplate

DEFAULT_PROMPT_TEMPLATES: List[PromptTemplate] = [
    PromptTemplate(
        id="improve_code",
        name="Code Improvement",
        template="Improve the following code:\n\n{content}\n\nFocus on: {focus}",
        description="General code improvement template",
        tags=["code", "improvement"]
    ),
    PromptTemplate(
        id="add_docstrings",
        name="Add Docstrings",
        template="Add comprehensive docstrings to all functions and classes:\n\n{content}",
        description="Template for adding documentation",
        tags=["documentation"]
    ),
    PromptTemplate(
        id="fix_bugs",
        name="Bug Fix",
        template="Analyze and fix bugs in this code:\n\n{content}\n\nKnown issues: {issues}",
        description="Template for bug fixing",
        tags=["bugs", "fix"]
    ),
    PromptTemplate(
        id="add_tests",
        name="Generate Tests",
        template="Generate comprehensive tests for:\n\n{content}\n\nCoverage focus: {coverage}",
        description="Template for test generation",
        tags=["tests", "coverage"]
    ),
]
