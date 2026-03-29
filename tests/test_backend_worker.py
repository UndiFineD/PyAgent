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
"""Tests for the backend worker package.

prj0000029 — LLM UI Backend Worker.
"""

from __future__ import annotations

import base64
import importlib
import json

from fastapi.testclient import TestClient

from backend.app import app
from backend.models import (
    ActionRequestMessage,
    ControlMessage,
    InitMessage,
    RunTaskMessage,
    SignalMessage,
    SpeechTranscriptMessage,
    TaskCompleteMessage,
    TaskDeltaMessage,
    TaskErrorMessage,
    TaskStartedMessage,
)
from backend.session_manager import SessionManager
from backend.ws_crypto import (
    decrypt_message,
    derive_shared_secret,
    encrypt_message,
    generate_keypair,
)


def test_backend_package_importable():
    mod = importlib.import_module("backend")
    assert mod is not None


def test_backend_app_importable():
    mod = importlib.import_module("backend.app")
    assert hasattr(mod, "app")


# ─── Model tests ──────────────────────────────────────────────────────────


def test_init_message_schema():
    msg = InitMessage(type="init", session_id="abc", client_info={"v": 1})
    d = msg.model_dump()
    assert d["type"] == "init"
    assert d["client_info"] == {"v": 1}


def test_run_task_message_schema():
    msg = RunTaskMessage(type="runTask", task_id="t1", task="generateText", payload={"prompt": "hi"})
    assert msg.payload["prompt"] == "hi"


def test_task_started_message_type():
    msg = TaskStartedMessage(task_id="t1", started_at="2026-01-01T00:00:00Z")
    assert json.loads(msg.model_dump_json())["type"] == "taskStarted"


def test_task_delta_message_type():
    msg = TaskDeltaMessage(task_id="t1", delta=" token")
    d = json.loads(msg.model_dump_json())
    assert d["type"] == "taskDelta"
    assert d["delta"] == " token"


def test_task_complete_status_default():
    msg = TaskCompleteMessage(task_id="t1", result={"text": "done"})
    assert msg.status == "success"


def test_task_error_code_default():
    msg = TaskErrorMessage(task_id="t1", error="boom")
    assert msg.code == "UNKNOWN"


def test_action_request_message_schema():
    msg = ActionRequestMessage(action="openFile", params={"path": "/tmp/f"})
    assert msg.action == "openFile"


def test_control_message_action():
    msg = ControlMessage(type="control", task_id="t1", action="cancel")
    assert msg.action == "cancel"


def test_speech_transcript_is_final_default():
    msg = SpeechTranscriptMessage(type="speechTranscript", transcript="hello")
    assert msg.is_final is True


def test_signal_message_schema():
    msg = SignalMessage(
        type="signal",
        session_id="s1",
        peer_id="p1",
        signal_type="offer",
        payload={"sdp": "v=0"},
    )
    assert msg.signal_type == "offer"


# ─── SessionManager tests ─────────────────────────────────────────────────


def test_session_manager_initially_empty():
    sm = SessionManager()
    assert sm.all_sessions() == {}


def test_session_manager_get_unknown_returns_none():
    sm = SessionManager()
    assert sm.get("nonexistent") is None


def test_session_manager_disconnect_unknown_is_safe():
    sm = SessionManager()
    sm.disconnect("ghost")  # must not raise


# ─── FastAPI HTTP tests ───────────────────────────────────────────────────

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# ─── WebSocket E2E helpers ────────────────────────────────────────────────


def _ws_handshake(ws) -> bytes:  # type: ignore[no-untyped-def]
    """Perform X25519 ECDH key exchange and return the session_key."""
    server_pub = base64.b64decode(ws.receive_text())
    client_priv, client_pub = generate_keypair()
    ws.send_text(base64.b64encode(client_pub).decode())
    return derive_shared_secret(client_priv, server_pub)


def _ws_send(ws, session_key: bytes, obj: dict) -> None:  # type: ignore[no-untyped-def]
    """Encrypt and send a JSON dict over the WebSocket."""
    plaintext = json.dumps(obj).encode("utf-8")
    ws.send_text(base64.b64encode(encrypt_message(session_key, plaintext)).decode())


def _ws_recv(ws, session_key: bytes) -> dict:  # type: ignore[no-untyped-def]
    """Receive an encrypted WebSocket frame and return the decoded JSON dict."""
    raw = decrypt_message(session_key, base64.b64decode(ws.receive_text()))
    return json.loads(raw)


# ─── WebSocket tests ──────────────────────────────────────────────────────


def test_ws_init_ack():
    with client.websocket_connect("/ws") as ws:
        session_key = _ws_handshake(ws)
        _ws_send(ws, session_key, {"type": "init", "session_id": "test"})
        data = _ws_recv(ws, session_key)
        assert data["type"] == "initAck"
        assert data["server_version"] == "0.1.0"


def test_ws_run_task_streams_tokens():
    with client.websocket_connect("/ws") as ws:
        session_key = _ws_handshake(ws)
        _ws_send(ws, session_key, {"type": "runTask", "task_id": "t1", "task": "gen"})
        messages = []
        for _ in range(10):
            msg = _ws_recv(ws, session_key)
            messages.append(msg)
            if msg["type"] == "taskComplete":
                break
        types = [m["type"] for m in messages]
        assert "taskStarted" in types
        assert "taskDelta" in types
        assert "taskComplete" in types


def test_ws_control_ack():
    with client.websocket_connect("/ws") as ws:
        session_key = _ws_handshake(ws)
        _ws_send(ws, session_key, {"type": "control", "task_id": "t1", "action": "cancel"})
        data = _ws_recv(ws, session_key)
        assert data["type"] == "controlAck"
        assert data["action"] == "cancel"


def test_ws_unknown_type_returns_error():
    with client.websocket_connect("/ws") as ws:
        session_key = _ws_handshake(ws)
        _ws_send(ws, session_key, {"type": "bogus"})
        data = _ws_recv(ws, session_key)
        assert data["type"] == "error"


def test_ws_invalid_json_returns_error():
    with client.websocket_connect("/ws") as ws:
        session_key = _ws_handshake(ws)
        # Send a valid encrypted frame that decrypts to non-JSON bytes
        plaintext = b"not json!!"
        ws.send_text(base64.b64encode(encrypt_message(session_key, plaintext)).decode())
        data = _ws_recv(ws, session_key)
        assert data["type"] == "error"
        assert "Invalid JSON" in data["error"]
