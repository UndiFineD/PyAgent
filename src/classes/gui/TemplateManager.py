#!/usr/bin/env python3
# Copyright (c) 2025 DebVisor contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""BMAD Template Manager for providing structured document templates."""

import tkinter as tk
from tkinter import ttk

BMAD_TEMPLATES = {
    "Select Template...": "",
    "Quick Spec (⚡)": """# QUICK SPEC: [Feature/Bug Name]
## Problem Description
[Describe what is happening vs what should happen]

## Proposed Solution
[Briefly describe how to fix it]

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
""",
    "PRD (📋)": """# PRODUCT REQUIREMENTS DOCUMENT: [Project Name]
## Executive Summary
[High-level goal]

## User Persona & Stories
[Who is it for? As a <user>, I want <goal> so that <benefit>]

## Functional Requirements
- Requirement 1: ...
- Requirement 2: ...

## Non-Functional Requirements
- Performance: ...
- Security: ...
""",
    "Technical Spec (🏗️)": """# TECHNICAL SPECIFICATION: [Project Name]
## Architecture Overview
[High-level design]

## Data Schema
[Database/Data structure changes]

## API Endpoints / Interfaces
[List of changes to interfaces]

## Implementation Plan
1. [Step 1]
2. [Step 2]
""",
    "Test Plan (🧪)": """# TEST PLAN: [Feature Name]
## Test Strategy
[Manual vs Automated, Unit vs E2E]

## Test Cases
1. [Normal Flow]
   - Input: ...
   - Expected: ...
2. [Edge Case]
   - Input: ...
   - Expected: ...
"""
}

class TemplateManager:
    """Manages insertion of BMAD-standard templates into text widgets."""
    @staticmethod
    def get_template_names():
        return list(BMAD_TEMPLATES.keys())

    @staticmethod
    def apply_template(text_widget, template_name):
        template = BMAD_TEMPLATES.get(template_name, "")
        if template:
            text_widget.delete("1.0", tk.END)
            text_widget.insert("1.0", template)
