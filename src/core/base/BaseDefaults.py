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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Standard default configurations and templates for BaseAgent."""

from __future__ import annotations
from src.core.base.Version import VERSION
from .models import PromptTemplate

__version__ = VERSION

DEFAULT_PROMPT_TEMPLATES: list[PromptTemplate] = [
    PromptTemplate(
        id="improve_code",
        name="Code Improvement",
        template="Improve the following code:\n\n{content}\n\nFocus on: {focus}",
        description="General code improvement template",
        tags=["code", "improvement"],
    ),
    PromptTemplate(
        id="add_docstrings",
        name="Add Docstrings",
        template="Add comprehensive docstrings to all functions and classes:\n\n{content}",
        description="Template for adding documentation",
        tags=["documentation"],
    ),
    PromptTemplate(
        id="fix_bugs",
        name="Bug Fix",
        template="Analyze and fix bugs in this code:\n\n{content}\n\nKnown issues: {issues}",
        description="Template for bug fixing",
        tags=["bugs", "fix"],
    ),
    PromptTemplate(
        id="add_tests",
        name="Generate Tests",
        template="Generate comprehensive tests for:\n\n{content}\n\nCoverage focus: {coverage}",
        description="Template for test generation",
        tags=["tests", "coverage"],
    ),
]
