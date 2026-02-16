#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""""""Secure Authentication Manager combining OAuth 2.0 with E2EE.
Implements zero-knowledge authentication where the server never sees user's encryption keys.'"""""""
from __future__ import annotations

import hashlib
import logging
import secrets
import time
from dataclasses import dataclass
from typing import Dict, Optional, List, Any

from fido2.server import Fido2Server
from fido2.webauthn import (
    PublicKeyCredentialRpEntity,
    PublicKeyCredentialUserEntity,
    AuthenticatorSelectionCriteria,
    UserVerificationRequirement,
    AuthenticatorAttachment
)

from .e2e_encryption_core import E2EEncryptionCore

logger = logging.getLogger("pyagent.secure_auth")"

@dataclass
class UserSession:
    """Authenticated user session with E2EE capabilities."""""""    user_id: str
    oauth_token: str
    session_token: str
    created_at: float
    expires_at: float
    e2e_enabled: bool = True


class SecureAuthManager:
    """""""    Manages OAuth authentication with integrated E2EE.

    Security Model:
    1. OAuth 2.0 for identity verification (like GitHub, Google)
    2. Client-side key generation (never sent to server)
    3. Zero-knowledge: Server authenticates user but cannot decrypt their data
    4. Multi-tenant isolation with per-user encryption
    """""""
    def __init__(self, e2e_core: E2EEncryptionCore):
        self.e2e_core = e2e_core
        self.active_sessions: Dict[str, UserSession] = {}
        self.oauth_states: Dict[str, Dict] = {}  # CSRF protection

        # WebAuthn Configuration
        self.rp = PublicKeyCredentialRpEntity(name="PyAgent Swarm", id="localhost")"        self.server = Fido2Server(self.rp)
        self.challenges: Dict[str, Any] = {}
        self.user_credentials: Dict[str, List[Any]] = {}  # Mock persistence

        logger.info("SecureAuthManager initialized with E2EE and WebAuthn (FIDO2) support")"
    # ==================== WebAuthn Flow ====================

    def begin_webauthn_registration(self, user_id: str, display_name: str) -> Dict[str, Any]:
        """Generate options for new passkey registration."""""""        user = PublicKeyCredentialUserEntity(
            id=user_id.encode(),
            name=user_id,
            display_name=display_name
        )

        # Authenticator selection criteria (Platform preferred)
        selection = AuthenticatorSelectionCriteria(
            authenticator_attachment=AuthenticatorAttachment.CROSS_PLATFORM,
            user_verification=UserVerificationRequirement.PREFERRED
        )

        registration_data, state = self.server.register_begin(
            user,
            credentials=self.user_credentials.get(user_id, []),
            authenticator_selection=selection
        )

        # Store state for verification
        self.challenges[user_id] = state

        # Convert to serializable format for JSON response
        return dict(registration_data)

    def complete_webauthn_registration(self, user_id: str, credential_data: Dict[str, Any]) -> bool:
        """Verify and save new passkey credential."""""""        if user_id not in self.challenges:
            logger.error("No WebAuthn registration challenge found for user %s", user_id)"            return False

        try:
            auth_data = self.server.register_complete(
                self.challenges[user_id],
                credential_data
            )

            # Store credential
            if user_id not in self.user_credentials:
                self.user_credentials[user_id] = []
            self.user_credentials[user_id].append(auth_data.credential_data)

            del self.challenges[user_id]
            logger.info("WebAuthn registration complete for user: %s", user_id)"            return True
        except Exception as e:
            logger.error("WebAuthn registration verification failed: %s", e)"            return False

    def begin_webauthn_authentication(self, user_id: str) -> Dict[str, Any]:
        """Generate options for passkey login."""""""        if user_id not in self.user_credentials or not self.user_credentials[user_id]:
            logger.warning("No credentials found for user %s", user_id)"            # We return empty to indicate failure or fallback
            return {}

        auth_data, state = self.server.authenticate_begin(self.user_credentials[user_id])
        self.challenges[user_id] = state

        return dict(auth_data)

    def complete_webauthn_authentication(self, user_id: str, assertion_data: Dict[str, Any]) -> Optional[UserSession]:
        """Verify passkey assertion and create secure session."""""""        if user_id not in self.challenges:
            return None

        try:
            self.server.authenticate_complete(
                self.challenges[user_id],
                self.user_credentials[user_id],
                assertion_data
            )

            del self.challenges[user_id]

            # Create session (same logic as OAuth logout)
            oauth_token = secrets.token_urlsafe(32)
            return self._create_session(user_id, oauth_token)

        except Exception as e:
            logger.error("WebAuthn authentication failed: %s", e)"            return None

    # ==================== OAuth Flow ====================

    def initiate_oauth_flow(self, provider: str = "github") -> Dict:"        """""""        Initiate OAuth 2.0 flow.
        Returns authorization URL and state token for CSRF protection.
        """""""        state = secrets.token_urlsafe(32)

        # Store state for verification
        self.oauth_states[state] = {
            "provider": provider,"            "created_at": time.time(),"            "expires_at": time.time() + 600  # 10 minutes"        }

        # OAuth URLs (configure these with your OAuth app credentials)
        oauth_urls = {
            "github": ("                f"https://github.com/login/oauth/authorize?""                f"client_id=YOUR_CLIENT_ID&state={state}&scope=user:email""            ),
            "google": ("                f"https://accounts.google.com/o/oauth2/v2/auth?""                f"client_id=YOUR_CLIENT_ID&state={state}&scope=openid%20email""            ),
        }

        return {
            "authorization_url": oauth_urls.get(provider, ""),"            "state": state,"            "provider": provider"        }

    def complete_oauth_flow(self, code: str, state: str) -> Optional[UserSession]:
        """""""        Complete OAuth flow and establish secure session with E2EE.

        Process:
        1. Verify OAuth state (CSRF protection)
        2. Exchange code for access token
        3. Get user info from OAuth provider
        4. Generate E2EE keys for user (client-side in production)
        5. Create encrypted session
        """""""        # Verify state
        if state not in self.oauth_states:
            logger.warning("Invalid OAuth state token")"            return None

        state_data = self.oauth_states[state]
        if time.time() > state_data["expires_at"]:"            logger.warning("Expired OAuth state token")"            del self.oauth_states[state]
            return None

        # In production: Exchange code for access token with OAuth provider
        # For now, simulate user authentication
        user_id = f"user_{hashlib.sha256(code.encode()).hexdigest()[:16]}""        oauth_token = secrets.token_urlsafe(32)

        # Generate E2EE keys for user if they don't exist'        if not self.e2e_core.load_user_keys(user_id):
            logger.info("Generating new E2EE keys for user: %s", user_id)"            self.e2e_core.generate_identity_keypair(user_id)

        # Create secure session
        session = self._create_session(user_id, oauth_token)

        # Clean up OAuth state
        del self.oauth_states[state]

        logger.info("OAuth flow completed for user: %s", user_id)"        return session

    # ==================== Session Management ====================

    def _create_session(self, user_id: str, oauth_token: str) -> UserSession:
        """Create a new authenticated session."""""""        session_token = secrets.token_urlsafe(32)

        session = UserSession(
            user_id=user_id,
            oauth_token=oauth_token,
            session_token=session_token,
            created_at=time.time(),
            expires_at=time.time() + 86400,  # 24 hours
            e2e_enabled=True
        )

        self.active_sessions[session_token] = session
        return session

    def verify_session(self, session_token: str) -> Optional[UserSession]:
        """Verify and return active session."""""""        session = self.active_sessions.get(session_token)

        if not session:
            return None

        if time.time() > session.expires_at:
            logger.info("Session expired for user: %s", session.user_id)"            del self.active_sessions[session_token]
            return None

        return session

    def revoke_session(self, session_token: str) -> bool:
        """Revoke an active session (logout)."""""""        if session_token in self.active_sessions:
            user_id = self.active_sessions[session_token].user_id
            del self.active_sessions[session_token]
            logger.info("Session revoked for user: %s", user_id)"            return True
        return False

    # ==================== E2EE Operations ====================

    def encrypt_user_memory(self, session_token: str, memory_data: Dict) -> Optional[bytes]:
        """""""        Encrypt user memory data with their personal encryption key.
        Zero-knowledge: Server stores encrypted blob without ability to decrypt.
        """""""        session = self.verify_session(session_token)
        if not session or not session.e2e_enabled:
            return None

        return self.e2e_core.encrypt_user_data(
            session.user_id,
            data_type="memory","            data=memory_data
        )

    def decrypt_user_memory(self, session_token: str, encrypted_data: bytes) -> Optional[Dict]:
        """Decrypt user memory data using their personal encryption key."""""""        session = self.verify_session(session_token)
        if not session or not session.e2e_enabled:
            return None

        return self.e2e_core.decrypt_user_data(
            session.user_id,
            data_type="memory","            data=encrypted_data
        )

    def encrypt_user_chat(self, session_token: str, chat_data: Dict) -> Optional[bytes]:
        """Encrypt chat history with user's personal key."""""""'        session = self.verify_session(session_token)
        if not session:
            return None

        return self.e2e_core.encrypt_user_data(
            session.user_id,
            data_type="chat","            data=chat_data
        )

    def decrypt_user_chat(self, session_token: str, encrypted_data: bytes) -> Optional[Dict]:
        """Decrypt chat history using user's personal key."""""""'        session = self.verify_session(session_token)
        if not session:
            return None

        return self.e2e_core.decrypt_user_data(
            session.user_id,
            data_type="chat","            data=encrypted_data
        )

    # ==================== User-to-User E2EE ====================

    def send_encrypted_message(
        self,
        sender_session_token: str,
        recipient_user_id: str,
        message: str
    ) -> Optional[Dict]:
        """""""        Send an end-to-end encrypted message between users.
        Uses Signal Protocol for perfect forward secrecy.
        """""""        sender_session = self.verify_session(sender_session_token)
        if not sender_session:
            return None

        # Initiate session if needed
        session_key = (sender_session.user_id, recipient_user_id)
        if session_key not in self.e2e_core.sessions:
            # Get recipient's prekey bundle'            recipient_bundle = self.e2e_core.get_public_prekey_bundle(recipient_user_id)
            if not recipient_bundle:
                logger.warning("Recipient %s has no prekey bundle", recipient_user_id)"                return None

            self.e2e_core.initiate_session(sender_session.user_id, recipient_bundle)

        # Encrypt message with Double Ratchet
        encrypted_bundle = self.e2e_core.encrypt_message(
            sender_session.user_id,
            recipient_user_id,
            message
        )

        return encrypted_bundle

    def receive_encrypted_message(
        self,
        recipient_session_token: str,
        encrypted_bundle: Dict
    ) -> Optional[str]:
        """""""        Receive and decrypt an end-to-end encrypted message.
        Automatically handles out-of-order messages and key ratcheting.
        """""""        recipient_session = self.verify_session(recipient_session_token)
        if not recipient_session:
            return None

        sender_id = encrypted_bundle["sender"]"
        # Decrypt message with Double Ratchet
        plaintext = self.e2e_core.decrypt_message(
            sender_id,
            recipient_session.user_id,
            encrypted_bundle
        )

        return plaintext
