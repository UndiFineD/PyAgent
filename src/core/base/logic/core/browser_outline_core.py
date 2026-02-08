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

from typing import List, Dict, Optional, Any
from dataclasses import dataclass

@dataclass
class BrowserElement:
    id: str  # e.g., "l1", "b2"
    tag: str # e.g., "button", "link", "input"
    text: str
    attributes: Dict[str, str]

class BrowserOutlineCore:
    """
    Transforms raw DOM/CDP data into a high-density 'Outline' for efficient LLM navigation.
    Reduces token usage by replacing complex selectors with simple labels (e.g., [l1]).
    Harvested from .external/AI-Auto-browser pattern.
    """

    def __init__(self):
        self.elements: Dict[str, BrowserElement] = {}
        self._id_counter = 0

    def generate_outline(self, raw_elements: List[Dict[str, Any]]) -> str:
        """
        Processes list of elements and returns a multi-line outline string.
        """
        self.elements.clear()
        self._id_counter = 0
        
        lines = []
        for el in raw_elements:
            tag = el.get("tag", "element")
            text = el.get("text", "").strip() or el.get("aria-label", "") or el.get("placeholder", "")
            
            # Identify the prefix based on tag
            prefix = "e" # default
            if tag == "button" or el.get("role") == "button":
                prefix = "b"
            elif tag == "a" or el.get("role") == "link":
                prefix = "l"
            elif tag == "input" or tag == "textarea":
                prefix = "i"
                
            self._id_counter += 1
            el_id = f"{prefix}{self._id_counter}"
            
            # Store element for later lookup
            self.elements[el_id] = BrowserElement(
                id=el_id,
                tag=tag,
                text=text,
                attributes=el.get("attributes", {})
            )
            
            # Build the outline line
            attr_str = " ".join([f"[{k}={v}]" for k, v in el.get("attributes", {}).items() if k in ["href", "type", "placeholder", "name"]])
            line = f"[{el_id}] {tag} \"{text}\" {attr_str}".strip()
            lines.append(line)
            
        return "\n".join(lines)

    def resolve_label(self, label: str) -> Optional[BrowserElement]:
        """Resolves a label like 'l1' back to its element details."""
        return self.elements.get(label)
