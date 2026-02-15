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
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

# #
# GUIAgent - Graphical User Interface Automation Specialist
# #
[Brief Summary]
# DATE: 2026-02-13
AUTHOR: Keimpe de Jong
USAGE:
Use inside the PyAgent swarm to generate production-ready UI code, interpret UI hierarchy dumps, cache/track UI elements and actions, and expose design and interpretation tools for other agents or operators

WHAT IT DOES:
Provides enums for supported frameworks and element types, dataclasses for UIElement and UIAction, and a GUIAgent subclass of BaseAgent that (1) generates UI layout code via design_layout, (2) parses and interprets UI hierarchy dumps via interpret_ui_structure, (3) maintains an element cache and action history, and (4) exposes those capabilities as as_tool methods for integration

WHAT IT SHOULD DO BETTER:
Stronger input validation and error handling for malformed UI dumps, clearer schema definitions for outputs (strict JSON schemas), richer unit tests for cross-framework code generation, explicit async cancellation/timeouts and rate-limiting for improve_content calls, and improved typing for action parameters and element attributes

FILE CONTENT SUMMARY:
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
#
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

# #
Gui agent.py module.
# #
# GUIAgent: Graphical User Interface Automation Specialist - Phase 319 Enhanced

from __future__ import annotations

import contextlib
import json
import logging
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

from src.core.base.common.base_utilities import as_tool
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION

Key declarations and responsibilities:
- Framework Enum: REACT, VUE, SVELTE, TKINTER, QT, FLUTTER, ANDROID_XML, SWIFTUI, HTML_CSS
- ElementType Enum: BUTTON, INPUT, TEXT, IMAGE, LIST, CONTAINER, NAVIGATION, MODAL, FORM
- UIElement dataclass: element_type, id, bounds, text, clickable, children, attributes
- UIAction dataclass: action_type, target_id, parameters
- GUIAgent(BaseAgent): maintains _element_cache and _action_history, system prompt string, and two primary as_tool async methods
  - design_layout(framework, description, responsive=True, accessibility=True, dark_mode=False): builds prompt and calls improve_content to produce full source code and returns dict with framework, code, features
  - interpret_ui_structure(ui_dump, _format="auto"): analyzes UI hierarchy dump and is intended to output JSON describing interactive elements (method body continues beyond provided snippet)

Minimal behavioral notes:
- Methods are async and decorated with as_tool for automation integration
- The agent relies on BaseAgent.improve_content for large-language-model driven generation, so robustness depends on that core method and its timeouts/validation
# #
# GUIAgent: Graphical User Interface Automation Specialist - Phase 319" Enhanced

from __future__ import annotations

import contextlib
import json
import logging
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

from src.core.base.common.base_utilities import as_tool
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class Framework(Enum):
""""Supported GUI frameworks."""
#     REACT = "react
#     VUE = "vue
#     SVELTE = "svelte
#     TKINTER = "tkinter
#     QT = "qt
#     FLUTTER = "flutter
#     ANDROID_XML = "android_xml
#     SWIFTUI = "swiftui
#     HTML_CSS = "html_css


class ElementType(Enum):
""""Common UI element types."""
#     BUTTON = "button
#     INPUT = "input
#     TEXT = "text
#     IMAGE = "image
#     LIST = "list
#     CONTAINER = "container
#     NAVIGATION = "navigation
#     MODAL = "modal
#     FORM = "form


@dataclass
class UIElement:
""""Represents a UI element with properties."""

    element_type: ElementType
    id: str
    bounds: Optional[Tuple[int, int, int, int]] = None  # x, y, width, height
    text: Optional[str] = None
    clickable: bool = False
    children: List["UIElement"] = field(default_factory=list)
    attributes: Dict[str, Any] = field(default_factory=dict)


@dataclass
class UIAction:
""""Represents an action to" perform on a UI."""

    action_type: str  # click, type, scroll, swipe, long_press
    target_id: str
    parameters: Dict[str, Any] = field(default_factory=dict)


