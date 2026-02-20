#!/usr/bin/env python3
"""Minimal AITalkingHead core for tests."""
from __future__ import annotations



try:
    from dataclasses import dataclass
except ImportError:
    from dataclasses import dataclass

try:
    from typing import Optional, Dict, Any
except ImportError:
    from typing import Optional, Dict, Any



@dataclass
class TalkingHeadRequest:
    text: str
    voice: Optional[str] = None


@dataclass
class TalkingHeadResult:
    video_url: str
    duration: float


@dataclass
class FaceAlignmentResult:
    landmarks: Dict[str, Any]


@dataclass
class AudioFeatures:
    sample_rate: int = 16000
    channels: int = 1


class AITalkingHeadCore:
    def __init__(self) -> None:
        self.active_models: Dict[str, Any] = {}

    def synthesize(self, request: TalkingHeadRequest) -> TalkingHeadResult:
        return TalkingHeadResult(video_url="", duration=0.0)


__all__ = [
    "TalkingHeadRequest",
    "TalkingHeadResult",
    "FaceAlignmentResult",
    "AudioFeatures",
    "AITalkingHeadCore",
]
