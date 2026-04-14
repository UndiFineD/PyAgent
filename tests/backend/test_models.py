#!/usr/bin/env python3
"""Tests for backend.models module — WebSocket message schema validation."""
from __future__ import annotations

import pytest
from pydantic import ValidationError

from backend.models import (
    InitMessage,
    RunTaskMessage,
    ControlMessage,
    SpeechTranscriptMessage,
    SignalMessage,
    TaskStartedMessage,
    TaskDeltaMessage,
    TaskCompleteMessage,
    TaskErrorMessage,
    ActionRequestMessage,
)


class TestInitMessage:
    """Tests for InitMessage model."""

    def test_init_message_valid(self):
        """Test creating a valid InitMessage."""
        msg = InitMessage(
            type="init",
            session_id="sess-123",
            client_info={"platform": "web", "version": "1.0"},
        )
        assert msg.type == "init"
        assert msg.session_id == "sess-123"
        assert msg.client_info["platform"] == "web"

    def test_init_message_minimal(self):
        """Test InitMessage with minimal required fields."""
        msg = InitMessage(type="init", session_id="sess-456")
        assert msg.type == "init"
        assert msg.session_id == "sess-456"
        assert msg.client_info == {}

    def test_init_message_invalid_type(self):
        """Test InitMessage rejects invalid type."""
        with pytest.raises(ValidationError):
            InitMessage(type="invalid", session_id="sess-789")

    def test_init_message_missing_session_id(self):
        """Test InitMessage requires session_id."""
        with pytest.raises(ValidationError):
            InitMessage(type="init")

    def test_init_message_empty_session_id(self):
        """Test InitMessage accepts empty string as session_id."""
        msg = InitMessage(type="init", session_id="")
        assert msg.session_id == ""


class TestRunTaskMessage:
    """Tests for RunTaskMessage model."""

    def test_run_task_message_valid(self):
        """Test creating a valid RunTaskMessage."""
        msg = RunTaskMessage(
            type="runTask",
            task_id="task-123",
            task="analyze_data",
            payload={"file": "data.csv"},
        )
        assert msg.type == "runTask"
        assert msg.task_id == "task-123"
        assert msg.task == "analyze_data"
        assert msg.payload["file"] == "data.csv"

    def test_run_task_message_minimal(self):
        """Test RunTaskMessage with minimal fields."""
        msg = RunTaskMessage(type="runTask", task_id="t-1", task="test")
        assert msg.type == "runTask"
        assert msg.task_id == "t-1"
        assert msg.task == "test"
        assert msg.payload == {}

    def test_run_task_message_invalid_type(self):
        """Test RunTaskMessage rejects invalid type."""
        with pytest.raises(ValidationError):
            RunTaskMessage(
                type="runFoo",
                task_id="task-1",
                task="test",
            )

    def test_run_task_message_missing_task_id(self):
        """Test RunTaskMessage requires task_id."""
        with pytest.raises(ValidationError):
            RunTaskMessage(type="runTask", task="test")

    def test_run_task_message_missing_task(self):
        """Test RunTaskMessage requires task."""
        with pytest.raises(ValidationError):
            RunTaskMessage(type="runTask", task_id="task-1")

    def test_run_task_message_nested_payload(self):
        """Test RunTaskMessage with complex nested payload."""
        payload = {
            "config": {
                "model": "gpt-4",
                "params": {"temperature": 0.7, "max_tokens": 2000},
            },
            "inputs": ["a", "b", "c"],
        }
        msg = RunTaskMessage(
            type="runTask", task_id="task-1", task="inference", payload=payload
        )
        assert msg.payload["config"]["model"] == "gpt-4"
        assert msg.payload["inputs"] == ["a", "b", "c"]


class TestControlMessage:
    """Tests for ControlMessage model."""

    def test_control_message_cancel(self):
        """Test creating a cancel ControlMessage."""
        msg = ControlMessage(type="control", task_id="task-123", action="cancel")
        assert msg.type == "control"
        assert msg.task_id == "task-123"
        assert msg.action == "cancel"

    def test_control_message_pause(self):
        """Test creating a pause ControlMessage."""
        msg = ControlMessage(type="control", task_id="task-456", action="pause")
        assert msg.action == "pause"

    def test_control_message_resume(self):
        """Test creating a resume ControlMessage."""
        msg = ControlMessage(type="control", task_id="task-789", action="resume")
        assert msg.action == "resume"

    def test_control_message_invalid_action(self):
        """Test ControlMessage rejects invalid action."""
        with pytest.raises(ValidationError):
            ControlMessage(type="control", task_id="task-1", action="restart")

    def test_control_message_missing_action(self):
        """Test ControlMessage requires action."""
        with pytest.raises(ValidationError):
            ControlMessage(type="control", task_id="task-1")

    @pytest.mark.parametrize("action", ["cancel", "pause", "resume"])
    def test_control_message_all_actions(self, action):
        """Test all valid control actions."""
        msg = ControlMessage(type="control", task_id="task-1", action=action)
        assert msg.action == action


