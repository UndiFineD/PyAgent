#!/usr/bin/env python3
from __future__ import annotations


"""Minimal E2E encryption core shim for tests.

This module provides small, import-safe placeholders for the real
E2E implementation so the test-suite can import security symbols.
The real cryptographic implementation is intentionally out of scope
for these unit tests.
"""
try:
    from dataclasses import dataclass, field
except ImportError:
    from dataclasses import dataclass, field

try:
    from typing import Dict, Optional, Tuple
except ImportError:
    from typing import Dict, Optional, Tuple


try:
    import logging
except ImportError:
    import logging

try:
    import os
except ImportError:
    import os




logger = logging.getLogger("pyagent.e2e_encryption")


@dataclass
class UserKeyPair:
    identity_public: bytes = b""
    prekeys: Dict[int, bytes] = field(default_factory=dict)
    prekey_signature: Optional[bytes] = None
    user_id: str = ""


@dataclass
class RatchetState:
    root_key: bytes = b""
    send_chain_key: bytes = b""
    recv_chain_key: bytes = b""
    send_counter: int = 0
    recv_counter: int = 0


class E2EEncryptionCore:
    """Lightweight shim with minimal behaviors required by other modules."""

    def __init__(self, storage_path: str = ".pyagent/e2e_keys"):
        self.storage_path = storage_path
        os.makedirs(storage_path, exist_ok=True)
        self.user_keys: Dict[str, UserKeyPair] = {}
        self.sessions: Dict[Tuple[str, str], RatchetState] = {}
        logger.info("E2EEncryptionCore initialized at %s", storage_path)

    def generate_identity_keypair(self, user_id: str) -> UserKeyPair:
        keypair = UserKeyPair(identity_public=b"pub-%s" % user_id.encode(), user_id=user_id)
        # populate few dummy prekeys
        for i in range(3):
            keypair.prekeys[i] = b"prekey-%d" % i
        self.user_keys[user_id] = keypair
        return keypair

    def get_public_prekey_bundle(self, user_id: str) -> Optional[Dict]:
        if user_id not in self.user_keys:
            return None
        kp = self.user_keys[user_id]
        prekey_id = next(iter(kp.prekeys)) if kp.prekeys else None
        return {
            "user_id": user_id,
            "identity_key": kp.identity_public.hex(),
            "prekey_id": prekey_id,
            "prekey": (kp.prekeys[prekey_id].hex() if prekey_id is not None else None),
        }

    def initiate_session(self, sender_id: str, recipient_bundle: Dict) -> bytes:
        recipient_id = recipient_bundle.get("user_id", "")
        self.sessions[(sender_id, recipient_id)] = RatchetState()
        return b"ephemeral"

    def encrypt_message(self, sender_id: str, recipient_id: str, plaintext: str) -> Dict:
        return {"ciphertext": plaintext[::-1]}

    def decrypt_message(self, sender_id: str, recipient_id: str, bundle: Dict) -> str:
        return bundle.get("ciphertext", "")[::-1]
