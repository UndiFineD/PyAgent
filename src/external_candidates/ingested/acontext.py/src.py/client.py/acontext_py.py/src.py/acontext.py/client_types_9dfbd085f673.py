# Extracted from: C:\DEV\PyAgent\.external\Acontext\src\client\acontext-py\src\acontext\client_types.py
"""
Common typing helpers used by resource modules to avoid circular imports.
"""

from collections.abc import Awaitable, Mapping
from typing import Any, BinaryIO, Protocol


class RequesterProtocol(Protocol):
    def request(
        self,
        method: str,
        path: str,
        *,
        params: Mapping[str, Any] | None = None,
        json_data: Mapping[str, Any] | None = None,
        data: Mapping[str, Any] | None = None,
        files: Mapping[str, tuple[str, BinaryIO, str | None]] | None = None,
        unwrap: bool = True,
    ) -> Any: ...


class AsyncRequesterProtocol(Protocol):
    def request(
        self,
        method: str,
        path: str,
        *,
        params: Mapping[str, Any] | None = None,
        json_data: Mapping[str, Any] | None = None,
        data: Mapping[str, Any] | None = None,
        files: Mapping[str, tuple[str, BinaryIO, str | None]] | None = None,
        unwrap: bool = True,
    ) -> Awaitable[Any]: ...
