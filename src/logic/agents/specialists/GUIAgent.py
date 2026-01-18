# Copyright 2026 PyAgent Authors
# GUIAgent: Graphical User Interface Automation Specialist - Phase 319 Enhanced

from __future__ import annotations
from src.core.base.Version import VERSION
import logging
import json
import re
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from src.core.base.BaseAgent import BaseAgent
from src.core.base.BaseUtilities import as_tool

__version__ = VERSION

class Framework(Enum):
    REACT = "react"
    VUE = "vue"
    SVELTE = "svelte"
    TKINTER = "tkinter"
    QT = "qt"
    FLUTTER = "flutter"
    ANDROID_XML = "android_xml"
    SWIFTUI = "swiftui"
    HTML_CSS = "html_css"

class ElementType(Enum):
    BUTTON = "button"
    INPUT = "input"
    TEXT = "text"
    IMAGE = "image"
    LIST = "list"
    CONTAINER = "container"
    NAVIGATION = "navigation"
    MODAL = "modal"
    FORM = "form"

@dataclass
class UIElement:
    """Represents a UI element with properties."""
    element_type: ElementType
    id: str
    bounds: Optional[Tuple[int, int, int, int]] = None  # x, y, width, height
    text: Optional[str] = None
    clickable: bool = False
    children: List['UIElement'] = field(default_factory=list)
    attributes: Dict[str, Any] = field(default_factory=dict)

@dataclass
class UIAction:
    """Represents an action to perform on a UI."""
    action_type: str  # click, type, scroll, swipe, long_press
    target_id: str
    parameters: Dict[str, Any] = field(default_factory=dict)

