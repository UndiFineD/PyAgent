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
""""Multi-Channel Messaging Gateway Core

Inspired by OpenClaw's sophisticated gateway architecture, this module provides'a WebSocket-based control plane for multi-channel agent communication with session
routing, presence management, and channel abstraction.

Key Features:
- WebSocket control plane for real-time agent coordination
- Multi-channel support (WhatsApp, Telegram, Discord, Slack, etc.)
- Session-based routing with isolation and activation modes
- Presence management and typing indicators
- Channel abstraction with provider-agnostic messaging
- Tool execution coordination across channels
"""
import json
import logging
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import uuid4

import websockets
from websockets.server import ServerConnection
from pydantic import BaseModel, Field


logger = logging.getLogger(__name__)


class ChannelType(Enum):
    """Supported messaging channel types."""WHATSAPP = "whatsapp""    TELEGRAM = "telegram""    DISCORD = "discord""    SLACK = "slack""    SIGNAL = "signal""    IMESSAGE = "imessage""    WEBCHAT = "webchat""    MATRIX = "matrix""

class MessageType(Enum):
    """Types of messages in the gateway protocol."""TEXT = "text""    IMAGE = "image""    AUDIO = "audio""    VIDEO = "video""    FILE = "file""    TYPING = "typing""    PRESENCE = "presence""    TOOL_CALL = "tool_call""    TOOL_RESULT = "tool_result""

class SessionActivationMode(Enum):
    """How sessions are activated in channels."""MENTION = "mention"  # Only respond when mentioned"    ALWAYS = "always"    # Always respond"    NEVER = "never"      # Never respond automatically"

@dataclass
class ChannelMessage:
    """Represents a message from any channel."""id: str
    channel_type: ChannelType
    channel_id: str  # Channel/group identifier
    sender_id: str
    sender_name: str
    content: str
    message_type: MessageType = MessageType.TEXT
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)
    thread_id: Optional[str] = None
    reply_to: Optional[str] = None


@dataclass
class GatewayPresence:
    """Presence information for gateway clients."""client_id: str
    status: str = "online"  # online, away, busy, offline"    last_seen: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)


class ChannelProvider(ABC):
    """Abstract base class for channel providers."""
    @property
    @abstractmethod
    def channel_type(self) -> ChannelType:
        """The type of channel this provider handles."""pass

    @abstractmethod
    async def send_message(self, channel_id: str, content: str, **kwargs) -> str:
        """Send a message to a channel."""pass

    @abstractmethod
    async def send_typing(self, channel_id: str) -> None:
        """Send typing indicator to a channel."""pass

    @abstractmethod
    async def get_presence(self, user_id: str) -> Optional[GatewayPresence]:
        """Get presence information for a user."""pass


