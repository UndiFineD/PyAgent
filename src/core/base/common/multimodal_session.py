#!/usr/bin/env python3
from __future__ import annotations

"""Minimal, parser-safe multimodal session shims used for tests."""
from typing import Any, Callable, Dict, List, Optional
from pathlib import Path


class MultimodalSession:
    def __init__(self, session_id: Optional[str] = None, storage_dir: Optional[Path] = None) -> None:
        self.session_id = session_id or "session-unknown"
        self.storage_dir = Path(storage_dir) if storage_dir else Path.cwd()
        self.state: Dict[str, Any] = {}

    def get(self, key: str) -> Any:
        return self.state.get(key)

    def set(self, key: str, value: Any) -> None:
        self.state[key] = value


class MultimodalStreamSession:
    """Lightweight manager for multimodal sessions used in tests."""

    def __init__(self, core: Any) -> None:
        self.core = core
        self.channels: Dict[str, str] = dict(getattr(core, "active_channels", {"Audio": "default"}))
        self.input_history: List[Dict[str, Any]] = []
        self.output_history: List[Dict[str, Any]] = []
        self.modificators: List[Callable[[List[Dict[str, Any]]], List[Dict[str, Any]]]] = []

    def add_modificator(self, mod: Callable[[List[Dict[str, Any]]], List[Dict[str, Any]]]) -> None:
        self.modificators.append(mod)

    def process_input_frame(self, audio: List[float], image: Optional[bytes] = None, **_: Any) -> Dict[str, Any]:
        result: Dict[str, Any] = {"audio_features": [], "vision_deltas": None}
        if hasattr(self.core, "calculate_audio_features"):
            result["audio_features"] = self.core.calculate_audio_features(audio)
        self.input_history.append(result)
        return result

    def filter_response(self, raw_stream: str) -> List[Dict[str, Any]]:
        fragments: List[Dict[str, Any]] = []
        if hasattr(self.core, "parse_stream"):
            fragments = self.core.parse_stream(raw_stream)
        else:
            fragments = [{"type": "text", "content": raw_stream}]

        for mod in self.modificators:
            fragments = mod(fragments)

        self.output_history.extend(fragments)
        return fragments
