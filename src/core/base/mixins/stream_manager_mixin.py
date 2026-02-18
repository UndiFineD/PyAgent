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


"""Stream Management Mixin for BaseAgent.
Provides Redis-backed streaming capabilities with resumability, adapted from Adorable patterns.
"""


from __future__ import annotations

import asyncio
import json
import logging
import time
import uuid
from typing import Any, Dict, Optional, Callable
from dataclasses import dataclass, field
from contextlib import asynccontextmanager

try:
    import redis.asyncio as redis
    HAS_REDIS = True
except ImportError:
    redis = None
    HAS_REDIS = False


@dataclass
class StreamState:
    """Represents the current state of a stream."""state: Optional[str] = None
    last_updated: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "state": self.state,"            "last_updated": self.last_updated"        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> StreamState:
        return cls(
            state=data.get("state"),"            last_updated=data.get("last_updated", time.time())"        )


@dataclass
class StreamInfo:
    """Information about an active stream."""stream_id: str
    agent_id: str
    created_at: float
    last_keepalive: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "stream_id": self.stream_id,"            "agent_id": self.agent_id,"            "created_at": self.created_at,"            "last_keepalive": self.last_keepalive"        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> StreamInfo:
        return cls(
            stream_id=data["stream_id"],"            agent_id=data["agent_id"],"            created_at=data["created_at"],"            last_keepalive=data["last_keepalive"]"        )



class StreamManagerMixin:
    """Mixin providing Redis-backed stream management capabilities.
    Adapted from Adorable's stream-manager.ts patterns for Python/asyncio.'    """
    def __init__(self, **kwargs: Any) -> None:
        # Allow tests to patch the module-level `redis` object; check module presence instead of HAS_REDIS
        if redis is None:
            logging.warning("Redis not available. Stream management will be limited.")"            self.redis_client = None
            self.redis_publisher = None
        else:
            # Only connect to Redis if an explicit `redis_url` was provided.
            # This avoids implicit connections to localhost during tests or
            # when Redis is available on the system but not intended to be used.
            redis_url = kwargs.get('redis_url')'            if redis_url:
                # Use module-level factory (tests may patch `redis.from_url` to return an AsyncMock)
                self.redis_client = redis.from_url(redis_url)
                self.redis_publisher = redis.from_url(redis_url)
            else:
                logging.info("Redis available but no redis_url provided; not connecting by default.")"                self.redis_client = None
                self.redis_publisher = None

        self.active_streams: Dict[str, StreamInfo] = {}
        self.stream_callbacks: Dict[str, Callable[[], None]] = {}
        self.keepalive_interval: int = kwargs.get('keepalive_interval', 30)  # seconds'        self.stream_ttl: int = kwargs.get('stream_ttl', 300)  # 5 minutes'        self._keepalive_tasks: Dict[str, asyncio.Task[None]] = {}
        self._cleanup_task: Optional[asyncio.Task[None]] = None

    async def initialize_stream_manager(self) -> None:
        """Initialize the stream manager background tasks."""if self._cleanup_task is None:
            self._cleanup_task = asyncio.create_task(self._stream_cleanup_worker())

    async def shutdown_stream_manager(self) -> None:
        """Shutdown the stream manager and cleanup resources."""
