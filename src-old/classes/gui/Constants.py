#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/classes/gui/Constants.description.md

# Constants

**File**: `src\classes\gui\Constants.py`  
**Type**: Python Module  
**Summary**: 0 classes, 0 functions, 2 imports  
**Lines**: 108  
**Complexity**: 0 (simple)

## Overview

Python module containing implementation for Constants.

## Dependencies

**Imports** (2):
- `__future__.annotations`
- `src.core.base.version.VERSION`

---
*Auto-generated documentation*
## Source: src-old/classes/gui/Constants.improvements.md

# Improvements for Constants

**File**: `src\classes\gui\Constants.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 108 lines (medium)  
**Complexity**: 0 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `Constants_test.py` with pytest tests

## Best Practices Checklist

- [x] All classes have docstrings
- [x] All public methods have docstrings
- [x] Type hints are present
- [x] pytest tests cover main functionality
- [x] Error handling is robust
- [x] Code follows PEP 8 style guide
- [x] No code duplication
- [x] Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

from __future__ import annotations

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
from src.core.base.version import VERSION

__version__ = VERSION

# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

# You may obtain a copy of the License at
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Constants and definitions for the BMAD Method and PyAgent GUI."""

# BMAD Agent Roles
BMAD_AGENTS = [
    "Developer",
    "Architect",
    "PM",
    "Scrum Master",
    "UX Designer",
    "Test Architect",
    "Analyst",
    "BMad Master",
    "Tech Writer",
    "Security Auditor",
    "DevOps Engineer",
    "Researcher",
    "SQL Specialist",
    "Web Searcher",
    "Moderator",
    "Financial Advisor",
    "Image Generator (2D/3D)"
]

# BMAD Methodology Tracks
BMAD_TRACKS = {
    "Quick Flow": {
        "desc": "Bug fixes, small features (< 5 mins)",
        "phases": ["Analysis", "Implementation", "Validation"]
    },
    "BMad Method": {
        "desc": "Products, platforms (PRD + Arch + UX, < 15 mins)",
        "phases": ["Analysis", "Planning", "Solutioning", "Implementation", "Validation"]
    },
    "Enterprise": {
        "desc": "Compliance, scale (Full governance suite, < 30 mins)",
        "phases": ["Governance", "Analysis", "Planning", "Solutioning", "Implementation", "Quality", "Compliance"]
    },
    "Vibe Coding (2025)": {
        "desc": "Research-driven AI workflow (Research/Define/Design/Prep/Build)",
        "phases": ["Research", "Define", "Design", "Agent Prep", "Build", "Validation"]
    }
}

# BMAD Methodology Phases
BMAD_PHASES = [
    "Analysis",
    "Planning",
    "Solutioning",
    "Implementation",
    "Validation"
]

# Agent Specific Instructions (Placeholders for BMAD instructions)
DEFAULT_INSTRUCTIONS = {
    "Developer": "Act as a Senior Software Engineer. Implement features with high performance, modularity, and clean code principles. Use modern libraries and maintain consistent style. Focus on idiomatic Python and best practices.",
    "Architect": "Act as a Principal Architect. Define system boundaries, selection of frameworks, and scalability strategies. Ensure modularity and future-proofing in all designs. Implement Multi-Agent Orchestration principles.",
    "PM": "Act as a Technical Product Manager. Translate business goals into technical requirements. Organize tasks into logical milestones and verify acceptance criteria. Use iterative refinement workflows.",
    "UX Designer": "Act as a Senior UX/UI Designer. Focus on user-centric design, accessibility (WCAG), and responsive layouts. Provide detailed visual specifications and component logic for multi-modal interfaces.",
    "Test Architect": "Act as a Quality Lead. Design comprehensive test suites including unit, integration, and end-to-end tests. Focus on boundary cases, regression reliability, and RAG evaluation metrics.",
    "Security Auditor": "Act as a Security Expert. Identify potential vulnerabilities, perform dependency scans, and ensure data privacy compliance. Follow OWASP Best Practices and LLM-ops security standards.",
    "Tech Writer": "Act as a Lead Technical Writer. Produce clear, concise documentation for APIs, users, and internal developers. Use structured formats like Markdown and ensure knowledge graph consistency.",
    "Researcher": "Act as a Market/Tech Researcher. Scan for current trends, competitive analysis, and emerging technologies using available search tools. Synthesize findings into actionable technical reports for 2025."
}

# Model Token Limits (Context Window Management)
MODEL_TOKENS = {
    "gpt-4o": 128000,
    "gpt-3.5-turbo": 16385,
    "claude-3-5-sonnet": 200000,
    "default": 16385
}

# Default Target File Extensions
DEFAULT_EXTENSIONS = [".py", ".js", ".ts", ".html", ".css", ".md", ".json", ".yaml"]

# GUI Layout Constants
DEFAULT_WINDOW_SIZE = "1400x900"
AGENT_COLUMN_WIDTH = 320
LEFT_PANEL_WIDTH = 400