class TestSpeechTranscriptMessage:
    """Tests for SpeechTranscriptMessage model."""

    def test_speech_transcript_message_valid(self):
        """Test creating a valid SpeechTranscriptMessage."""
        msg = SpeechTranscriptMessage(
            type="speechTranscript",
            task_id="task-123",
            transcript="hello world",
            is_final=True,
        )
        assert msg.type == "speechTranscript"
        assert msg.task_id == "task-123"
        assert msg.transcript == "hello world"
        assert msg.is_final is True

    def test_speech_transcript_message_partial(self):
        """Test SpeechTranscriptMessage with partial transcript."""
        msg = SpeechTranscriptMessage(
            type="speechTranscript",
            transcript="hello",
            is_final=False,
        )
        assert msg.transcript == "hello"
        assert msg.is_final is False
        assert msg.task_id is None

    def test_speech_transcript_message_missing_transcript(self):
        """Test SpeechTranscriptMessage requires transcript."""
        with pytest.raises(ValidationError):
            SpeechTranscriptMessage(type="speechTranscript", is_final=True)

    def test_speech_transcript_message_empty_transcript(self):
        """Test SpeechTranscriptMessage accepts empty transcript."""
        msg = SpeechTranscriptMessage(
            type="speechTranscript",
            transcript="",
            is_final=True,
        )
        assert msg.transcript == ""

    def test_speech_transcript_message_defaults(self):
        """Test SpeechTranscriptMessage default values."""
        msg = SpeechTranscriptMessage(
            type="speechTranscript",
            transcript="test",
        )
        assert msg.is_final is True
        assert msg.task_id is None


class TestSignalMessage:
    """Tests for SignalMessage model."""

    def test_signal_message_offer(self):
        """Test creating a signal message with offer."""
        msg = SignalMessage(
            type="signal",
            session_id="sess-123",
            peer_id="peer-456",
            signal_type="offer",
            payload={"sdp": "v=0\no=..."},
        )
        assert msg.type == "signal"
        assert msg.session_id == "sess-123"
        assert msg.peer_id == "peer-456"
        assert msg.signal_type == "offer"
        assert msg.payload["sdp"].startswith("v=0")

    def test_signal_message_answer(self):
        """Test creating a signal message with answer."""
        msg = SignalMessage(
            type="signal",
            session_id="sess-1",
            peer_id="peer-1",
            signal_type="answer",
            payload={"sdp": "v=0"},
        )
        assert msg.signal_type == "answer"

    def test_signal_message_ice(self):
        """Test creating a signal message with ICE candidate."""
        msg = SignalMessage(
            type="signal",
            session_id="sess-1",
            peer_id="peer-1",
            signal_type="ice",
            payload={"candidate": "candidate:...", "sdpMLineIndex": 0},
        )
        assert msg.signal_type == "ice"

    def test_signal_message_invalid_signal_type(self):
        """Test SignalMessage rejects invalid signal type."""
        with pytest.raises(ValidationError):
            SignalMessage(
                type="signal",
                session_id="sess-1",
                peer_id="peer-1",
                signal_type="invalid",
                payload={},
            )

    @pytest.mark.parametrize("signal_type", ["offer", "answer", "ice"])
    def test_signal_message_all_types(self, signal_type):
        """Test all valid signal types."""
        msg = SignalMessage(
            type="signal",
            session_id="sess-1",
            peer_id="peer-1",
            signal_type=signal_type,
            payload={},
        )
        assert msg.signal_type == signal_type