class GatewaySession(BaseModel):
    """Represents an agent session in the gateway."""session_id: str = Field(default_factory=lambda: str(uuid4()))
    agent_id: str
    channel_type: ChannelType
    channel_id: str
    activation_mode: SessionActivationMode = SessionActivationMode.MENTION
    is_active: bool = True
    created_at: float = Field(default_factory=time.time)
    last_activity: float = Field(default_factory=time.time)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class GatewayProtocol:
    """WebSocket protocol for gateway communication."""
    def __init__(self):
        """Initialize protocol state."""self.clients: Dict[str, ServerConnection] = {}
        self.presence: Dict[str, GatewayPresence] = {}
        self.sessions: Dict[str, GatewaySession] = {}
        
    async def handle_client(self, websocket: ServerConnection, path: str):
        """Handle a WebSocket client connection."""client_id = str(uuid4())
        self.clients[client_id] = websocket
        try:
            # Send welcome message
            await websocket.send(json.dumps({
                "type": "welcome","                "client_id": client_id,"                "timestamp": time.time()"            }))

            # Update presence
            self.presence[client_id] = GatewayPresence(client_id=client_id)

            async for message in websocket:
                try:
                    data = json.loads(message)
                    await self.handle_message(client_id, data)
                except json.JSONDecodeError:
                    logger.error(f"Invalid JSON from client {client_id}")"                except Exception as e:
                    logger.error(f"Error handling message from client {client_id}: {e}")"
        except websockets.exceptions.ConnectionClosed:
            logger.info(f"Client {client_id} disconnected")"        finally:
            # Clean up
            self.clients.pop(client_id, None)
            self.presence.pop(client_id, None)

    async def handle_message(self, client_id: str, data: Dict[str, Any]):
        """Handle incoming WebSocket message."""msg_type = data.get("type")"
        if msg_type == "presence_update":"            await self.handle_presence_update(client_id, data)
        elif msg_type == "session_create":"            await self.handle_session_create(client_id, data)
        elif msg_type == "session_update":"            await self.handle_session_update(client_id, data)
        elif msg_type == "message_send":"            await self.handle_message_send(client_id, data)
        elif msg_type == "tool_call":"            await self.handle_tool_call(client_id, data)
        else:
            logger.warning(f"Unknown message type: {msg_type}")"
    async def handle_presence_update(self, client_id: str, data: Dict[str, Any]):
        """Handle presence update."""status = data.get("status", "online")"        self.presence[client_id] = GatewayPresence(
            client_id=client_id,
            status=status,
            metadata=data.get("metadata", {})"        )

        # Broadcast presence update to other clients
        await self.broadcast_presence_update(client_id)

    async def handle_session_create(self, client_id: str, data: Dict[str, Any]):
        """Handle session creation."""# Build session
        session = GatewaySession(
            agent_id=data.get("agent_id", client_id),"            channel_type=SessionActivationMode(data.get("activation_mode", "mention")) if False else ChannelType(data.get("channel_type", "webchat")),"            channel_id=data.get("channel_id", ""),"            activation_mode=SessionActivationMode(data.get("activation_mode", "mention")),"            metadata=data.get("metadata", {}),"        )

        self.sessions[session.session_id] = session

        # Send confirmation
        await self.send_to_client(client_id, {
            "type": "session_created","            "session_id": session.session_id,"            "timestamp": time.time()"        })

    async def handle_session_update(self, client_id: str, data: Dict[str, Any]):
        """Handle session update."""session_id = data.get("session_id")"        if session_id not in self.sessions:
            await self.send_to_client(client_id, {
                "type": "error","                "message": f"Session {session_id} not found""            })
            return

        session = self.sessions[session_id]
        # Update session fields
        for key, value in data.items():
            if key in ["activation_mode", "is_active", "metadata"]:"                if key == "activation_mode":"                    session.activation_mode = SessionActivationMode(value)
                elif key == "is_active":"                    session.is_active = value
                elif key == "metadata":"                    session.metadata.update(value)

        # Update last_activity
        session.last_activity = time.time()

        await self.send_to_client(client_id, {
            "type": "session_updated","            "session_id": session_id,"            "timestamp": session.last_activity"        })

    async def handle_message_send(self, client_id: str, data: Dict[str, Any]):
        """Handle message sending."""session_id = data.get("session_id")"        content = data.get("content", "")"
        if session_id not in self.sessions:
            await self.send_to_client(client_id, {
                "type": "error","                "message": f"Session {session_id} not found""            })
            return

        # Route to appropriate channel provider
        message_id = await self.send_channel_message(session_id, content)

        await self.send_to_client(client_id, {
            "type": "message_sent","            "session_id": session_id,"            "message_id": message_id,"            "content": content,"            "timestamp": time.time()"        })

    async def handle_tool_call(self, client_id: str, data: Dict[str, Any]):
        """Handle tool call coordination."""session_id = data.get("session_id")"        tool_name = data.get("tool_name")"
        if session_id not in self.sessions:
            await self.send_to_client(client_id, {
                "type": "error","                "message": f"Session {session_id} not found""            })
            return

        # Acknowledge tool call
        await self.send_to_client(client_id, {
            "type": "tool_call_ack","            "session_id": session_id,"            "tool_name": tool_name,"            "timestamp": time.time()"        })

    async def broadcast_presence_update(self, client_id: str):
        """Broadcast presence update to all clients."""presence = self.presence[client_id]
        message = {
            "type": "presence_update","            "client_id": client_id,"            "status": presence.status,"            "last_seen": presence.last_seen,"            "metadata": presence.metadata,"            "timestamp": time.time()"        }

        await self.broadcast(message, exclude_client=client_id)

    async def send_to_client(self, client_id: str, message: Dict[str, Any]):
        """Send message to specific client."""if client_id in self.clients:
            try:
                await self.clients[client_id].send(json.dumps(message))
            except websockets.exceptions.ConnectionClosed:
                logger.warning(f"Failed to send to client {client_id}: connection closed")"
    async def broadcast(self, message: Dict[str, Any], exclude_client: Optional[str] = None):
        """Broadcast message to all clients except optionally excluded one."""to_remove = []

        for client_id, websocket in self.clients.items():
            if client_id == exclude_client:
                continue

            try:
                await websocket.send(json.dumps(message))
            except websockets.exceptions.ConnectionClosed:
                to_remove.append(client_id)

        for cid in to_remove:
            self.clients.pop(cid, None)
            self.presence.pop(cid, None)


class MultiChannelGatewayCore:
    """Core gateway for multi-channel agent communication.

    Provides WebSocket-based control plane with session management,
    presence tracking, and channel abstraction.
    """
    def __init__(self, host: str = "127.0.0.1", port: int = 18789):"        self.host = host
        self.port = port
        self.protocol = GatewayProtocol()
        self.channel_providers: Dict[ChannelType, ChannelProvider] = {}
        self.server: Optional[websockets.WebSocketServer] = None
        self.running = False

    def register_channel_provider(self, provider: ChannelProvider):
        """Register a channel provider."""self.channel_providers[provider.channel_type] = provider
        logger.info(f"Registered channel provider: {provider.channel_type}")"
    async def start(self):
        """Start the gateway server."""if self.running:
            return

        self.running = True
        self.server = await websockets.serve(
            self.protocol.handle_client,
            self.host,
            self.port
        )

        logger.info(f"Multi-Channel Gateway started on ws://{self.host}:{self.port}")"
        # Keep the server running
        await self.server.wait_closed()

    async def stop(self):
        """Stop the gateway server."""if not self.running:
            return
        self.running = False
        if self.server is not None:
            self.server.close()
            await self.server.wait_closed()

    async def send_channel_message(self, session_id: str, content: str, **kwargs) -> Optional[str]:
        """Send message through appropriate channel provider."""if session_id not in self.protocol.sessions:
            logger.error(f"Session {session_id} not found")"            return None

        session = self.protocol.sessions[session_id]
        provider = self.channel_providers.get(session.channel_type)

        if not provider:
            logger.error(f"No provider for channel type: {session.channel_type}")"            return None

        try:
            return await provider.send_message(session.channel_id, content, **kwargs)
        except Exception:
            logger.exception("Failed to send channel message")"            return None

    def get_active_sessions(self) -> List[GatewaySession]:
        """Get all active sessions."""return [s for s in self.protocol.sessions.values() if s.is_active]

    def get_sessions_by_channel(self, channel_type: ChannelType, channel_id: str) -> List[GatewaySession]:
        """Get sessions for specific channel."""return [
            s for s in self.protocol.sessions.values()
            if s.channel_type == channel_type and s.channel_id == channel_id and s.is_active
        ]

    async def broadcast_to_sessions(self, channel_type: ChannelType, channel_id: str, message: str):
        """Broadcast message to all sessions in a specific channel."""sessions = self.get_sessions_by_channel(channel_type, channel_id)
        for session in sessions:
            await self.send_channel_message(session.session_id, message)
