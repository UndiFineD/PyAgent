# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agentcloud.py\agent_backend.py\src.py\test.py\messaging.py\test_send_message_to_socket_e97f2a501e29.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agentcloud\agent-backend\src\test\messaging\test_send_message_to_socket.py

from unittest.mock import MagicMock, patch

import pytest

from messaging import send_message_to_socket as sms

from models.sockets import SocketEvents, SocketMessage

from pydantic import ValidationError

from socketio import SimpleClient


class TestSend:
    @pytest.fixture
    def mock_client(self):
        return MagicMock(spec=SimpleClient)

    @pytest.fixture
    def mock_event(self):
        return MagicMock(spec=SocketEvents)

    @pytest.fixture
    def mock_message(self):
        return MagicMock(spec=SocketMessage)

    def test_send_with_invalid_socket_or_logging(self, mock_client, mock_event, mock_message):
        with pytest.raises((ValidationError, AssertionError, TypeError)) as excinfo:
            sms.send(mock_client, mock_event, mock_message, socket_or_logging="invalid_value")

    def test_send_socket_behavior_none_inputs(self):
        with pytest.raises(AssertionError) as excinfo:
            sms.send(None, None, None, socket_logging="socket")

        assert "client cannot be None" in str(excinfo.value)
