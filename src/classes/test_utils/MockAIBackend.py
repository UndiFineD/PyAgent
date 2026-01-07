#!/usr/bin/env python3

"""Auto-extracted class from agent_test_utils.py"""

from __future__ import annotations

from .MockResponse import MockResponse
from .MockResponseType import MockResponseType

from typing import Dict, List, Tuple
import logging
import re
import time

class MockAIBackend:
    """Mock AI backend for testing.

    Provides configurable mock responses for AI backend calls
    without making real API requests.

    Example:
        mock=MockAIBackend()
        mock.add_response("prompt1", MockResponse(content="response"))
        result=mock.call("prompt1")
    """

    def __init__(self) -> None:
        """Initialize mock backend."""
        self._responses: Dict[str, MockResponse] = {}
        self._default_response = MockResponse(content="Mock response")
        self._call_history: List[Tuple[str, float]] = []
        self._response_sequence: List[MockResponse] = []
        self._sequence_index: int = 0

    def add_response(
        self,
        prompt_pattern: str,
        response: MockResponse,
    ) -> None:
        """Add mock response for a prompt pattern.

        Args:
            prompt_pattern: Prompt pattern (can be exact or regex).
            response: Mock response to return.
        """
        self._responses[prompt_pattern] = response
        logging.debug(f"Added mock response for pattern: {prompt_pattern}")

    def set_default_response(self, response: MockResponse) -> None:
        """Set default response for unmatched prompts.

        Args:
            response: Default mock response.
        """
        self._default_response = response

    def call(self, prompt: str) -> str:
        """Call mock backend with prompt.

        Args:
            prompt: Prompt to send.

        Returns:
            str: Mock response content.

        Raises:
            TimeoutError: If response type is TIMEOUT.
            RuntimeError: If response type is ERROR.
        """
        self._call_history.append((prompt, time.time()))

        # Use response sequence if available
        if self._response_sequence and self._sequence_index < len(self._response_sequence):
            response = self._response_sequence[self._sequence_index]
            self._sequence_index += 1
        else:
            # Find matching response
            response = self._default_response
            for pattern, resp in self._responses.items():
                if pattern in prompt or re.search(pattern, prompt):
                    response = resp
                    break

        # Simulate latency
        if response.latency_ms > 0:
            time.sleep(response.latency_ms / 1000)

        # Handle response types
        if response.response_type == MockResponseType.TIMEOUT:
            raise TimeoutError("Mock timeout")
        if response.response_type == MockResponseType.ERROR:
            raise RuntimeError(response.error_message or "Mock error")
        if response.response_type == MockResponseType.RATE_LIMITED:
            raise RuntimeError("Rate limited")
        if response.response_type == MockResponseType.EMPTY:
            return ""

        return response.content

    def add_response_sequence(self, responses: List[MockResponse]) -> None:
        """Add a sequence of responses for sequential calls.

        Args:
            responses: List of mock responses.
        """
        self._response_sequence = responses
        self._sequence_index = 0

    def set_error_response(self, response_type: MockResponseType, message: str) -> None:
        """Set an error response to be returned.

        Args:
            response_type: Type of error response.
            message: Error message.
        """
        self._default_response = MockResponse(
            response_type=response_type,
            error_message=message
        )

    def get_call_history(self) -> List[Tuple[str, float]]:
        """Get history of calls made."""
        return list(self._call_history)

    def clear(self) -> None:
        """Clear all mock responses and history."""
        self._responses.clear()
        self._call_history.clear()
