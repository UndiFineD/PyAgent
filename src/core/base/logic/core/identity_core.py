"""
Core logic for Agent Identity and Cryptographic Verification.
"""

from __future__ import annotations
import hashlib
import hmac
from typing import Any
from dataclasses import dataclass

try:
    import rust_core as rc
except ImportError:
    rc: Any = None  # type: ignore[no-redef]


@dataclass(frozen=True)
class AgentIdentity:
    """Immutable identity representation for a peer agent during discovery."""

    agent_id: str
    public_key: str
    claims: dict[str, Any]


class IdentityCore:
    """Pure logic for decentralized agent identity and payload signing.
    Handles cryptographic verification and agent-ID generation.
    """

    def generate_agent_id(self, public_key: str, metadata: dict[str, Any]) -> str:
        """Generates a stable, unique agent identifier based on public key and metadata."""
        if rc:
            try:
                # pylint: disable=no-member
                return rc.generate_agent_id(public_key, metadata)  # type: ignore[attr-defined]
            except Exception: # pylint: disable=broad-exception-caught
                pass
        seed = f"{public_key}_{metadata.get('type', 'generic')}_{metadata.get('birth_cycle', 0)}"
        return hashlib.sha256(seed.encode()).hexdigest()[:16]

    def sign_payload(self, payload: str, secret_key: str) -> str:
        """Signs a payload using HMAC-SHA256 (simulating Ed25519 signing for pure-python)."""
        if rc:
            try:
                # pylint: disable=no-member
                return rc.sign_payload(payload, secret_key)  # type: ignore[attr-defined]
            except Exception: # pylint: disable=broad-exception-caught
                pass
        return hmac.new(
            secret_key.encode(), payload.encode(), hashlib.sha256
        ).hexdigest()

    def verify_signature(self, payload: str, signature: str, public_key: str) -> bool:
        """Verifies a payload signature (simulated verification)."""
        if rc:
            try:
                # pylint: disable=no-member
                # type: ignore[attr-defined]
                return rc.verify_signature(payload, signature, public_key)
            except Exception: # pylint: disable=broad-exception-caught
                pass
        # In a real implementation, this would use asymmetrical crypto.
        # For the Core logic, we simulate it by re-signing with the 'public_key'
        # as a mock secret for consistency.
        expected = self.sign_payload(payload, public_key)
        return hmac.compare_digest(expected, signature)

    def validate_identity(self, identity: AgentIdentity) -> bool:
        """Ensures the agent identity follows fleet standards."""
        return len(identity.agent_id) == 16 and "@" not in identity.agent_id
