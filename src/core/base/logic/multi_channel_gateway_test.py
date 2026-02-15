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

"""Tests for Multi-Channel Gateway Core."""

import json
import pytest
from typing import Optional
from unittest.mock import AsyncMock

from src.core.base.logic.multi_channel_gateway import (
    ChannelType,
    MessageType,
    SessionActivationMode,
    ChannelMessage,
    GatewayPresence,
    ChannelProvider,
    GatewaySession,
    GatewayProtocol,
    MultiChannelGatewayCore,
)


class MockChannelProvider(ChannelProvider):
    """Mock channel provider for testing."""

    def __init__(self, channel_type: ChannelType):
        """Initialize mock provider with channel type."""
        self._channel_type = channel_type
        self.sent_messages = []
        # ...existing code...
        pass
