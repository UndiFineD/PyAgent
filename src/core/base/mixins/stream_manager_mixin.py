#!/usr/bin/env python3
"""Stream manager mixin - minimal shim for tests.

Provides a no-Redis implementation that tracks streams in-memory
to keep unit tests importable and deterministic.
"""
from __future__ import annotations


import asyncio
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Optional


@dataclass
class StreamState:
    state: Optional[str] = None
    last_updated: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return {"state": self.state, "last_updated": self.last_updated}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "StreamState":
        return cls(state=data.get("state"), last_updated=data.get("last_updated", time.time()))


@dataclass
class StreamInfo:
    stream_id: str
    agent_id: str
    created_at: float
    last_keepalive: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "stream_id": self.stream_id,
            "agent_id": self.agent_id,
            "created_at": self.created_at,
            "last_keepalive": self.last_keepalive,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "StreamInfo":
        return cls(
            stream_id=data["stream_id"],
            agent_id=data["agent_id"],
            created_at=data["created_at"],
            last_keepalive=data["last_keepalive"],
        )


class StreamManagerMixin:
    def __init__(self, **kwargs: Any) -> None:
        self.active_streams: Dict[str, StreamInfo] = {}
        self.stream_callbacks: Dict[str, Callable[[], None]] = {}
        self.keepalive_interval: int = kwargs.get("keepalive_interval", 30)
        self.stream_ttl: int = kwargs.get("stream_ttl", 300)
        self._keepalive_tasks: Dict[str, asyncio.Task[None]] = {}
        self._cleanup_task: Optional[asyncio.Task[None]] = None

    async def initialize_stream_manager(self) -> None:
        if self._cleanup_task is None:
            self._cleanup_task = asyncio.create_task(self._stream_cleanup_worker())

    async def shutdown_stream_manager(self) -> None:
        for task in self._keepalive_tasks.values():
            task.cancel()
        self._keepalive_tasks.clear()
        if self._cleanup_task:
            self._cleanup_task.cancel()
            self._cleanup_task = None

    async def get_stream_state(self, agent_id: str) -> StreamState:
        info = self.active_streams.get(agent_id)
        if not info:
            return StreamState()
        return StreamState(state="running", last_updated=info.last_keepalive)

    async def is_stream_running(self, agent_id: str) -> bool:
        state = await self.get_stream_state(agent_id)
        return state.state == "running"

    async def stop_stream(self, agent_id: str) -> None:
        if agent_id in self.active_streams:
            del self.active_streams[agent_id]
        if agent_id in self._keepalive_tasks:
            self._keepalive_tasks[agent_id].cancel()
            del self._keepalive_tasks[agent_id]

    async def clear_stream_state(self, agent_id: str) -> None:
        if agent_id in self.active_streams:
            del self.active_streams[agent_id]

    async def setup_abort_callback(self, agent_id: str, callback: Callable[[], None]) -> None:
        self.stream_callbacks[agent_id] = callback

    async def update_keepalive(self, agent_id: str) -> None:
        if agent_id not in self.active_streams:
            return
        self.active_streams[agent_id].last_keepalive = time.time()

    async def handle_stream_lifecycle(self, agent_id: str, event: str) -> None:
        if event == "start":
            await self._handle_stream_start(agent_id)
        elif event == "finish":
            await self._handle_stream_finish(agent_id)
        elif event == "error":
            await self._handle_stream_error(agent_id)

    async def _handle_stream_start(self, agent_id: str) -> None:
        stream_info = StreamInfo(stream_id=str(uuid.uuid4()), agent_id=agent_id, created_at=time.time(), last_keepalive=time.time())
        self.active_streams[agent_id] = stream_info
        if agent_id not in self._keepalive_tasks:
            self._keepalive_tasks[agent_id] = asyncio.create_task(self._keepalive_worker(agent_id))

    async def _handle_stream_finish(self, agent_id: str) -> None:
        await self.clear_stream_state(agent_id)

    async def _handle_stream_error(self, agent_id: str) -> None:
        await self.clear_stream_state(agent_id)

    async def _keepalive_worker(self, agent_id: str) -> None:
        try:
            while agent_id in self.active_streams:
                await asyncio.sleep(self.keepalive_interval)
                await self.update_keepalive(agent_id)
        except asyncio.CancelledError:
            pass

    async def _stream_cleanup_worker(self) -> None:
        try:
            while True:
                await asyncio.sleep(self.keepalive_interval)
                now = time.time()
                to_remove = []
                for agent_id, info in list(self.active_streams.items()):
                    if now - info.last_keepalive > self.stream_ttl:
                        to_remove.append(agent_id)
                for agent_id in to_remove:
                    await self.clear_stream_state(agent_id)
        except asyncio.CancelledError:
            pass
