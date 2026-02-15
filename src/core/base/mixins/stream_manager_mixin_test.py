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

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""
Tests for Stream Manager Mixin.
Tests Redis-backed streaming capabilities adapted from Adorable patterns.
"""

import pytest
from unittest.mock import patch, AsyncMock
import time

from src.core.base.mixins.stream_manager_mixin import StreamManagerMixin, StreamState, StreamInfo


class MockStreamManagerMixin(StreamManagerMixin):
    """Test implementation of StreamManagerMixin."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class TestStreamManager:
    """Test cases for StreamManagerMixin."""

    @pytest.fixture
    def stream_manager(self):
        """Create a test stream manager instance."""
        return MockStreamManagerMixin()
    @pytest.fixture
    def stream_manager_with_redis(self):
        """Create a test stream manager with mocked Redis."""
        with patch('src.core.base.mixins.stream_manager_mixin.redis') as mock_redis:
            mock_client = AsyncMock()
            mock_redis.from_url.return_value = mock_client
            manager = MockStreamManagerMixin(redis_url="redis://test")
        return manager, mock_client

    def test_initialization_without_redis(self, stream_manager):
        """Test initialization when Redis is not available."""
        assert stream_manager.redis_client is None
        assert stream_manager.redis_publisher is None
        assert stream_manager.active_streams == {}
        assert stream_manager.stream_callbacks == {}

    def test_initialization_with_redis(self, stream_manager_with_redis):
        """Test initialization with Redis available."""
        manager, mock_client = stream_manager_with_redis
        assert manager.redis_client is not None
        assert manager.redis_publisher is not None

    @pytest.mark.asyncio
    async def test_get_stream_state_without_redis(self, stream_manager):
        """Test getting stream state when Redis is unavailable."""
        state = await stream_manager.get_stream_state("test_agent")
        assert isinstance(state, StreamState)
        assert state.state is None

    @pytest.mark.asyncio
    async def test_get_stream_state_with_redis(self, stream_manager_with_redis):
        """Test getting stream state with Redis."""
        manager, mock_client = stream_manager_with_redis

        # Mock Redis response
        mock_client.get.return_value = '{"state": "running", "last_updated": 1234567890.0}'

        state = await manager.get_stream_state("test_agent")

        assert state.state == "running"
        assert state.last_updated == 1234567890.0
        mock_client.get.assert_called_once_with("agent:test_agent:stream-state")

    @pytest.mark.asyncio
    async def test_is_stream_running(self, stream_manager_with_redis):
        """Test checking if stream is running."""
        manager, mock_client = stream_manager_with_redis

        mock_client.get.return_value = '{"state": "running"}'
        assert await manager.is_stream_running("test_agent")

        mock_client.get.return_value = '{"state": "stopped"}'
        assert not await manager.is_stream_running("test_agent")

        mock_client.get.return_value = None
        assert not await manager.is_stream_running("test_agent")

    @pytest.mark.asyncio
    async def test_stop_stream(self, stream_manager_with_redis):
        """Test stopping a stream."""
        manager, mock_client = stream_manager_with_redis

        # Add an active stream
        manager.active_streams["test_agent"] = StreamInfo(
            stream_id="test_stream",
            agent_id="test_agent",
            created_at=time.time(),
            last_keepalive=time.time()
        )

        await manager.stop_stream("test_agent")

        # Verify Redis calls
        mock_client.publish.assert_called_once()
        mock_client.delete.assert_called_once_with("agent:test_agent:stream-state")

        # Verify stream was removed
        assert "test_agent" not in manager.active_streams

    @pytest.mark.asyncio
    async def test_wait_for_stream_to_stop(self, stream_manager_with_redis):
        """Test waiting for stream to stop."""
        manager, mock_client = stream_manager_with_redis

        # Mock stream running then stopped
        call_count = 0

        async def mock_is_running(agent_id):
            nonlocal call_count
            call_count += 1
            return call_count <= 2  # Return True twice, then False

        manager.is_stream_running = mock_is_running

        result = await manager.wait_for_stream_to_stop("test_agent", max_attempts=5)
        assert result
        assert call_count == 3  # Should check 3 times: True, True, False

    @pytest.mark.asyncio
    async def test_clear_stream_state(self, stream_manager_with_redis):
        """Test clearing stream state."""
        manager, mock_client = stream_manager_with_redis

        # Add active stream
        manager.active_streams["test_agent"] = StreamInfo(
            stream_id="test_stream",
            agent_id="test_agent",
            created_at=time.time(),
            last_keepalive=time.time()
        )

        await manager.clear_stream_state("test_agent")

        mock_client.delete.assert_called_once_with("agent:test_agent:stream-state")
        assert "test_agent" not in manager.active_streams

    @pytest.mark.asyncio
    async def test_handle_stream_lifecycle_start(self, stream_manager_with_redis):
        """Test handling stream start lifecycle event."""
        manager, mock_client = stream_manager_with_redis

        await manager.handle_stream_lifecycle("test_agent", "start")

        # Verify stream was added
        assert "test_agent" in manager.active_streams
        stream_info = manager.active_streams["test_agent"]
        assert stream_info.agent_id == "test_agent"

        # Verify Redis state was set
        mock_client.setex.assert_called_once()

    @pytest.mark.asyncio
    async def test_handle_stream_lifecycle_finish(self, stream_manager_with_redis):
        """Test handling stream finish lifecycle event."""
        manager, mock_client = stream_manager_with_redis

        # Add active stream
        manager.active_streams["test_agent"] = StreamInfo(
            stream_id="test_stream",
            agent_id="test_agent",
            created_at=time.time(),
            last_keepalive=time.time()
        )

        await manager.handle_stream_lifecycle("test_agent", "finish")

        # Verify stream was cleared
        assert "test_agent" not in manager.active_streams
        mock_client.delete.assert_called_once()

    @pytest.mark.asyncio
    async def test_handle_stream_lifecycle_error(self, stream_manager_with_redis):
        """Test handling stream error lifecycle event."""
        manager, mock_client = stream_manager_with_redis

        # Add active stream
        manager.active_streams["test_agent"] = StreamInfo(
            stream_id="test_stream",
            agent_id="test_agent",
            created_at=time.time(),
            last_keepalive=time.time()
        )

        await manager.handle_stream_lifecycle("test_agent", "error")

        # Verify stream was cleared
        assert "test_agent" not in manager.active_streams
        mock_client.delete.assert_called_once()

    @pytest.mark.asyncio
    async def test_stream_context_manager(self, stream_manager_with_redis):
        """Test stream context manager."""
        manager, mock_client = stream_manager_with_redis

        async with manager.stream_context("test_agent"):
            # Verify stream was started
            assert "test_agent" in manager.active_streams

        # Verify stream was finished after context
        assert "test_agent" not in manager.active_streams

    @pytest.mark.asyncio
    async def test_stream_context_manager_with_exception(self, stream_manager_with_redis):
        """Test stream context manager handles exceptions."""
        manager, mock_client = stream_manager_with_redis

        with pytest.raises(ValueError):
            async with manager.stream_context("test_agent"):
                # Verify stream was started
                assert "test_agent" in manager.active_streams
                raise ValueError("Test exception")

        # Verify stream was cleaned up despite exception
        assert "test_agent" not in manager.active_streams






