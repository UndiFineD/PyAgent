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
"""Multimodal data models for PyAgent.

Defines the core data structures for representing multimodal content
(text, image, audio) and metadata in a unified format suitable for
LLM ingestion and agent processing.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any


class Modality(Enum):
    """Supported input/output modalities."""

    TEXT = auto()
    IMAGE = auto()
    AUDIO = auto()
    VIDEO = auto()
    DOCUMENT = auto()


@dataclass
class MultiModalData:
    """A single piece of multimodal content with metadata.

    Attributes
    ----------
    modality:
        The type of content (TEXT, IMAGE, AUDIO, etc.).
    content:
        Raw content.  For text, a ``str``.  For binary media, ``bytes``.
    mime_type:
        MIME type string (e.g. ``"text/plain"``, ``"image/png"``).
    metadata:
        Arbitrary key/value metadata (e.g. width, height, duration).
    embedding:
        Optional vector embedding representation.
    """

    modality: Modality
    content: str | bytes
    mime_type: str = "text/plain"
    metadata: dict[str, Any] = field(default_factory=dict)
    embedding: list[float] | None = None

    @property
    def is_text(self) -> bool:
        """Return True if this data item contains text content."""
        return self.modality is Modality.TEXT

    @property
    def is_binary(self) -> bool:
        """Return True if this data item contains binary content."""
        return isinstance(self.content, bytes)

    def as_text(self) -> str:
        """Return content as a string.

        Raises
        ------
        ValueError
            If the content is binary and cannot be trivially decoded.
        """
        if isinstance(self.content, str):
            return self.content
        try:
            return self.content.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(
                f"Cannot decode binary {self.mime_type!r} content as UTF-8"
            ) from exc


@dataclass
class MultiModalInputs:
    """Container for a collection of multimodal data items.

    Used to pass a set of inputs (e.g. a prompt image + a text question)
    to an agent or LLM endpoint as a single structured payload.

    Attributes
    ----------
    items:
        The list of :class:`MultiModalData` items.
    context:
        Optional free-form context string prepended to the prompt.
    """

    items: list[MultiModalData] = field(default_factory=list)
    context: str = ""

    def add(self, item: MultiModalData) -> None:
        """Append a data item to the inputs."""
        self.items.append(item)

    def text_items(self) -> list[MultiModalData]:
        """Return only the TEXT modality items."""
        return [i for i in self.items if i.modality is Modality.TEXT]

    def by_modality(self, modality: Modality) -> list[MultiModalData]:
        """Return all items matching the given modality."""
        return [i for i in self.items if i.modality is modality]

    def to_prompt_parts(self) -> list[str]:
        """Flatten all text-representable items into a list of strings.

        Non-UTF-8 binary items are replaced with a ``[<mime_type> omitted]``
        placeholder.
        """
        parts: list[str] = []
        if self.context:
            parts.append(self.context)
        parts.extend(_item_to_text(item) for item in self.items)
        return parts


def _item_to_text(item: MultiModalData) -> str:
    """Convert a single MultiModalData item to its text representation."""
    try:
        return item.as_text()
    except ValueError:
        return f"[{item.mime_type} omitted]"
