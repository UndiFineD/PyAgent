#!/usr/bin/env python3

"""Auto-extracted class from agent_test_utils.py"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable
import re

class AssertionHelpers:
    """Helper functions for common assertions in tests."""

    @staticmethod
    def assert_file_contains(file_path: Path, text: str) -> bool:
        """Assert that a file contains specific text.

        Args:
            file_path: Path to the file.
            text: Text to search for.

        Returns:
            True if assertion passes.

        Raises:
            AssertionError: If text is not found.
        """
        content = file_path.read_text()
        assert text in content, f"File {file_path} does not contain '{text}'"
        return True

    @staticmethod
    def assert_output_matches_pattern(output: str, pattern: str) -> bool:
        """Assert that output matches a regex pattern.

        Args:
            output: The output string.
            pattern: The regex pattern.

        Returns:
            True if assertion passes.

        Raises:
            AssertionError: If pattern does not match.
        """
        assert re.search(pattern, output), f"Output does not match pattern '{pattern}'"
        return True

    @staticmethod
    def assert_raises_with_message(
        fn: Callable[..., Any],
        exception_type: type[BaseException],
        message: str,
        *args: Any,
    ) -> bool:
        """Assert that a function raises an exception with a specific message.

        Args:
            fn: Function to call.
            exception_type: Expected exception type.
            message: Expected message text.
            *args: Arguments to pass to the function.

        Returns:
            True if assertion passes.

        Raises:
            AssertionError: If exception is not raised or message doesn't match.
        """
        try:
            fn(*args)
            raise AssertionError(f"Expected {exception_type.__name__} but no exception was raised")
        except BaseException as e:
            if isinstance(e, exception_type):
                assert message in str(e), f"Exception message '{str(e)}' does not contain '{message}'"
                return True
            raise
