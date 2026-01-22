#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# AgentBar: Real-time status and control component for Phase 51 Multimedia.

from typing import Dict, List, Any

class AgentBar:
    """
    Floating UI component for real-time Agent Status and Multimodal Stream Control.
    Integrates with the 120fps DVD-channel MUXer.
    """

    def __init__(self):
        self.status = "IDLE"
        self.active_channels = ["TEXT", "AUDIO", "VIDEO"]
        self.throughput_fps = 0.0
        self.latency_ms = 0.0
        self.sync_offset_ms = 0.0

    def update_metrics(self, fps: float, latency: float, sync: float):
        """Updates the real-time performance metrics."""
        self.throughput_fps = fps
        self.latency_ms = latency
        self.sync_offset_ms = sync
        self.status = "ACTIVE" if fps > 0 else "IDLE"

    def render_props(self) -> Dict[str, Any]:
        """Returns properties for React/Vue front-end rendering."""
        return {
            "component": "AgentBar",
            "props": {
                "status": self.status,
                "metrics": {
                    "fps": round(self.throughput_fps, 1),
                    "latency": f"{round(self.latency_ms, 2)}ms",
                    "sync": f"{round(self.sync_offset_ms, 2)}ms"
                },
                "channels": [
                    {"name": "TEXT", "active": True, "type": "0x01"},
                    {"name": "AUDIO", "active": self.throughput_fps > 0, "type": "0x02"},
                    {"name": "VIDEO", "active": self.throughput_fps > 50, "type": "0x03"}
                ],
                "theme": "quantum-dark"
            }
        }

    def get_styles(self) -> str:
        """Returns the CSS/Atomic styles for the component."""
        return """
        .agent-bar {
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 15px;
            padding: 10px 20px;
            background: rgba(10, 10, 15, 0.9);
            border: 1px solid #33f;
            border-radius: 30px;
            box-shadow: 0 0 20px rgba(0, 0, 255, 0.3);
            z-index: 10000;
            backdrop-filter: blur(10px);
        }
        .metric-item { color: #0f0; font-family: monospace; font-size: 12px; }
        .channel-dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; }
        .dot-active { background: #0f0; box-shadow: 0 0 5px #0f0; }
        .dot-idle { background: #555; }
        """
