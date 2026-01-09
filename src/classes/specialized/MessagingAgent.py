#!/usr/bin/env python3

"""Agent specializing in messaging platform integration (WhatsApp, Slack, Discord).
Provides a unified interface for external communications.
"""

import logging
from typing import Dict, List, Any, Optional
from src.classes.base_agent import BaseAgent
from src.classes.base_agent.utilities import as_tool

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
    def send_notification(self, platform: str, recipient: str, message: str) -> str:
        """Sends a message to a specific platform/recipient. (SKELETON)"""
        logging.info(f"Sending {platform} message to {recipient}: {message}")
        # In a real implementation, use Twilio API, Slack Webhooks, or Discord bots
        return f"Message sent to {recipient} via {platform} (Simulated)"

    @as_tool
    def format_for_mobile(self, report: str) -> str:
        """Truncates and formats a long report for messaging platforms."""
        return report[:500] + "..." if len(report) > 500 else report

if __name__ == "__main__":
    from src.classes.base_agent.utilities import create_main_function
    main = create_main_function(MessagingAgent, "Messaging Agent", "Messaging history path")
    main()
