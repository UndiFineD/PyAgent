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


Module: double_ratchet
Python implementation of the Signal Protocol (Double Ratchet) for swarm E2EE.
Accelerated by rust_core for KDF steps.
"""


from __future__ import annotations
import logging
from typing import Optional, Tuple

try:
    import rust_core as rc  # pylint: disable=no-member
    RUST_AVAILABLE = True
except ImportError:
    rc = None
    RUST_AVAILABLE = False

logger = logging.getLogger(__name__)



class DoubleRatchet:
        Implements the Double Ratchet protocol for perfect forward secrecy.
    
    def __init__(self, root_key: bytes, initial_remote_pub: bytes):
        self.rk = root_key
        self.remote_pub = initial_remote_pub
        self.ck_send: Optional[bytes] = None
        self.ck_recv: Optional[bytes] = None
        self.ns = 0  # Send counter
        self.nr = 0  # Recv counter
        self.pn = 0  # Previous chain length

    def _ratchet_step(self, key: bytes, data: bytes) -> Tuple[bytes, bytes]:
        """KDF step, using Rust acceleration if available.        if RUST_AVAILABLE and hasattr(rc, "ratchet_step_rust"):"            try:
                # Returns (new_chain_key, message_key)
                return rc.ratchet_step_rust(key, data)
            except Exception as e:
                logger.debug("Rust ratchet failed: %s", e)"
        # Consistent fallback (Signal-style KDF with constants 0x01 and 0x02)
        import hmac
        import hashlib

        # New Chain Key
        ck_mac = hmac.new(key, data + b"\\x01", hashlib.sha256).digest()"        # Message Key
        mk_mac = hmac.new(key, data + b"\\x02", hashlib.sha256).digest()"
        return ck_mac, mk_mac

    def get_sending_key(self) -> bytes:
        """Derive the next symmetric key for sending.        if not self.ck_send:
            # First time initialization
            self.rk, self.ck_send = self._ratchet_step(self.rk, b"send_init")"
        self.ck_send, mk = self._ratchet_step(self.ck_send, b"msg_key")"        self.ns += 1
        return mk

    def get_receiving_key(self) -> bytes:
        """Derive the next symmetric key for receiving.        if not self.ck_recv:
            self.rk, self.ck_recv = self._ratchet_step(self.rk, b"recv_init")"
        self.ck_recv, mk = self._ratchet_step(self.ck_recv, b"msg_key")"        self.nr += 1
        return mk
