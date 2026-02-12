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

"""Unit tests for BaseAgent exception handling (Phase 336)."""

from unittest.mock import patch
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.common.models import FailureClassification


class TestBaseAgentExceptions:
    def test_classify_exception(self):
        # Mocking init to bypass side effects
        with patch("src.core.base.lifecycle.base_agent.BaseAgent.__init__", return_value=None):
            agent = BaseAgent()
            # Restore _classify_exception from the class
            agent._classify_exception = BaseAgent._classify_exception.__get__(agent, BaseAgent)

            assert agent._classify_exception(RecursionError("Max depth")) == FailureClassification.RECURSION_LIMIT.value
            assert agent._classify_exception(MemoryError("OOM")) == FailureClassification.RESOURCE_EXHAUSTION.value
            assert agent._classify_exception(Exception("Connection refused")
                                             ) == FailureClassification.NETWORK_FAILURE.value
            assert agent._classify_exception(Exception("Shard checksum failed")
                                             ) == FailureClassification.SHARD_CORRUPTION.value
            assert agent._classify_exception(ValueError("Bad val")) == FailureClassification.UNKNOWN.value

    @patch("src.core.base.lifecycle.base_agent.BaseAgent.run_async")
    @patch("src.core.base.lifecycle.base_agent.BaseAgent._notify_webhooks")
    @patch("src.core.base.lifecycle.base_agent.BaseAgent.__init__", return_value=None)
    def test_run_exception_handling(self, mock_init, mock_notify, mock_run_async):
        mock_run_async.side_effect = RecursionError("Loop detected")

        agent = BaseAgent()
        agent.run_async = mock_run_async
        agent._notify_webhooks = mock_notify
        # Manually bind run as we skipped init
        agent.run = BaseAgent.run.__get__(agent, BaseAgent)
        agent._classify_exception = BaseAgent._classify_exception.__get__(agent, BaseAgent)

        # Call sync run
        result = agent.run("test prompt")

        assert "Error:" in result
        assert FailureClassification.RECURSION_LIMIT.value in result

        mock_notify.assert_called_with(
            "agent_error",
            {
                "error": "Loop detected",
                "failure_type": FailureClassification.RECURSION_LIMIT.value
            }
        )