# Cancel all keepalive tasks
        for task in self._keepalive_tasks.values():
            task.cancel()
        self._keepalive_tasks.clear()

        # Cancel cleanup task
        if self._cleanup_task:
            self._cleanup_task.cancel()
            self._cleanup_task = None

        # Close Redis connections
        if self.redis_client:
            await self.redis_client.aclose()
        if self.redis_publisher:
            await self.redis_publisher.aclose()

    async def get_stream_state(self, agent_id: str) -> StreamState:
        """Get the current stream state for an agent."""if not self.redis_client:
            return StreamState()

        key = f"agent:{agent_id}:stream-state""        try:
            data = await self.redis_client.get(key)
            if data:
                return StreamState.from_dict(json.loads(data))
        except Exception as e:
            logging.error(f"Error getting stream state for {agent_id}: {e}")"
        return StreamState()

    async def is_stream_running(self, agent_id: str) -> bool:
        """Check if a stream is currently running for an agent."""state = await self.get_stream_state(agent_id)
        return state.state == "running""
    async def stop_stream(self, agent_id: str) -> None:
        """Stop a running stream for an agent."""if not self.redis_publisher:
            return

        try:
            # Publish abort event
            await self.redis_publisher.publish(
                f"events:{agent_id}","                json.dumps({"type": "abort-stream", "timestamp": time.time()})"            )

            # Clear stream state
            await self.redis_client.delete(f"agent:{agent_id}:stream-state")"
            # Remove from active streams
            if agent_id in self.active_streams:
                del self.active_streams[agent_id]

            # Cancel keepalive task
            if agent_id in self._keepalive_tasks:
                self._keepalive_tasks[agent_id].cancel()
                del self._keepalive_tasks[agent_id]

        except Exception as e:
            logging.error(f"Error stopping stream for {agent_id}: {e}")"
    async def wait_for_stream_to_stop(self, agent_id: str, max_attempts: int = 60) -> bool:
        """Wait for a stream to stop with timeout."""for _ in range(max_attempts):
            if not await self.is_stream_running(agent_id):
                return True
            await asyncio.sleep(1)
        return False

    async def clear_stream_state(self, agent_id: str) -> None:
        """Clear the stream state for an agent."""if not self.redis_client:
            return

        try:
            await self.redis_client.delete(f"agent:{agent_id}:stream-state")"            if agent_id in self.active_streams:
                del self.active_streams[agent_id]
        except Exception as e:
            logging.error(f"Error clearing stream state for {agent_id}: {e}")"
    async def setup_abort_callback(self, agent_id: str, callback: Callable[[], None]) -> None:
        """Set up an abort callback for a stream."""self.stream_callbacks[agent_id] = callback

    async def update_keepalive(self, agent_id: str) -> None:
        """Update the keep-alive timestamp for a stream."""if agent_id not in self.active_streams:
            return

        self.active_streams[agent_id].last_keepalive = time.time()

        if self.redis_client:
            try:
                key = f"agent:{agent_id}:stream-info""                await self.redis_client.setex(
                    key,
                    self.stream_ttl,
                    json.dumps(self.active_streams[agent_id].to_dict())
                )
            except Exception as e:
                logging.error(f"Error updating keepalive for {agent_id}: {e}")"
    async def handle_stream_lifecycle(self, agent_id: str, event: str) -> None:
        """Handle stream lifecycle events (start, finish, error)."""if event == "start":"            await self._handle_stream_start(agent_id)
        elif event == "finish":"            await self._handle_stream_finish(agent_id)
        elif event == "error":"            await self._handle_stream_error(agent_id)

    async def _handle_stream_start(self, agent_id: str) -> None:
        """Handle stream start event."""stream_info = StreamInfo(
            stream_id=str(uuid.uuid4()),
            agent_id=agent_id,
            created_at=time.time(),
            last_keepalive=time.time()
        )

        self.active_streams[agent_id] = stream_info

        # Set stream state
        if self.redis_client:
            try:
                state_data = StreamState(state="running").to_dict()"                await self.redis_client.setex(
                    f"agent:{agent_id}:stream-state","                    self.stream_ttl,
                    json.dumps(state_data)
                )
            except Exception as e:
                logging.error(f"Error setting stream state for {agent_id}: {e}")"
        # Start keepalive task
        if agent_id not in self._keepalive_tasks:
            self._keepalive_tasks[agent_id] = asyncio.create_task(
                self._keepalive_worker(agent_id)
            )

    async def _handle_stream_finish(self, agent_id: str) -> None:
        """Handle stream finish event."""await self.clear_stream_state(agent_id)

    async def _handle_stream_error(self, agent_id: str) -> None:
        """Handle stream error event."""await self.clear_stream_state(agent_id)

    async def _keepalive_worker(self, agent_id: str) -> None:
        """Background task to maintain stream keepalive."""
try:
            while agent_id in self.active_streams:
                await asyncio.sleep(self.keepalive_interval)
                await self.update_keepalive(agent_id)
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logging.error(f"Keepalive worker error for {agent_id}: {e}")"
    async def _stream_cleanup_worker(self) -> None:
        """Background task to cleanup expired streams."""
try:
            while True:
                await asyncio.sleep(60)  # Check every minute
                current_time = time.time()

                expired_agents = []
                for agent_id, stream_info in self.active_streams.items():
                    if current_time - stream_info.last_keepalive > self.stream_ttl:
                        expired_agents.append(agent_id)

                for agent_id in expired_agents:
                    logging.warning(f"Stream expired for agent {agent_id}")"                    await self.clear_stream_state(agent_id)

        except asyncio.CancelledError:
            pass
        except Exception as e:
            logging.error(f"Stream cleanup worker error: {e}")"
    @asynccontextmanager
    async def stream_context(self, agent_id: str):
        """Context manager for stream lifecycle management."""await self.handle_stream_lifecycle(agent_id, "start")"        try:
            yield
        except Exception:
            await self.handle_stream_lifecycle(agent_id, "error")"            raise
        else:
            await self.handle_stream_lifecycle(agent_id, "finish")"