class TestTaskStartedMessage:
    """Tests for TaskStartedMessage model."""

    def test_task_started_message_valid(self):
        """Test creating a valid TaskStartedMessage."""
        msg = TaskStartedMessage(
            task_id="task-123",
            started_at="2024-01-01T12:00:00Z",
        )
        assert msg.type == "taskStarted"
        assert msg.task_id == "task-123"
        assert msg.started_at == "2024-01-01T12:00:00Z"

    def test_task_started_message_type_default(self):
        """Test TaskStartedMessage type defaults to 'taskStarted'."""
        msg = TaskStartedMessage(
            task_id="task-1",
            started_at="2024-01-01T00:00:00Z",
        )
        assert msg.type == "taskStarted"

    def test_task_started_message_invalid_type(self):
        """Test TaskStartedMessage rejects invalid type."""
        with pytest.raises(ValidationError):
            TaskStartedMessage(
                type="invalid",
                task_id="task-1",
                started_at="2024-01-01T00:00:00Z",
            )


class TestTaskDeltaMessage:
    """Tests for TaskDeltaMessage model."""

    def test_task_delta_message_valid(self):
        """Test creating a valid TaskDeltaMessage."""
        msg = TaskDeltaMessage(
            task_id="task-123",
            delta="Processing...",
            meta={"step": 1, "progress": 0.5},
        )
        assert msg.type == "taskDelta"
        assert msg.task_id == "task-123"
        assert msg.delta == "Processing..."
        assert msg.meta["step"] == 1

    def test_task_delta_message_minimal(self):
        """Test TaskDeltaMessage with minimal fields."""
        msg = TaskDeltaMessage(task_id="task-1", delta="data")
        assert msg.type == "taskDelta"
        assert msg.meta == {}

    def test_task_delta_message_empty_delta(self):
        """Test TaskDeltaMessage accepts empty delta."""
        msg = TaskDeltaMessage(task_id="task-1", delta="")
        assert msg.delta == ""


class TestTaskCompleteMessage:
    """Tests for TaskCompleteMessage model."""

    def test_task_complete_message_success(self):
        """Test creating a successful TaskCompleteMessage."""
        msg = TaskCompleteMessage(
            task_id="task-123",
            result={"output": "done", "count": 42},
            status="success",
        )
        assert msg.type == "taskComplete"
        assert msg.task_id == "task-123"
        assert msg.status == "success"
        assert msg.result["output"] == "done"

    def test_task_complete_message_error_status(self):
        """Test TaskCompleteMessage with error status."""
        msg = TaskCompleteMessage(
            task_id="task-1",
            result={"error": "Something went wrong"},
            status="error",
        )
        assert msg.status == "error"

    def test_task_complete_message_default_status(self):
        """Test TaskCompleteMessage defaults status to 'success'."""
        msg = TaskCompleteMessage(task_id="task-1", result={})
        assert msg.status == "success"

    def test_task_complete_message_invalid_status(self):
        """Test TaskCompleteMessage rejects invalid status."""
        with pytest.raises(ValidationError):
            TaskCompleteMessage(
                task_id="task-1",
                result={},
                status="pending",
            )


class TestTaskErrorMessage:
    """Tests for TaskErrorMessage model."""

    def test_task_error_message_valid(self):
        """Test creating a valid TaskErrorMessage."""
        msg = TaskErrorMessage(
            task_id="task-123",
            error="Operation failed",
            code="TIMEOUT",
        )
        assert msg.type == "taskError"
        assert msg.task_id == "task-123"
        assert msg.error == "Operation failed"
        assert msg.code == "TIMEOUT"

    def test_task_error_message_default_code(self):
        """Test TaskErrorMessage defaults code to 'UNKNOWN'."""
        msg = TaskErrorMessage(task_id="task-1", error="Error occurred")
        assert msg.code == "UNKNOWN"

    def test_task_error_message_minimal(self):
        """Test TaskErrorMessage with minimal fields."""
        msg = TaskErrorMessage(task_id="task-1", error="Failed")
        assert msg.type == "taskError"
        assert msg.code == "UNKNOWN"

    @pytest.mark.parametrize(
        "code",
        [
            "TIMEOUT",
            "NOT_FOUND",
            "PERMISSION_DENIED",
            "INTERNAL_ERROR",
            "UNKNOWN",
        ],
    )
    def test_task_error_message_codes(self, code):
        """Test various error codes."""
        msg = TaskErrorMessage(task_id="task-1", error="Error", code=code)
        assert msg.code == code