class GUIAgent(BaseAgent):
    """
    Agent specializing in interacting with and designing GUIs.
    Can generate layout code (Qt, React, Tkinter) and interpret UI snapshots.
    """

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._element_cache: Dict[str, UIElement] = {}
        self._action_history: List[UIAction] = []
        self._system_prompt = (
            "You are the GUI Agent. You design intuitive user interfaces and "
            "provide instructions for interacting with graphical applications. "
            "You prefer clean, responsive, accessible designs with good UX principles."
        )

    @as_tool
    async def design_layout(
        self, 
        framework: str, 
        description: str,
        responsive: bool = True,
        accessibility: bool = True,
        dark_mode: bool = False
    ) -> Dict[str, Any]:
        """Generates GUI layout code based on description."""
        framework_enum = Framework(framework.lower()) if framework.lower() in [f.value for f in Framework] else Framework.REACT
        
        prompt = (
            f"Framework: {framework_enum.value}\n"
            f"Description: {description}\n"
            f"Requirements:\n"
            f"- Responsive: {responsive}\n"
            f"- Accessibility (ARIA, semantic HTML): {accessibility}\n"
            f"- Dark mode support: {dark_mode}\n\n"
            "Generate complete, production-ready source code for this UI layout.\n"
            "Include:\n"
            "1. Component structure\n"
            "2. Styling (CSS/styled-components/etc.)\n"
            "3. Event handlers (placeholder functions)\n"
            "4. Accessibility attributes\n"
            "5. Brief comments explaining key sections"
        )
        
        code = await self.improve_content(prompt)
        
        return {
            "framework": framework_enum.value,
            "code": code,
            "features": {
                "responsive": responsive,
                "accessibility": accessibility,
                "dark_mode": dark_mode
            }
        }

    @as_tool
    async def interpret_ui_structure(self, ui_dump: str, format: str = "auto") -> Dict[str, Any]:
        """Analyzes a UI hierarchy (e.g., XML/JSON from Android or Web)."""
        prompt = (
            f"Analyze this UI hierarchy and identify interactive elements:\n\n"
            f"{ui_dump[:3000]}\n\n"
            "Output JSON with:\n"
            "{\n"
            '  "elements": [{"id": "...", "type": "button|input|text|...", "bounds": [x,y,w,h], "text": "...", "clickable": true/false}],\n'
            '  "navigation_structure": "description of nav flow",\n'
            '  "accessibility_issues": ["list of potential issues"],\n'
            '  "suggested_actions": [{"action": "click|type|scroll", "target": "element_id", "purpose": "..."}]\n'
            "}"
        )
        
        res = await self.improve_content(prompt)
        
        try:
            match = re.search(r"(\{[\s\S]*\})", res)
            if match:
                data = json.loads(match.group(1))
                
                # Cache elements
                for elem in data.get("elements", []):
                    ui_elem = UIElement(
                        element_type=ElementType(elem.get("type", "container")),
                        id=elem.get("id", "unknown"),
                        bounds=tuple(elem.get("bounds", [])) if elem.get("bounds") else None,
                        text=elem.get("text"),
                        clickable=elem.get("clickable", False)
                    )
                    self._element_cache[ui_elem.id] = ui_elem
                
                return data
        except Exception as e:
            logging.debug(f"GUIAgent: Parse error: {e}")
        
        return {"raw": res}

    @as_tool
    async def generate_action_sequence(
        self, 
        goal: str, 
        ui_dump: str
    ) -> Dict[str, Any]:
        """Generates a sequence of UI actions to achieve a goal."""
        prompt = (
            f"Goal: {goal}\n\n"
            f"Current UI State:\n{ui_dump[:2000]}\n\n"
            "Generate a sequence of actions to achieve this goal:\n"
            "Output JSON: {'actions': [{'action': 'click|type|scroll|swipe|wait', 'target': 'element_id', 'value': 'text to type (if applicable)', 'reason': 'why this action'}]}"
        )
        
        res = await self.improve_content(prompt)
        
        try:
            match = re.search(r"(\{[\s\S]*\})", res)
            if match:
                data = json.loads(match.group(1))
                
                # Record actions
                for action in data.get("actions", []):
                    self._action_history.append(UIAction(
                        action_type=action.get("action", "click"),
                        target_id=action.get("target", ""),
                        parameters={"value": action.get("value"), "reason": action.get("reason")}
                    ))
                
                return data
        except:
            pass
        
        return {"raw": res}

    @as_tool
    async def create_component(
        self, 
        component_type: str, 
        props: Dict[str, Any],
        framework: str = "react"
    ) -> Dict[str, Any]:
        """Creates a reusable UI component."""
        prompt = (
            f"Create a reusable {component_type} component for {framework}.\n\n"
            f"Props/Properties: {json.dumps(props, indent=2)}\n\n"
            "Requirements:\n"
            "1. TypeScript types (if applicable)\n"
            "2. Default prop values\n"
            "3. Proper accessibility\n"
            "4. Styling (CSS-in-JS or separate CSS)\n"
            "5. Usage example\n"
            "Output the complete component code."
        )
        
        code = await self.improve_content(prompt)
        
        return {
            "component_type": component_type,
            "framework": framework,
            "code": code,
            "props": props
        }

    @as_tool
    async def audit_accessibility(self, ui_code: str) -> Dict[str, Any]:
        """Audits UI code for accessibility issues."""
        prompt = (
            f"Audit this UI code for accessibility compliance (WCAG 2.1):\n\n"
            f"{ui_code[:3000]}\n\n"
            "Check for:\n"
            "1. Missing alt text on images\n"
            "2. Missing ARIA labels\n"
            "3. Color contrast issues\n"
            "4. Keyboard navigation problems\n"
            "5. Missing form labels\n"
            "6. Focus management issues\n\n"
            "Output JSON: {'score': 0-100, 'issues': [{'severity': 'critical|major|minor', 'description': '...', 'line': N, 'fix': '...'}], 'recommendations': [...]}"
        )
        
        res = await self.improve_content(prompt)
        
        try:
            match = re.search(r"(\{[\s\S]*\})", res)
            if match:
                return json.loads(match.group(1))
        except:
            pass
        
        return {"raw": res}

    @as_tool
    async def convert_framework(
        self, 
        source_code: str, 
        source_framework: str, 
        target_framework: str
    ) -> Dict[str, Any]:
        """Converts UI code between frameworks."""
        prompt = (
            f"Convert this {source_framework} UI code to {target_framework}:\n\n"
            f"{source_code[:3000]}\n\n"
            "Maintain:\n"
            "1. All functionality\n"
            "2. Styling (adapted to target framework conventions)\n"
            "3. Event handlers\n"
            "4. Component structure\n"
            "5. Accessibility features\n"
            "Output the complete converted code."
        )
        
        converted = await self.improve_content(prompt)
        
        return {
            "source_framework": source_framework,
            "target_framework": target_framework,
            "converted_code": converted
        }

    def get_cached_elements(self) -> Dict[str, Dict[str, Any]]:
        """Returns cached UI elements."""
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
        """Returns the action history."""
        return [
            {"action": a.action_type, "target": a.target_id, "params": a.parameters}
            for a in self._action_history
        ]