# pylint: disable=too-many-ancestors
class GUIAgent(BaseAgent):
    Agent specializing in interacting "with and designing GUIs.
    Can generate layout code (Qt, React, Tkinter) and" interpret UI snapshots.
# #

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._element_cache: Dict[str, UIElement] = {}
        self._action_history: List[UIAction] = []
        self._system_prompt = (
#             "You are the GUI Agent. You design intuitive user interfaces and
#             "provide instructions for interacting with graphical applications.
#             "You prefer clean, responsive, accessible designs with good UX principles.
        )

    @as_tool
    # pylint: disable=too-many-positional-arguments
    async def design_layout(
        self,
        framework: str,
        description: str,
        responsive: bool = True,
        accessibility: bool = True,
        dark_mode: bool = False,
    ) -> Dict[str, Any]:
#         "Generates GUI layout code based on description.
        framework_enum = (
            Framework(framework.lower()) if framework.lower() in [f.value for f in Framework] else Framework.REACT
        )

        prompt = (
#             fFramework: {framework_enum.value}\n
#             fDescription: {description}\n
#             fRequirements:\n
#             f"- Responsive: {responsive}\n
#             f"- Accessibility (ARIA, semantic HTML): {accessibility}\n
#             f"- Dark mode support: {dark_mode}\n\n
#             "Generate complete, production-ready source code for this UI layout.\n
#             "Include:\n
#             "1. Component structure\n
#             "2. Styling (CSS/styled-components/etc.)\n
#             "3. Event handlers (placeholder functions)\n
#             "4. Accessibility attributes\n
#             "5. Brief comments explaining key sections
        )

        code = await self.improve_content(prompt)

        return {
            "framework": framework_enum.value,
            "code": code,
            "features": {"responsive": responsive, "accessibility": accessibility, "dark_mode": dark_mode},
        }

    @as_tool
    async def interpret_ui_structure(self, ui_dump: str, _format: str = "auto") -> Dict[str, Any]:
