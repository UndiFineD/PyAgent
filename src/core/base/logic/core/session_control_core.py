#!/usr/bin/env python3
"""Session Control Core - minimal parser-safe implementation."""
from __future__ import annotations

import enum
import json
from pathlib import Path
from typing import Optional


class SessionSignal(enum.Enum):
    RUNNING = "running"
    PAUSE = "pause"
    STOP = "stop"
    RESUME = "resume"


class SessionControlCore:
    def __init__(self, storage_dir: str = "data/agent_cache/sessions") -> None:
        self.storage_path = Path(storage_dir)
        self.storage_path.mkdir(parents=True, exist_ok=True)

    def _get_signal_file(self, session_id: str) -> Path:
        return self.storage_path / f"{session_id}_signal.json"

    def set_signal(self, session_id: str, signal: SessionSignal) -> None:
        file_path = self._get_signal_file(session_id)
        data = {"signal": signal.value, "session_id": session_id}
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f)

    def get_signal(self, session_id: str) -> SessionSignal:
        file_path = self._get_signal_file(session_id)
        if not file_path.exists():
            return SessionSignal.RUNNING
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return SessionSignal(data.get("signal", "running"))
        except (json.JSONDecodeError, ValueError):
            return SessionSignal.RUNNING

    def check_interrupt(self, session_id: str) -> bool:
        return self.get_signal(session_id) == SessionSignal.STOP

    def check_pause(self, session_id: str) -> bool:
        return self.get_signal(session_id) == SessionSignal.PAUSE
