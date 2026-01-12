from __future__ import annotations
from typing import Dict, List, Any, Optional

class InterfaceSyncCore:
    """
    InterfaceSyncCore handles synchronization logic between CLI, GUI, and Web.
    It manages the central state and 'Theme Engine' propagation.
    """

    def __init__(self) -> None:
        self.themes: Dict[str, Dict[str, str]] = {
            "dark": {
                "background": "#1e1e1e",
                "foreground": "#d4d4d4",
                "accent": "#007acc"
            },
            "light": {
                "background": "#ffffff",
                "foreground": "#000000",
                "accent": "#005fb8"
            }
        }
        self.current_theme = "dark"

    def get_theme_payload(self, theme_name: Optional[str] = None) -> Dict[str, str]:
        """Returns the color palette for a given theme."""
        name = theme_name or self.current_theme
        return self.themes.get(name, self.themes["dark"])

    def broadcast_action(self, action_type: str, payload: Any) -> Dict[str, Any]:
        """
        Formats an action for broadcast to all interface targets.
        """
        return {
            "event": "INTERFACE_SYNC",
            "type": action_type,
            "payload": payload,
            "timestamp": "2026-01-08" # Simulated
        }

    def resolve_topology_state(self, agents: List[Dict[str, Any]], connections: List[tuple]) -> Dict[str, Any]:
        """
        Prepares a unified topology state for the Web viewer and GUI.
        """
        return {
            "nodes": agents,
            "edges": [{"from": c[0], "to": c[1]} for c in connections],
            "sync_version": "v2.0"
        }
