#!/usr/bin/env python3
from __future__ import annotations
"""
Parser-safe stub: Multi-Channel Gateway Core (conservative).

Minimal stubbed gateway types to preserve imports during batch fixes.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class GatewayPresence:
    client_id: str
    status: str = "online"
    metadata: Dict[str, Any] = field(default_factory=dict)


class MultiChannelGatewayCore:
    def __init__(self, host: str = "127.0.0.1", port: int = 18789):
        self.host = host
        self.port = port
        self.running = False

    async def start(self):
        self.running = True

    async def stop(self):
        self.running = False


__all__ = ["GatewayPresence", "MultiChannelGatewayCore"]
