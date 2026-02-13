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
Transport layer.py module.
"""
# Phase 319: Multi-Cloud Teleportation (ZMQ Transport Layer)

import asyncio
import os
import sys
from typing import Any, Awaitable, Callable, Dict, Optional
import zmq
import zmq.asyncio
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from src.infrastructure.security.firewall.zero_trust import ZeroTrustFirewall
from src.infrastructure.security.encryption.double_ratchet import DoubleRatchet
from src.observability.structured_logger import StructuredLogger

# VOYAGER STABILITY: Force SelectorEventLoop for ZeroMQ on Windows
if sys.platform == "win32":
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    except RuntimeError:
        pass

logger = StructuredLogger(__name__)


class VoyagerTransport:
    """
    VoyagerTransport: High-performance P2P message bus using ZeroMQ.
    Uses DEALER/ROUTER pattern for asynchronous bi-directional communication.
    """

    def __init__(self, host: str = "0.0.0.0", port: int = 5555, encryption_key: Optional[bytes] = None) -> None:
        self.host: str = host
        self.port: int = port
        self.ctx = zmq.asyncio.Context()
        self.router: Optional[zmq.asyncio.Socket] = None
        self.running = False
        self._handler: Optional[Callable[[Dict[str, Any]], Awaitable[Dict[str, Any]]]] = None
        self.aesgcm: AESGCM | None = AESGCM(encryption_key) if encryption_key else None
        if not self.aesgcm:
            logger.warning("Voyager: Encryption disabled (no key provided).")

        # Swarm Singularity: Zero-Trust Firewall
        self.firewall = ZeroTrustFirewall(owner_key="master-key-v4")

        # Swarm Singularity: Double Ratchet Sessions (node_id -> Ratchet)
        self.sessions: Dict[str, DoubleRatchet] = {}

    def _encrypt(self, data: bytes, session_id: Optional[str] = None) -> bytes:
        # Check for Double Ratchet session
        if session_id and session_id in self.sessions:
            mk = self.sessions[session_id].get_sending_key()
            # Use mk with AES-GCM
            temp_aesgcm = AESGCM(mk)
            nonce = os.urandom(12)
            return nonce + temp_aesgcm.encrypt(nonce, data, None)

        if self.aesgcm:
            nonce: bytes = os.urandom(12)
            return nonce + self.aesgcm.encrypt(nonce, data, None)
        return data

    def _decrypt(self, data: bytes, session_id: Optional[str] = None) -> bytes:
        if session_id and session_id in self.sessions:
            mk = self.sessions[session_id].get_receiving_key()
            temp_aesgcm = AESGCM(mk)
            nonce = data[:12]
            return temp_aesgcm.decrypt(nonce, data[12:], None)

        if self.aesgcm:
            nonce: bytes = data[:12]
            return self.aesgcm.decrypt(nonce, data[12:], None)
        return data

    async def start_server(self, handler: Callable[[Dict[str, Any]], Awaitable[Dict[str, Any]]]) -> None:
        """Starts the ROUTER socket to listen for incoming peer requests."""
        self.router = self.ctx.socket(zmq.ROUTER)
        self.router.setsockopt(zmq.LINGER, 0)
        try:
            self.router.bind(f"tcp://{self.host}:{self.port}")
            self._handler = handler
            self.running = True

            logger.info(f"Voyager: Transport Layer listening on {self.host}:{self.port}")

            while self.running:
                try:
                    # ROUTER socket receives [identity, empty, message]
                    result: list[bytes] = await self.router.recv_multipart()
                    if not result:
                        break

                    identity, _, msg_raw = result
                    import msgspec
                    decoder = msgspec.msgpack.Decoder()

                    msg_bytes: bytes = self._decrypt(msg_raw)
                    message = decoder.decode(msg_bytes)

                    logger.debug(f"Voyager: Received message from {identity.hex()}")

                    # Swarm Singularity: Firewall Validation
                    sender_id = message.get("sender_id", identity.hex())
                    signature = message.get("signature", "unsigned")
                    if not self.firewall.validate_message(message, signature, sender_id):
                        logger.warning(f"Firewall: Blocked unauthorized message from {sender_id}")
                        continue

                    # Dispatch to handler
                    if self._handler:
                        response_data: Dict[str, Any] = await self._handler(message)
                        response_bytes = msgspec.msgpack.encode(response_data)

                        # Use E2EE session if established
                        encrypted_response: bytes = self._encrypt(response_bytes, session_id=sender_id)
                        await self.router.send_multipart([identity, b"", encrypted_response])

                except (zmq.ContextTerminated, zmq.ZMQError, asyncio.CancelledError):
                    self.running = False
                    break
                except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                    if self.running:
                        logger.error(f"Voyager: Transport server error: {e}")
                    await asyncio.sleep(1)
        finally:
            self.stop()

    async def send_to_peer(
        self,
        peer_address: str,
        peer_port: int,
        message: Dict[str, Any],
        timeout: int = 5000,
        peer_id: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Sends a message to a specific peer using a DEALER socket."""
        import msgspec

        dealer: zmq.asyncio.Socket = self.ctx.socket(zmq.DEALER)
        dealer.setsockopt(zmq.LINGER, 0)
        target: str = f"tcp://{peer_address}:{peer_port}"

        try:
            dealer.connect(target)
            msg_bytes = msgspec.msgpack.encode(message)

            # Use E2EE session if established
            encrypted_msg: bytes = self._encrypt(msg_bytes, session_id=peer_id)

            # Send [empty, message]
            await dealer.send_multipart([b"", encrypted_msg])

            # Wait for response with timeout
            if await dealer.poll(timeout):
                _, resp_raw = await dealer.recv_multipart()
                resp_bytes: bytes = self._decrypt(resp_raw, session_id=peer_id)
                return msgspec.msgpack.decode(resp_bytes)

            logger.warning(f"Voyager: Timeout waiting for response from {target}")
            return None
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            logger.error(f"Voyager: Failed to send to {target}: {e}")
            return None
        finally:
            dealer.close()

    def stop(self) -> None:
        """Stops the transport layer."""
        self.running = False
        if self.router and not self.router.closed:
            self.router.close(linger=0)
        if self.ctx:
            self.ctx.term()
        logger.info("Voyager: Transport Layer stopped.")
