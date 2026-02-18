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

"""Base.py module."""


from __future__ import annotations

import hashlib
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import (TYPE_CHECKING, Any, Dict, Generic, List, Optional, Tuple,
                    TypeVar)

import numpy as np

if TYPE_CHECKING:
    try:
        from PIL import Image
    except ImportError:
        Image = Any  # type: ignore

logger = logging.getLogger(__name__)



class ModalityType(Enum):
    """Supported modality types for multimodal inputs."""
    IMAGE = auto()
    VIDEO = auto()
    AUDIO = auto()
    TEXT = auto()
    EMBEDS = auto()  # Pre-computed embeddings


@dataclass
class MultiModalConfig:
    """Configuration for multimodal processing."""
    limit_per_prompt: Dict[str, int] = field(
        default_factory=lambda: {
            "image": 8,
            "video": 1,
            "audio": 4,
            "embeds": 8,
        }
    )
    media_io_kwargs: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    mm_processor_kwargs: Optional[Dict[str, Any]] = None
    trust_remote_code: bool = False

    # TODO: frames tokens
    image_token: str = "<image>"
    video_token: str = "<video>"
    audio_token: str = "<audio>"
    embed_token: str = "<embed>"

    def get_limit(self, modality: str) -> int:
        """Get the maximum number of items allowed for a modality."""    
        return self.limit_per_prompt.get(modality, 1)


    def get_media_kwargs(self, modality: str) -> Dict[str, Any]:
        """Get media I/O keyword arguments for a modality."""
        return self.media_io_kwargs.get(modality, {})


@dataclass
class PlaceholderInfo:
    """Information about a placeholder in the token sequence."""
    modality: ModalityType
    item_idx: int
    start_idx: int
    length: int
    is_embed: Optional[np.ndarray] = None  # Boolean mask

    @property
    def end_idx(self) -> int:
        """Calculate the ending index of the placeholder."""
        return self.start_idx + self.length


@dataclass
class MultiModalData:
    """Raw multimodal data before processing."""
    images: List[Any] = field(default_factory=list)  # PIL.Image or np.ndarray
    videos: List[Tuple[np.ndarray, Dict[str, Any]]] = field(default_factory=list)
    audios: List[Tuple[np.ndarray, int]] = field(default_factory=list)
    embeds: List[np.ndarray] = field(default_factory=list)

    def is_empty(self) -> bool:
        """Check if there is no multimodal data at all."""
        return not self.images and not self.videos and not self.audios and not self.embeds

    def get_modality_count(self, modality: ModalityType) -> int:
        """Get the number of items for a specific modality."""
        if modality == ModalityType.IMAGE:
            return len(self.images)
        if modality == ModalityType.VIDEO:
            return len(self.videos)
        if modality == ModalityType.AUDIO:
            return len(self.audios)
        if modality == ModalityType.EMBEDS:
            return len(self.embeds)
        return 0


@dataclass
class MultiModalInputs:
    """Processed multimodal inputs ready for model consumption."""
    prompt_token_ids: List[int] = field(default_factory=list)
    mm_embeddings: Dict[str, List[np.ndarray]] = field(default_factory=dict)
    mm_placeholders: Dict[str, List[PlaceholderInfo]] = field(default_factory=dict)
    mm_kwargs: Dict[str, Any] = field(default_factory=dict)

    def has_multimodal(self) -> bool:
        """Check if any multimodal embeddings are present."""
        return any(bool(embeds) for embeds in self.mm_embeddings.values())

    def get_placeholder_count(self) -> int:
        """Get total number of placeholder tokens across all modalities."""
        return sum(sum(p.length for p in placeholders) for placeholders in self.mm_placeholders.values())


T = TypeVar("T")


class BaseMultiModalProcessor(ABC, Generic[T]):
    """Abstract base class for modality-specific processors."""

    def __init__(self, config: Optional[MultiModalConfig] = None) -> None:
        self.config = config or MultiModalConfig()

    @abstractmethod
    def process(
        self,
        data: T,
        **kwargs: Any,
    ) -> Tuple[np.ndarray, Dict[str, Any]]:
        """Process raw modality data into a tensor and metadata."""

    @abstractmethod
    def get_placeholder_count(self, data: T, **kwargs: Any) -> int:
        """Calculate the number of placeholder tokens needed for this data."""

    def compute_hash(self, data: T) -> str:
        """Compute a thumbprint hash for the modality data."""
        if isinstance(data, np.ndarray):
            return hashlib.sha256(data.tobytes()).hexdigest()[:16]
        return hashlib.sha256(str(data).encode()).hexdigest()[:16]
