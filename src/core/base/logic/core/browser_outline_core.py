#!/usr/bin/env python3
"""Minimal browser outline helpers used by tests."""
from __future__ import annotations



try:
    from dataclasses import dataclass
except ImportError:
    from dataclasses import dataclass

try:
    from typing import Any, Dict, List, Optional
except ImportError:
    from typing import Any, Dict, List, Optional



@dataclass
class BrowserElement:
    id: str
    tag: str
    text: str
    attributes: Dict[str, str]


class BrowserOutlineCore:
    """Simple outline generator for DOM-like element lists."""

    def __init__(self) -> None:
        self.elements: Dict[str, BrowserElement] = {}
        self._id_counter = 0

    def generate_outline(self, raw_elements: List[Dict[str, Any]]) -> str:
        """Convert a list of element dicts into a compact outline string."""
        self.elements.clear()
        self._id_counter = 0
        lines: List[str] = []

        for el in raw_elements:
            tag = el.get("tag", "element")
            text = (el.get("text") or el.get("aria-label") or "").strip()
            self._id_counter += 1
            prefix = "e"
            if tag == "button" or el.get("role") == "button":
                prefix = "b"
            elif tag == "a" or el.get("role") == "link":
                prefix = "l"
            elif tag in ("input", "textarea"):
                prefix = "i"

            el_id = f"{prefix}{self._id_counter}"
            attrs = {k: str(v) for k, v in (el.get("attributes") or {}).items()}

            be = BrowserElement(id=el_id, tag=tag, text=text, attributes=attrs)
            self.elements[el_id] = be

            attr_str = " ".join(f"[{k}={v}]" for k, v in attrs.items() if k in ("href", "type", "name"))
            line = f"[{el_id}] {tag} \"{text}\" {attr_str}".strip()
            lines.append(line)

        return "\n".join(lines)

    def resolve_label(self, label: str) -> Optional[BrowserElement]:
        return self.elements.get(label)


__all__ = ["BrowserElement", "BrowserOutlineCore"]