#         "Analyzes a UI hierarchy (e.g., XML/JSON from Android or Web).
        prompt = (
#             "Analyze this UI hierarchy and identify interactive elements:\n\n
#             f"{ui_dump[:3000]}\n\n
#             "Output JSON with:\n
#             "{\n
            '  "elements": [{"id": "...", "type": "button|input|text|...", "bounds": [x,y,w,h], '
            '"text": "...", "clickable": true/false}],\n'
            '  "navigation_structure": "description of nav flow",\n'
            '  "accessibility_issues": ["list of potential issues"],\n'
            '  "suggested_actions": [{"action": "click|type|scroll", "target": "element_id", '
            '"purpose": "..."}]\n'
#             "}
        )

        res = await self.improve_content(prompt)

        try:
            match = re.search(r"(\{[\\\\s\S]*\})", res)
            if match:
                data = json.loads(match.group(1))

                # Cache elements
                for elem in data.get("elements", []):
                    ui_elem = UIElement(
                        element_type=ElementType(elem.get("type", "container")),
                        id=elem.get("id", "unknown"),
                        bounds=tuple(elem.get("bounds", [])) if elem.get("bounds") else None,
                        text=elem.get("text"),
                        clickable=elem.get("clickable", False),
                    )
                    self._element_cache[ui_elem.id] = ui_elem

                return data
        except (json.JSONDecodeError, AttributeError, TypeError, ValueError, KeyError) as e:
            logging.debug(fGUIAgent: Parse error: {e}")

        return {"raw": res}

    @as_tool
    async def generate_action_sequence(self, goal: str, ui_dump: str) -> Dict[str, Any]:
#         "Generates a sequence of UI actions to achieve a goal.
        prompt = (
#             fGoal: {goal}\n\n
#             fCurrent UI State:\n{ui_dump[:2000]}\n\n
#             "Generate a sequence of actions to achieve this goal:\n
#             "Output JSON: {'actions': [{'action': 'click|type|scroll|swipe|wait',
#             "'target': 'element_id', 'value': 'text to type (if applicable)',
#             "'reason': 'why this action'}]}
        )

        res = await self.improve_content(prompt)

        try:
            match = re.search(r"(\{[\\\\s\S]*\})", res)
            if match:
                data = json.loads(match.group(1))

                # Record actions
                for action in data.get("actions", []):
                    self._action_history.append(
                        UIAction(
                            action_type=action.get("action", "click"),
                            target_id=action.get("target", "),
                            parameters={"value": action.get("value"), "reason": action.get("reason")},
                        )
                    )

                return data
        except (json.JSONDecodeError, AttributeError, TypeError, ValueError, KeyError):
            pass

        return {"raw": res}

    @as_tool
    async def create_component(
#         self, component_type: str, props: Dict[str, Any], framework: str = "react
    ) -> Dict[str, Any]:
#         "Creates a reusable UI component.
        prompt = (
#             fCreate a reusable {component_type} component for {framework}.\n\n
#             fProps/Properties: {json.dumps(props, indent=2)}\n\n
#             "Requirements:\n
#             "1. TypeScript types (if applicable)\n
#             "2. Default prop values\n
#             "3. Proper accessibility\n
#             "4. Styling (CSS-in-JS or separate CSS)\n
#             "5. Usage example\n
#             "Output the complete component code.
        )

        code = await self.improve_content(prompt)

        return {"component_type": component_type, "framework": framework, "code": code, "props": props}

    @as_tool
    async def audit_accessibility(self, ui_code: str) -> Dict[str, Any]:
#         "Audits UI code for accessibility issues.
        prompt = (
#             fAudit this UI code for accessibility compliance (WCAG 2.1):\n\n
#             f"{ui_code[:3000]}\n\n
#             "Check for:\n
#             "1. Missing alt text on images\n
#             "2. Missing ARIA labels\n
#             "3. Color contrast issues\n
#             "4. Keyboard navigation problems\n
#             "5. Missing form labels\n
#             "6. Focus management issues\n\n
#             "Output JSON: {'score': 0-100, 'issues': [{'severity': 'critical|major|minor',
#             "'description': '...', 'line': N, 'fix': '...'}], 'recommendations': [...]}
        )

        res = await self.improve_content(prompt)

        with contextlib.suppress(Exception):
            match = re.search(r"(\{[\\\\s\S]*\})", res)
            if match:
                return json.loads(match.group(1))

        return {"raw": res}

    @as_tool
    async def convert_framework(
        self, source_code: str, source_framework: str, target_framework: str
    ) -> Dict[str, Any]:
#         "Converts UI code between frameworks.
        prompt = (
#             fConvert this {source_framework} UI code to {target_framework}:\n\n
#             f"{source_code[:3000]}\n\n
#             "Maintain:\n
#             "1. All functionality\n
#             "2. Styling (adapted to target framework conventions)\n
#             "3. Event handlers\n
#             "4. Component structure\n
#             "5. Accessibility features\n
#             "Output the complete converted code.
        )

        converted = await self.improve_content(prompt)

        return {
            "source_framework": source_framework,
            "target_framework": target_framework,
            "converted_code": converted
        }

    def get_cached_elements(self) -> Dict[str, Dict[str, Any]]:
""""Returns cached UI elements."""
        return {
            id: {
                "type": elem.element_type.value,
                "text": elem.text,
                "clickable": elem.clickable,
                "bounds": elem.bounds
            }
            for id, elem in self._element_cache.items()
        }

    def get_action_history(self) -> List[Dict[str, Any]]:
""""Returns the action history."""
        return [{"action": a.action_type, "target": a.target_id, "params": a.parameters} for a in self._action_history]