class TestActionRequestMessage:
    """Tests for ActionRequestMessage model."""

    def test_action_request_message_valid(self):
        """Test creating a valid ActionRequestMessage."""
        msg = ActionRequestMessage(
            action="navigate",
            params={"url": "https://example.com"},
            task_id="task-123",
        )
        assert msg.type == "actionRequest"
        assert msg.action == "navigate"
        assert msg.params["url"] == "https://example.com"
        assert msg.task_id == "task-123"

    def test_action_request_message_no_task_id(self):
        """Test ActionRequestMessage without task_id."""
        msg = ActionRequestMessage(
            action="notification",
            params={"message": "Done"},
        )
        assert msg.action == "notification"
        assert msg.task_id is None

    def test_action_request_message_minimal(self):
        """Test ActionRequestMessage with minimal fields."""
        msg = ActionRequestMessage(action="refresh")
        assert msg.type == "actionRequest"
        assert msg.action == "refresh"
        assert msg.params == {}

    def test_action_request_message_complex_params(self):
        """Test ActionRequestMessage with complex nested params."""
        params = {
            "viewport": {"width": 1920, "height": 1080},
            "options": {"timeout": 30, "retry": True},
            "selectors": ["#btn-submit", ".error-msg"],
        }
        msg = ActionRequestMessage(action="screenshot", params=params)
        assert msg.params["viewport"]["width"] == 1920
        assert msg.params["options"]["retry"] is True


class TestMessageSerialization:
    """Tests for message serialization and deserialization."""

    def test_init_message_dict_roundtrip(self):
        """Test InitMessage dict serialization roundtrip."""
        original = InitMessage(
            type="init",
            session_id="sess-1",
            client_info={"version": "1.0"},
        )
        msg_dict = original.model_dump()
        restored = InitMessage(**msg_dict)
        assert restored.session_id == original.session_id

    def test_run_task_message_json_roundtrip(self):
        """Test RunTaskMessage JSON roundtrip."""
        original = RunTaskMessage(
            type="runTask",
            task_id="task-1",
            task="compute",
            payload={"x": 10},
        )
        json_str = original.model_dump_json()
        restored = RunTaskMessage.model_validate_json(json_str)
        assert restored.task_id == original.task_id
        assert restored.payload["x"] == 10

    def test_task_complete_message_dict_roundtrip(self):
        """Test TaskCompleteMessage dict roundtrip."""
        original = TaskCompleteMessage(
            task_id="task-1",
            result={"status": "ok", "data": [1, 2, 3]},
            status="success",
        )
        msg_dict = original.model_dump()
        restored = TaskCompleteMessage(**msg_dict)
        assert restored.result["data"] == [1, 2, 3]

    def test_complex_message_json_preservation(self):
        """Test that JSON serialization preserves complex structures."""
        msg = ActionRequestMessage(
            action="complex_action",
            params={
                "nested": {
                    "array": [1, 2, 3],
                    "object": {"key": "value"},
                    "null_value": None,
                },
                "numbers": [1.5, 2.7],
                "booleans": [True, False],
            },
            task_id="task-1",
        )
        json_str = msg.model_dump_json()
        restored = ActionRequestMessage.model_validate_json(json_str)
        assert restored.params["nested"]["object"]["key"] == "value"
        assert restored.params["numbers"] == [1.5, 2.7]


class TestMessageFieldValidation:
    """Tests for field-level validation."""

    def test_message_type_immutable_behavior(self):
        """Test that message types are correct."""
        messages = [
            (InitMessage(type="init", session_id="s"), "init"),
            (RunTaskMessage(type="runTask", task_id="t", task="x"), "runTask"),
            (ControlMessage(type="control", task_id="t", action="cancel"), "control"),
            (
                SpeechTranscriptMessage(type="speechTranscript", transcript="x"),
                "speechTranscript",
            ),
            (
                SignalMessage(
                    type="signal",
                    session_id="s",
                    peer_id="p",
                    signal_type="offer",
                    payload={},
                ),
                "signal",
            ),
            (TaskStartedMessage(task_id="t", started_at="2024-01-01"), "taskStarted"),
            (TaskDeltaMessage(task_id="t", delta="x"), "taskDelta"),
            (TaskCompleteMessage(task_id="t", result={}), "taskComplete"),
            (TaskErrorMessage(task_id="t", error="x"), "taskError"),
            (ActionRequestMessage(action="x"), "actionRequest"),
        ]

        for msg, expected_type in messages:
            assert msg.type == expected_type

    def test_extra_fields_are_ignored(self):
        """Test that Pydantic ignores extra fields by default."""
        # Pydantic will ignore extra fields
        data = {"type": "init", "session_id": "s", "extra_field": "ignored"}
        msg = InitMessage(**data)
        assert msg.session_id == "s"
        assert not hasattr(msg, "extra_field")
