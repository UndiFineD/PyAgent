#!/usr/bin/env python3
"""Tests for the chat API."""
from fastapi.testclient import TestClient

# import the application under test
from chat.api import app


def test_create_and_post() -> None:
    """You should be able to create a room, post a message, and retrieve it."""
    client = TestClient(app)
    resp = client.post("/rooms", json={"name": "proj", "members": ["u"]})
    assert resp.status_code == 200
    resp = client.post("/rooms/proj/messages", json={"sender": "u", "text": "hi"})
    assert resp.status_code == 200
    resp = client.get("/rooms/proj/messages")
    assert resp.json()[0]["text"] == "hi"


def test_tool_posts(monkeypatch) -> None:
    """Using the send_message_tool should result in an HTTP POST to the correct endpoint with the correct payload."""
    # arrange: capture the httpx.post arguments
    captured: dict = {}

    def fake_post(url, json):
        """Fake httpx.post that captures the URL and JSON payload."""
        captured['url'] = url
        captured['json'] = json
        class Dummy:
            status_code = 200
            def json(self_inner):
                """Fake response JSON."""
                return {"ok": True}
        return Dummy()

    monkeypatch.setattr("chat.mcp_tools.httpx.post", fake_post)

    # act
    from chat.mcp_tools import send_message_tool
    send_message_tool("proj", "u", "hi")

    # assert
    assert captured['url'].endswith("/rooms/proj/messages")
    assert captured['json']["sender"] == "u"
    assert captured['json']["text"] == "hi"


def test_metric_increment():
    """Posting a message should increment the messages_counter metric."""
    from chat.api import messages_counter
    # reset counter to zero
    messages_counter._value.set(0)  # using internal var for simplicity

    client = TestClient(app)
    client.post("/rooms", json={"name": "m2", "members": ["x"]})
    client.post("/rooms/m2/messages", json={"sender": "x", "text": "hey"})
    assert messages_counter._value.get() == 1


def test_duplicate_room_fails() -> None:
    """Creating a room with a name that already exists should return a 400 error."""
    client = TestClient(app)
    client.post("/rooms", json={"name": "dup", "members": []})
    resp = client.post("/rooms", json={"name": "dup", "members": []})
    assert resp.status_code == 400


def test_post_to_missing_room() -> None:
    """Posting a message to a room that doesn't exist should return a 404 error."""
    client = TestClient(app)
    resp = client.post("/rooms/nope/messages", json={"sender": "x", "text": "h"})
    assert resp.status_code == 404


def test_get_history_missing_room() -> None:
    """Getting message history for a room that doesn't exist should return a 404 error."""
    client = TestClient(app)
    resp = client.get("/rooms/notfound/messages")
    assert resp.status_code == 404
