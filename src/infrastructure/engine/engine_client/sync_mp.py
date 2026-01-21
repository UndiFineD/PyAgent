"""
Phase 45: Synchronous Multi-process Engine Client
ZMQ-based synchronous client.
"""

from __future__ import annotations
import logging
from typing import Optional, TYPE_CHECKING
from src.infrastructure.engine.engine_client.base import EngineCoreClientBase
from src.infrastructure.engine.engine_client.types import EngineOutput

if TYPE_CHECKING:
    import zmq
    from src.infrastructure.engine.engine_client.types import EngineClientConfig, SchedulerOutput

logger = logging.getLogger(__name__)


class SyncMPClient(EngineCoreClientBase["SchedulerOutput", EngineOutput]):
    """
    Synchronous multi-process engine client with ZMQ.

    Blocking request/response pattern.
    """

    def __init__(self, config: EngineClientConfig):
        super().__init__(config)
        self._context: Optional[zmq.Context] = None
        self._socket: Optional[zmq.Socket] = None
        self._pending: dict[str, EngineOutput] = {}

    def _init_zmq(self) -> None:
        """Initialize ZMQ socket."""
        try:
            import zmq
            self._context = zmq.Context()
            self._socket = self._context.socket(zmq.REQ)
            self._socket.setsockopt(zmq.RCVTIMEO, self.config.request_timeout_ms)
            self._socket.setsockopt(zmq.SNDTIMEO, self.config.request_timeout_ms)
            self._socket.connect(self.config.zmq_endpoint)
        except ImportError:
            logger.warning("ZMQ not available, using mock mode")

    def send_request(self, request: SchedulerOutput) -> str:
        """Send request via ZMQ."""
        request_id = self._generate_request_id()

        if self._socket is None:
            # Mock mode
            self._pending[request_id] = EngineOutput(
                request_id=request_id,
                outputs=[{"mock": True}],
                finished=True
            )
            return request_id

        try:
            import msgpack
            payload = msgpack.packb({
                "request_id": request_id,
                "request_ids": request.request_ids,
                "scheduled_tokens": request.scheduled_tokens,
                "num_prefill": request.num_prefill,
                "num_decode": request.num_decode,
            })
            self._socket.send(payload)

            # Blocking receive
            response = self._socket.recv()
            data = msgpack.unpackb(response)

            self._pending[request_id] = EngineOutput(
                request_id=request_id,
                outputs=data.get("outputs", []),
                finished=data.get("finished", True),
                metrics=data.get("metrics", {})
            )
        except Exception as e:
            logger.error(f"ZMQ error: {e}")
            self._pending[request_id] = EngineOutput(
                request_id=request_id,
                error=str(e)
            )

        return request_id

    def get_output(self, request_id: str, timeout_ms: Optional[int] = None) -> Optional[EngineOutput]:
        """Get output synchronously."""
        return self._pending.pop(request_id, None)

    async def get_output_async(self, request_id: str, timeout_ms: Optional[int] = None) -> Optional[EngineOutput]:
        """Get output (sync wrapper for async interface)."""
        return self.get_output(request_id, timeout_ms)

    def start(self) -> None:
        """Start client."""
        self._init_zmq()
        self._running = True
        logger.info("SyncMPClient started")

    def shutdown(self) -> None:
        """Shutdown client."""
        self._running = False
        if self._socket:
            self._socket.close()
        if self._context:
            self._context.term()
        logger.info("SyncMPClient shutdown")
