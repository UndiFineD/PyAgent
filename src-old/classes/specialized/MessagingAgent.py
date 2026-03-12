#!/usr/bin/env python3

"""
LLM_CONTEXT_START

## Source: src-old/classes/specialized/MessagingAgent.description.md

# MessagingAgent

**File**: `src\classes\specialized\MessagingAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 38  
**Complexity**: 3 (simple)

## Overview

Agent specializing in messaging platform integration (WhatsApp, Slack, Discord).
Provides a unified interface for external communications.

## Classes (1)

### `MessagingAgent`

**Inherits from**: BaseAgent

Integrates with messaging platforms for fleet notifications.

**Methods** (3):
- `__init__(self, file_path)`
- `send_notification(self, platform, recipient, message)`
- `format_for_mobile(self, report)`

## Dependencies

**Imports** (8):
- `logging`
- `src.classes.base_agent.BaseAgent`
- `src.classes.base_agent.utilities.as_tool`
- `src.classes.base_agent.utilities.create_main_function`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/classes/specialized/MessagingAgent.improvements.md

# Improvements for MessagingAgent

**File**: `src\classes\specialized\MessagingAgent.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 38 lines (small)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `MessagingAgent_test.py` with pytest tests

## Best Practices Checklist

- All classes have docstrings
- All public methods have docstrings
- Type hints are present
- pytest tests cover main functionality
- Error handling is robust
- Code follows PEP 8 style guide
- No code duplication
- Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

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

        main = create_main_function(
            MessagingAgent, "Messaging Agent", "Messaging history path"
        )
        main()
