#!/usr/bin/env python3
"""Lightweight secure auth manager shim for tests.

Provides minimal behavior for creating and verifying sessions.
Real WebAuthn / OAuth flows are out of scope for unit tests.
"""
from __future__ import annotations


try:
    import logging
except ImportError:
    import logging

try:
    import secrets
except ImportError:
    import secrets

try:
    import time
except ImportError:
    import time


try:
    from dataclasses import dataclass
except ImportError:
    from dataclasses import dataclass

try:
    from typing import Dict, Optional, Any
except ImportError:
    from typing import Dict, Optional, Any


try:
    from .e2e_encryption_core import E2EEncryptionCore
except ImportError:
    from .e2e_encryption_core import E2EEncryptionCore



logger = logging.getLogger("pyagent.secure_auth")


@dataclass
class UserSession:
    user_id: str
    oauth_token: str
    session_token: str
    created_at: float
    expires_at: float
    e2e_enabled: bool = True


class SecureAuthManager:
    """Minimal manager exposing session creation and verification."""

    def __init__(self, e2e_core: E2EEncryptionCore):
        self.e2e_core = e2e_core
        self.active_sessions: Dict[str, UserSession] = {}
        self.oauth_states: Dict[str, Dict] = {}

    def _create_session(self, user_id: str, oauth_token: str) -> UserSession:
        token = secrets.token_urlsafe(24)
        session = UserSession(
            user_id=user_id,
            oauth_token=oauth_token,
            session_token=token,
            created_at=time.time(),
            expires_at=time.time() + 86400,
            e2e_enabled=True,
        )
        self.active_sessions[token] = session
        return session

    def initiate_oauth_flow(self, provider: str = "github") -> Dict[str, str]:
        state = secrets.token_urlsafe(16)
        self.oauth_states[state] = {"provider": provider, "created_at": time.time()}
        return {"authorization_url": f"https://example/{provider}?state={state}", "state": state}

    def complete_oauth_flow(self, code: str, state: str) -> Optional[UserSession]:
        if state not in self.oauth_states:
            return None
        user_id = f"user_{secrets.token_hex(8)}"
        oauth_token = secrets.token_urlsafe(24)
        session = self._create_session(user_id, oauth_token)
        del self.oauth_states[state]
        return session

    def verify_session(self, session_token: str) -> Optional[UserSession]:
        session = self.active_sessions.get(session_token)
        if not session:
            return None
        if time.time() > session.expires_at:
            del self.active_sessions[session_token]
            return None
        return session

    def revoke_session(self, session_token: str) -> bool:
        if session_token in self.active_sessions:
            del self.active_sessions[session_token]
            return True
        return False
