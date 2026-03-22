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
"""Multimodal processing pipeline for PyAgent.

Provides the ``MultiModalProcessor`` — a pluggable pipeline that converts
raw MultiModalData items into representations suitable for LLM ingestion.
"""

from __future__ import annotations

import base64
import logging
from typing import Any, Protocol

from .models import Modality, MultiModalData, MultiModalInputs

logger = logging.getLogger(__name__)


class ModalityProcessor(Protocol):
    """Protocol for per-modality processor plugins."""

    def process(self, data: MultiModalData) -> dict[str, Any]:
        """Process a single MultiModalData item and return a structured dict."""
        ...


class TextProcessor:
    """Processor for TEXT modality — wraps text into a standard dict."""

    def process(self, data: MultiModalData) -> dict[str, Any]:
        return {"type": "text", "text": data.as_text()}


class ImageProcessor:
    """Processor for IMAGE modality — base64-encodes bytes and returns a data-URI."""

    def process(self, data: MultiModalData) -> dict[str, Any]:
        if isinstance(data.content, bytes):
            b64 = base64.b64encode(data.content).decode("ascii")
            uri = f"data:{data.mime_type};base64,{b64}"
        else:
            uri = data.content  # already a URL or data URI
        return {"type": "image_url", "image_url": {"url": uri}}


class AudioProcessor:
    """Processor for AUDIO modality — base64-encodes and annotates MIME type."""

    def process(self, data: MultiModalData) -> dict[str, Any]:
        if isinstance(data.content, bytes):
            b64 = base64.b64encode(data.content).decode("ascii")
            return {"type": "audio", "audio": {"data": b64, "mime_type": data.mime_type}}
        return {"type": "audio", "audio": {"url": data.content, "mime_type": data.mime_type}}


class MultiModalProcessor:
    """Processing pipeline that converts MultiModalInputs into LLM-ready message parts.

    By default, a ``TextProcessor``, ``ImageProcessor``, and ``AudioProcessor``
    are registered.  Additional processors can be added via :meth:`register`.

    Parameters
    ----------
    processors:
        Optional mapping from :class:`Modality` to a custom processor.  Overrides
        defaults for any modality provided.
    """

    _DEFAULT_PROCESSORS: dict[Modality, ModalityProcessor] = {
        Modality.TEXT: TextProcessor(),
        Modality.IMAGE: ImageProcessor(),
        Modality.AUDIO: AudioProcessor(),
    }

    def __init__(
        self,
        processors: dict[Modality, ModalityProcessor] | None = None,
    ) -> None:
        self._processors: dict[Modality, ModalityProcessor] = dict(self._DEFAULT_PROCESSORS)
        if processors:
            self._processors.update(processors)

    def register(self, modality: Modality, processor: ModalityProcessor) -> None:
        """Register or replace the processor for *modality*."""
        self._processors[modality] = processor

    def process_item(self, data: MultiModalData) -> dict[str, Any]:
        """Process a single :class:`MultiModalData` item.

        Falls back to a text placeholder for unsupported modalities.
        """
        proc = self._processors.get(data.modality)
        if proc is None:
            logger.warning("No processor for modality %s; using text fallback", data.modality.name)
            return {"type": "text", "text": f"[{data.modality.name} not supported]"}
        return proc.process(data)

    def process(self, inputs: MultiModalInputs) -> list[dict[str, Any]]:
        """Process all items in *inputs* and return a list of LLM message parts.

        The optional ``inputs.context`` is prepended as a plain text part.
        """
        parts: list[dict[str, Any]] = []
        if inputs.context:
            parts.append({"type": "text", "text": inputs.context})
        parts.extend(self.process_item(item) for item in inputs.items)
        return parts

    @staticmethod
    def validate() -> bool:
        """Return True — confirms the processor module is importable."""
        return True
