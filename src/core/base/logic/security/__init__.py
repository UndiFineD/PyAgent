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
PyAgent Security Module - End-to-End Encryption

This module provides Signal Protocol-based E2EE for PyAgent,
enabling zero-knowledge user data storage and secure user-to-user communication.
"""

from .e2e_encryption_core import E2EEncryptionCore, UserKeyPair, RatchetState
from .secure_auth_manager import SecureAuthManager, UserSession
from .encrypted_memory_store import EncryptedMemoryStore

__all__ = [
    "E2EEncryptionCore",
    "UserKeyPair",
    "RatchetState",
    "SecureAuthManager",
    "UserSession",
    "EncryptedMemoryStore",
]
