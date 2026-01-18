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


"""Agent specializing in messaging platform integration (WhatsApp, Slack, Discord).
Provides a unified interface for external communications.
"""

from __future__ import annotations
from src.core.base.Version import VERSION
import logging
from typing import Any
from src.core.base.BaseAgent import BaseAgent
from src.core.base.BaseUtilities import as_tool

__version__ = VERSION


class MessagingAgent(BaseAgent):
    """Integrates with messaging platforms for fleet notifications."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._system_prompt = (
            "You are the Messaging Agent. "
            "Your role is to handle communications via external platforms like WhatsApp and Slack. "
            "You format reports for mobile reading and handle incoming alerts."
        )

    @as_tool
    async def send_notification(
        self, platform: str, recipient: str, message: str
    ) -> str:
        """Sends a message to a specific platform/recipient. (SKELETON)"""
        logging.info(f"Sending {platform} message to {recipient}: {message}")

        # Phase 125: Privacy Guard Integration
        if hasattr(self, "fleet") and self.fleet:
            privacy_guard = self.fleet.agents.get("PrivacyGuard")

            if privacy_guard and hasattr(privacy_guard, "verify_message_safety"):
                check_result = privacy_guard.verify_message_safety(message)
                if not check_result.get("safe", True):
                    return f"SAFETY ERROR: Message blocked. Reason: {check_result.get('reason')}"

        # In a real implementation, use Twilio API, Slack Webhooks, or Discord bots
        return f"Message sent to {recipient} via {platform} (Simulated)"

    @as_tool
    async def poll_for_replies(self, platform: str) -> list[dict[str, Any]]:
        """Polls for new messages on a specific platform."""
        logging.info(f"Polling {platform} for new messages...")
        return []  # Return empty list for now

    @as_tool
    async def format_for_mobile(self, report: str) -> str:
        """Truncates and formats a long report for messaging platforms."""
        return report[:500] + "..." if len(report) > 500 else report


if __name__ == "__main__":
    from src.core.base.BaseUtilities import create_main_function

    main = create_main_function(
        MessagingAgent, "Messaging Agent", "Messaging history path"
    )
    main()
