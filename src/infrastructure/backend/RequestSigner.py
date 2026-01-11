#!/usr/bin/env python3

"""Auto-extracted class from agent_backend.py"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from queue import PriorityQueue
from typing import Any, Callable, Dict, List, Optional, Tuple
import hashlib
import json
import logging
import os
import re
import subprocess
import threading
import time
import uuid

class RequestSigner:
    """Signs and verifies requests for integrity and authenticity.

    Uses HMAC - SHA256 to sign request payloads, enabling verification
    that requests haven't been tampered with.

    Example:
        signer=RequestSigner(secret_key="my-secret")
        signature=signer.sign("prompt data")
        assert signer.verify("prompt data", signature)
    """

    def __init__(self, secret_key: Optional[str] = None) -> None:
        """Initialize request signer.

        Args:
            secret_key: Secret key for signing. If None, uses environment variable.
        """
        import hmac
        self._hmac = hmac
        self.secret_key = (secret_key or os.environ.get("DV_AGENT_SIGNING_KEY", "")).encode()
        self._signatures: Dict[str, str] = {}

    def sign(self, data: str, request_id: Optional[str] = None) -> str:
        """Sign data and return signature.

        Args:
            data: Data to sign.
            request_id: Optional request ID for tracking.

        Returns:
            str: Hex - encoded signature.
        """
        signature = self._hmac.new(
            self.secret_key,
            data.encode(),
            hashlib.sha256
        ).hexdigest()

        if request_id:
            self._signatures[request_id] = signature

        return signature

    def verify(self, data: str, signature: str) -> bool:
        """Verify signature for data.

        Args:
            data: Original data.
            signature: Signature to verify.

        Returns:
            bool: True if signature is valid.
        """
        expected = self._hmac.new(
            self.secret_key,
            data.encode(),
            hashlib.sha256
        ).hexdigest()

        return self._hmac.compare_digest(expected, signature)

    def get_stored_signature(self, request_id: str) -> Optional[str]:
        """Get stored signature by request ID."""
        return self._signatures.get(request_id)
