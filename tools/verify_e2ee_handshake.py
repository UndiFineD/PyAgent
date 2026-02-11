#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors

import asyncio
import logging
from unittest.mock import MagicMock
from src.infrastructure.swarm.fleet.fleet_manager import FleetManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("HandshakeVerify")

async def verify_handshake():
    """
    Simulates a peer-to-peer secure handshake between two FleetManagers.
    Tests Phase 320 (Double Ratchet E2EE integration).
    """
    logger.info("Starting E2EE Handshake Verification...")

    # Node A Setup
    node_a = FleetManager(workspace_root="node_a_ws")
    node_a.transport = MagicMock()
    
    # Node B Setup
    node_b = FleetManager(workspace_root="node_b_ws")
    node_b.transport = MagicMock()

    # Get their resolved node IDs (usually based on workspace name or generated)
    # Based on the code: self.backup_node = DistributedBackup(node_id=f"node-{self.workspace_root.name}")
    # We can just manually set a .node_id property if needed or check what it is.
    node_a.node_id = "node_a"
    node_b.node_id = "node_b"

    # Capture Node A's HANDSHAKE_INIT message
    async def side_effect_a(target, msg):
        if msg["type"] == "HANDSHAKE_INIT":
            logger.info(f"Node A -> Node B: HANDSHAKE_INIT (Identity: {msg['identity_key'][:10]}...)")
            # Simulate Node B receiving and responding
            response = await node_b.handle_message(msg)
            return response
        return {"status": "ignored"}

    node_a.transport.send_message.side_effect = side_effect_a

    # Simulate Peer Discovery: Node A finds Node B
    await node_a._on_voyager_peer_added("node_b")

    # Verify sessions exist in both
    session_a = node_a.encryption_core.sessions.get(("node_a", "node_b"))
    session_b = node_b.encryption_core.sessions.get(("node_a", "node_b"))

    if session_a and session_b:
        logger.info("SUCCESS: Secure session established on both nodes.")
        
        # Test encrypted message exchange
        plaintext = "TOP_SECRET_SWARM_KEY"
        encrypted = node_a.encryption_core.encrypt_message("node_a", "node_b", plaintext)
        
        decrypted = node_b.encryption_core.decrypt_message("node_a", "node_b", encrypted)
        if decrypted == plaintext:
            logger.info(f"SUCCESS: Secure messaging verified: '{decrypted}'")
        else:
            logger.error(f"FAILURE: Decryption failed. Expected '{plaintext}', got '{decrypted}'")
    else:
        logger.error(f"FAILURE: Session mapping missing. A: {bool(session_a)}, B: {bool(session_b)}")

if __name__ == "__main__":
    asyncio.run(verify_handshake())
