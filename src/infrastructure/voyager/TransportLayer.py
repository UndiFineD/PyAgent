# Copyright 2026 PyAgent Authors
# Phase 319: Multi-Cloud Teleportation (ZMQ Transport Layer)

import zmq
import zmq.asyncio
import asyncio
import logging
from typing import Any, Dict, Optional, Callable, Awaitable
from src.observability.StructuredLogger import StructuredLogger

logger = StructuredLogger(__name__)

class VoyagerTransport:
    """
    VoyagerTransport: High-performance P2P message bus using ZeroMQ.
    Uses DEALER/ROUTER pattern for asynchronous bi-directional communication.
    """
    def __init__(self, host: str = "0.0.0.0", port: int = 5555):
        self.host = host
        self.port = port
        self.ctx = zmq.asyncio.Context()
        self.router: Optional[zmq.asyncio.Socket] = None
        self.running = False
        self._handler: Optional[Callable[[Dict[str, Any]], Awaitable[Dict[str, Any]]]] = None

    async def start_server(self, handler: Callable[[Dict[str, Any]], Awaitable[Dict[str, Any]]]):
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
                    result = await self.router.recv_multipart()
                    if not result:
                        break
                    
                    identity, _, msg_bytes = result
                    import msgpack
                    message = msgpack.unpackb(msg_bytes, raw=False)
                    
                    logger.debug(f"Voyager: Received message from {identity.hex()}")
                    
                    # Dispatch to handler
                    if self._handler:
                        response_data = await self._handler(message)
                        response_bytes = msgpack.packb(response_data, use_bin_type=True)
                        await self.router.send_multipart([identity, b"", response_bytes])
                        
                except (zmq.ContextTerminated, zmq.ZMQError, asyncio.CancelledError):
                    self.running = False
                    break
                except Exception as e:
                    if self.running:
                        logger.error(f"Voyager: Transport server error: {e}")
                    await asyncio.sleep(1)
        finally:
            self.stop()

    async def send_to_peer(self, peer_address: str, peer_port: int, message: Dict[str, Any], timeout: int = 5000) -> Optional[Dict[str, Any]]:
        """Sends a message to a specific peer using a DEALER socket."""
        import msgpack
        dealer = self.ctx.socket(zmq.DEALER)
        dealer.setsockopt(zmq.LINGER, 0)
        target = f"tcp://{peer_address}:{peer_port}"
        
        try:
            dealer.connect(target)
            msg_bytes = msgpack.packb(message, use_bin_type=True)
            
            # Send [empty, message]
            await dealer.send_multipart([b"", msg_bytes])
            
            # Wait for response with timeout
            if await dealer.poll(timeout):
                _, resp_bytes = await dealer.recv_multipart()
                return msgpack.unpackb(resp_bytes, raw=False)
            else:
                logger.warning(f"Voyager: Timeout waiting for response from {target}")
                return None
        except Exception as e:
            logger.error(f"Voyager: Failed to send to {target}: {e}")
            return None
        finally:
            dealer.close()

    def stop(self):
        """Stops the transport layer."""
        self.running = False
        if self.router and not self.router.closed:
            self.router.close(linger=0)
        if self.ctx:
            self.ctx.term()
        logger.info("Voyager: Transport Layer stopped.")
