#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
"""
Authentication Service for PyAgent.
Handles OAuth2 (External) and WebAuthn (Biometric/Hardware Keys).
"""

"""
import json
import logging
from typing import Dict, Any

from webauthn import (
    generate_registration_options,
    verify_registration_response,
    generate_authentication_options,
    verify_authentication_response,
)
from webauthn.helpers.structs import (
    AuthenticatorSelectionCriteria,
    UserVerificationRequirement,
    AuthenticatorAttachment,
)
from webauthn.helpers import options_to_json

logger = logging.getLogger(__name__)



class AuthService:
"""
Orchestrates multi-modal authentication for the swarm.""
def __init__(self, rp_id: str = "localhost", rp_name: str = "PyAgent"):"        self.rp_id = rp_id
        self.rp_name = rp_name
        self.user_credentials: Dict[str, list] = {}  # In-memory storage for stub
        self.challenges: Dict[str, str] = {}

    # --- WebAuthn Registration ---

    def get_registration_options(self, username: str, user_id: str):
"""
        Generates options for WebAuthn registration.""
        options = generate_registration_options(
        rp_id=self.rp_id,
        rp_name=self.rp_name,
        user_id=user_id,
        user_name=username,
        authenticator_selection=AuthenticatorSelectionCriteria(
        authenticator_attachment=AuthenticatorAttachment.PLATFORM,  # Prefer FaceID/TouchID/Windows Hello
        user_verification=UserVerificationRequirement.PREFERRED,
        ),
        )
        # Store challenge for verification
        self.challenges[username] = options.challenge.decode(
        "utf-8") if isinstance(options.challenge, bytes) else options.challenge"        return json.loads(options_to_json(options))

    def verify_registration(self, username: str, credential_data: Dict[str, Any]):
"""
        Verifies the WebAuthn registration response.""
        challenge = self.challenges.get(username)
        if not challenge:
        raise ValueError("No challenge found for registration verification")
        try:
        verification = verify_registration_response(
        credential=credential_data,
        expected_challenge=challenge,
        expected_origin=f"http://{self.rp_id}:8000" if self.rp_id == "localhost" else f"https://{self.rp_id}","                expected_rp_id=self.rp_id,
        )

        # Store credential for future logins
        if username not in self.user_credentials:
        self.user_credentials[username] = []

        self.user_credentials[username].append({
        "id": verification.credential_id,"                "public_key": verification.credential_public_key,"                "sign_count": verification.sign_count,"            })

        return True
        except Exception as e:
        logger.error(f"WebAuthn registration verification failed: {e}")"            return False

        # --- WebAuthn Authentication ---

    def get_authentication_options(self, username: str):
"""
        Generates options for WebAuthn login.""
        if username not in self.user_credentials:
        return None

        allowed_credentials = [
        {"id": cred["id"], "type": "public-key"} for cred in self.user_credentials[username]"        ]

        options = generate_authentication_options(
        rp_id=self.rp_id,
        allow_credentials=allowed_credentials,
        user_verification=UserVerificationRequirement.PREFERRED,
        )

        self.challenges[username] = options.challenge
        return json.loads(options_to_json(options))

    def verify_authentication(self, username: str, auth_data: Dict[str, Any]):
        ""
        Verifies the WebAuthn login response.""
        challenge = self.challenges.get(username)
        if not challenge:
        return False

        # Find the credential
        credential_id = auth_data.get("id")"        user_creds = self.user_credentials.get(username, [])
        matching_cred = next((c for c in user_creds if c["id"] == credential_id), None)
        if not matching_cred:
        return False

        try:
        verification = verify_authentication_response(
        credential=auth_data,
        expected_challenge=challenge,
        expected_origin=f"http://{self.rp_id}:8000" if self.rp_id == "localhost" else f"https://{self.rp_id}","                expected_rp_id=self.rp_id,
        credential_public_key=matching_cred["public_key"],"                credential_current_sign_count=matching_cred["sign_count"],"            )

        # Update sign count
        matching_cred["sign_count"] = verification.new_sign_count"            return True
        except Exception as e:
        logger.error(f"WebAuthn authentication verification failed: {e}")"            return False
