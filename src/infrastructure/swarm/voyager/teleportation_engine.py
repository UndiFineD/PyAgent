# Copyright 2026 PyAgent Authors
# Phase 319: Multi-Cloud Teleportation (Teleportation Engine)

import msgpack
import zlib
import base64
from typing import Any, Dict, Optional
from src.observability.structured_logger import StructuredLogger
from src.core.base.lifecycle.version import VERSION

logger = StructuredLogger(__name__)

class TeleportationEngine:
    """
    Handles the serialization and deserialization of agent states for 
    cross-machine 'teleportation'.
    """
    
    @staticmethod
    def capture_agent_state(agent: Any) -> bytes:
        """
        Captures the complete state of an agent into a compressed binary blob.
        """
        logger.info(f"Teleportation: Capturing state for agent {getattr(agent, 'name', 'Unknown')}")
        
        # Extract core state
        # In a real scenario, we'd use the persistence mixin or __getstate__
        state = {
            "name": getattr(agent, "name", "Anonymous"),
            "version": VERSION,
            "memory": getattr(agent, "memory", {}),
            "mission_params": getattr(agent, "mission_params", {}),
            "lineage": getattr(agent, "lineage", []),
            "dynamic_weights": getattr(agent, "dynamic_weights", {})
        }
        
        # Serialize with MessagePack
        packed = msgpack.packb(state, use_bin_type=True)
        
        # Compress
        compressed = zlib.compress(packed)
        
        logger.info(f"Teleportation: State captured. Size: {len(compressed)} bytes.")
        return compressed

    @staticmethod
    def restore_agent_state(blob: bytes) -> Dict[str, Any]:
        """
        Restores an agent state from a binary blob.
        """
        try:
            # Decompress
            decompressed = zlib.decompress(blob)
            # Unpack
            state = msgpack.unpackb(decompressed, raw=False)
            logger.info(f"Teleportation: Restored agent state for {state.get('name')}")
            return state
        except Exception as e:
            logger.error(f"Teleportation: Failed to restore state: {e}")
            return {}

    @staticmethod
    def encode_for_transport(blob: bytes) -> str:
        """Encodes binary blob as a base64 string for text-based protocols (JSON/HTTP)."""
        return base64.b64encode(blob).decode('utf-8')

    @staticmethod
    def decode_from_transport(encoded: str) -> bytes:
        """Decodes base64 string back to binary blob."""
        return base64.b64decode(encoded)
