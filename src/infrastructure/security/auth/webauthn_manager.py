#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
WebAuthn (FIDO2) Authentication Manager for PyAgent.
Handles registration and authentication ceremonies for biometric hardware keys.
"""

import logging
import base64
import os
import json
from typing import Dict, Any
from authlib.integrations.starlette_client import OAuth

try:
    from webauthn import (
        generate_registration_options,
        verify_registration_response,
        generate_authentication_options,
        verify_authentication_response,
        options_to_json,
        base64url_to_bytes
    )
    from webauthn.helpers.structs import (
        AttestationConveyancePreference,
        AuthenticatorAttachment,
        AuthenticatorSelectionCriteria,
        PublicKeyCredentialRpEntity,
        PublicKeyCredentialUserEntity,
        UserVerificationRequirement,
    )
    HAS_WEBAUTHN = True
except ImportError:
    HAS_WEBAUTHN = False

logger = logging.getLogger(__name__)

class WebAuthnManager:
    """Manages WebAuthn registration and authentication logic."""

    def __init__(self, rp_id: str = "localhost", rp_name: str = "PyAgent"):
        self.rp_id = rp_id
        self.rp_name = rp_name
        self.users: Dict[str, Dict[str, Any]] = {}  # Mock DB: username -> credential data
        self.challenges: Dict[str, str] = {}         # username -> challenge
        
        # Phase 327: OAuth Integration
        self.oauth = OAuth()
        self.oauth.register(
            name='github',
            client_id=os.getenv('GITHUB_CLIENT_ID', 'STUB'),
            client_secret=os.getenv('GITHUB_CLIENT_SECRET', 'STUB'),
            access_token_url='https://github.com/login/oauth/access_token',
            access_token_params=None,
            authorize_url='https://github.com/login/oauth/authorize',
            authorize_params=None,
            api_base_url='https://api.github.com/',
            client_kwargs={'scope': 'user:email'},
        )

    def get_registration_options(self, username: str) -> Dict[str, Any]:
        """Generates options for a new WebAuthn registration."""
        if not HAS_WEBAUTHN:
            logger.warning("webauthn library not installed. Returning mock options.")
            return {"mock": True, "challenge": base64.b64encode(os.urandom(32)).decode()}

        user_id = os.urandom(16)
        options = generate_registration_options(
            rp_id=self.rp_id,
            rp_name=self.rp_name,
            user_id=user_id,
            user_name=username,
            attestation=AttestationConveyancePreference.DIRECT,
            authenticator_selection=AuthenticatorSelectionCriteria(
                authenticator_attachment=AuthenticatorAttachment.PLATFORM,
                user_verification=UserVerificationRequirement.PREFERRED,
            ),
        )
        
        # Store challenge for verification
        self.challenges[username] = options.challenge
        return json.loads(options_to_json(options))

    def verify_registration(self, username: str, response: Dict[str, Any]) -> bool:
        """Verifies a WebAuthn registration response."""
        if not HAS_WEBAUTHN:
            logger.warning("webauthn library not installed. Mocking success.")
            return True 

        challenge = self.challenges.get(username)
        if not challenge:
            logger.error(f"No registration challenge found for user: {username}")
            return False

        try:
            verification = verify_registration_response(
                credential=response,
                expected_challenge=base64url_to_bytes(challenge),
                expected_rp_id=self.rp_id,
                expected_origin=f"http://{self.rp_id}:8000", # Mock origin for lab
            )
            
            # Store public key and credential ID
            self.users[username] = {
                "credential_id": verification.credential_id,
                "public_key": verification.public_key,
                "sign_count": verification.sign_count,
            }
            
            logger.info(f"WebAuthn: Successfully registered biometric key for {username}")
            return True
        except Exception as e:
            logger.error(f"WebAuthn: Registration verification failed: {e}")
            return False

    def get_authentication_options(self, username: str) -> Dict[str, Any]:
        """Generates options for a WebAuthn authentication ceremony."""
        if not HAS_WEBAUTHN:
             return {"mock": True, "challenge": "mock_challenge"}

        user_data = self.users.get(username)
        if not user_data:
            raise ValueError(f"User not found: {username}")

        options = generate_authentication_options(
            rp_id=self.rp_id,
            challenge=os.urandom(32),
            allow_credentials=[{
                "id": user_data["credential_id"],
                "type": "public-key"
            }],
            user_verification=UserVerificationRequirement.PREFERRED,
        )
        
        self.challenges[username] = options.challenge
        return json.loads(options_to_json(options))

    def verify_authentication(self, username: str, response: Dict[str, Any]) -> bool:
        """Verifies a WebAuthn authentication response."""
        if not HAS_WEBAUTHN:
            return True

        challenge = self.challenges.get(username)
        user_data = self.users.get(username)
        
        if not challenge or not user_data:
            return False

        try:
            verification = verify_authentication_response(
                credential=response,
                expected_challenge=base64url_to_bytes(challenge),
                expected_rp_id=self.rp_id,
                expected_origin=f"http://{self.rp_id}:8000",
                credential_public_key=user_data["public_key"],
                credential_current_sign_count=user_data["sign_count"],
            )
            
            # Update sign count to prevent replay attacks
            self.users[username]["sign_count"] = verification.new_sign_count
            logger.info(f"WebAuthn: Successfully authenticated {username}")
            return True
        except Exception as e:
            logger.error(f"WebAuthn: Authentication failed: {e}")
            return False
