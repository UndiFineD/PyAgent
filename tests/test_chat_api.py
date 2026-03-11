#!/usr/bin/env python3
"""Tests for the chat API."""
import importlib
from typing import Callable, Protocol, TypedDict, cast

import pytest
from _pytest.monkeypatch import MonkeyPatch

# fastapi import can raise a SystemError when pydantic-core version mismatches.
# skip the entire module in that case to allow the rest of the suite to run.
try:
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
except SystemError as e:
    pytest.skip(f"Skipping chat API tests due to import error: {e}", allow_module_level=True)


class CounterValueProtocol(Protocol):
    """Protocol for prometheus-like counter value internals used in tests."""

    def set(self, value: int) -> None:
        """Set the counter value."""

    def get(self) -> int:
        """Get the counter value."""


class CounterProtocol(Protocol):
    """Protocol for counters exposing an internal `_value` member."""

    _value: CounterValueProtocol


class MessagePayload(TypedDict):
    """Typed payload for chat messages posted through the tool."""

    sender: str
    text: str


class CapturedPost(TypedDict, total=False):
    """Captured HTTP call fields for fake post assertions."""

    url: str
    json: MessagePayload


def _load_app() -> FastAPI:
    """Load and return the FastAPI app from chat.api without requiring type stubs."""
    api_module = importlib.import_module("chat.api")
    return cast(FastAPI, api_module.app)


def _load_messages_counter() -> CounterProtocol:
    """Load and return chat.api.messages_counter as a typed counter protocol."""
    api_module = importlib.import_module("chat.api")
    return cast(CounterProtocol, api_module.messages_counter)


def test_create_and_post() -> None:
    """You should be able to create a room, post a message, and retrieve it."""
    app = _load_app()
    client = TestClient(app)
    resp = client.post("/rooms", json={"name": "proj", "members": ["u"]})
    assert resp.status_code == 200
    resp = client.post("/rooms/proj/messages", json={"sender": "u", "text": "hi"})
    assert resp.status_code == 200
    resp = client.get("/rooms/proj/messages")
    assert resp.json()[0]["text"] == "hi"


def test_tool_posts(monkeypatch: MonkeyPatch) -> None:
    """Using the send_message_tool should result in an HTTP POST to the correct endpoint with the correct payload."""
    # arrange: capture the httpx.post arguments
    captured: CapturedPost = {}

    def fake_post(url: str, json: MessagePayload) -> object:
        """Fake httpx.post that captures the URL and JSON payload."""
        captured['url'] = url
        captured['json'] = json

        class Dummy:
            """Dummy response object with expected interface for the tool."""

            status_code = 200

            def json(self) -> dict[str, bool]:
                """Fake response JSON."""
                return {"ok": True}

        return Dummy()

    monkeypatch.setattr("chat.mcp_tools.httpx.post", fake_post)

    # act
    mcp_module = importlib.import_module("chat.mcp_tools")
    send_message_tool = cast(Callable[[str, str, str], object], mcp_module.send_message_tool)
    send_message_tool("proj", "u", "hi")

    # assert
    assert captured['url'].endswith("/rooms/proj/messages")
    assert captured['json']["sender"] == "u"
    assert captured['json']["text"] == "hi"


def test_metric_increment() -> None:
    """Posting a message should increment the messages_counter metric."""
    messages_counter = _load_messages_counter()
    # reset counter to zero
    messages_counter._value.set(0)  # using internal var for simplicity

    app = _load_app()
    client = TestClient(app)
    client.post("/rooms", json={"name": "m2", "members": ["x"]})
    client.post("/rooms/m2/messages", json={"sender": "x", "text": "hey"})
    assert messages_counter._value.get() == 1


def test_duplicate_room_fails() -> None:
    """Creating a room with a name that already exists should return a 400 error."""
    app = _load_app()
    client = TestClient(app)
    client.post("/rooms", json={"name": "dup", "members": []})
    resp = client.post("/rooms", json={"name": "dup", "members": []})
    assert resp.status_code == 400


def test_post_to_missing_room() -> None:
    """Posting a message to a room that doesn't exist should return a 404 error."""
    app = _load_app()
    client = TestClient(app)
    resp = client.post("/rooms/nope/messages", json={"sender": "x", "text": "h"})
    assert resp.status_code == 404


def test_get_history_missing_room() -> None:
    """Getting message history for a room that doesn't exist should return a 404 error."""
    app = _load_app()
    client = TestClient(app)
    resp = client.get("/rooms/notfound/messages")
    assert resp.status_code == 404
