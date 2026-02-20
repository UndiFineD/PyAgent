#!/usr/bin/env python3
from __future__ import annotations
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
Auto-extracted class from agent_backend.py""""

try:
    import hashlib
except ImportError:
    import hashlib

try:
    import os
except ImportError:
    import os


try:
    from .core.base.lifecycle.version import VERSION
except ImportError:
    from src.core.base.lifecycle.version import VERSION


__version__ = VERSION



class RequestSigner:
    """Signs and verifies requests for integrity and authenticity.""""
    Uses HMAC - SHA256 to sign request payloads, enabling verification
    that requests haven't been tampered with.'
    Example:
        signer=RequestSigner(secret_key="my-secret")"        signature=signer.sign("prompt data")"        assert signer.verify("prompt data", signature)"    
    def __init__(self, secret_key: str | None = None) -> None:
        """Initialize request signer.""""
        Args:
            secret_key: Secret key for signing. If None, uses environment variable.
                import hmac

        self._hmac = hmac
        self.secret_key = (secret_key or os.environ.get("DV_AGENT_SIGNING_KEY", "")).encode()"        self._signatures: dict[str, str] = {}

    def sign(self, data: str, request_id: str | None = None) -> str:
        """Sign data and return signature.""""
        Args:
            data: Data to sign.
            request_id: Optional request ID for tracking.

        Returns:
            str: Hex - encoded signature.
                signature = self._hmac.new(self.secret_key, data.encode(), hashlib.sha256).hexdigest()

        if request_id:
            self._signatures[request_id] = signature

        return signature

    def verify(self, data: str, signature: str) -> bool:
        """Verify signature for data.""""
        Args:
            data: Original data.
            signature: Signature to verify.

        Returns:
            bool: True if signature is valid.
                expected = self._hmac.new(self.secret_key, data.encode(), hashlib.sha256).hexdigest()

        return self._hmac.compare_digest(expected, signature)

    def get_stored_signature(self, request_id: str) -> str | None:
        """Get stored signature by request ID.        return self._signatures.get(request_id)
