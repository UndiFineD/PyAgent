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
"""Tests for the multimodal package (models, processor, top-level __init__)."""

from __future__ import annotations

import pytest

import multimodal
from multimodal.models import Modality, MultiModalData, MultiModalInputs
from multimodal.processor import (
    AudioProcessor,
    ImageProcessor,
    MultiModalProcessor,
    TextProcessor,
)


# ---------------------------------------------------------------------------
# Package importability
# ---------------------------------------------------------------------------

def test_multimodal_package_import() -> None:
    """Test that the multimodal package can be imported."""
    assert hasattr(multimodal, "__name__")
    assert multimodal.placeholder() is True


# ---------------------------------------------------------------------------
# Modality enum
# ---------------------------------------------------------------------------

def test_modality_values() -> None:
    assert Modality.TEXT
    assert Modality.IMAGE
    assert Modality.AUDIO
    assert Modality.VIDEO
    assert Modality.DOCUMENT


# ---------------------------------------------------------------------------
# MultiModalData
# ---------------------------------------------------------------------------

def test_text_data_is_text() -> None:
    d = MultiModalData(modality=Modality.TEXT, content="hello", mime_type="text/plain")
    assert d.is_text
    assert not d.is_binary
    assert d.as_text() == "hello"


def test_binary_data_is_binary() -> None:
    d = MultiModalData(modality=Modality.IMAGE, content=b"\x89PNG", mime_type="image/png")
    assert d.is_binary
    assert not d.is_text


def test_as_text_raises_for_non_utf8_binary() -> None:
    d = MultiModalData(modality=Modality.IMAGE, content=b"\xff\xfe", mime_type="image/png")
    with pytest.raises(ValueError, match="Cannot decode"):
        d.as_text()


def test_metadata_stored() -> None:
    d = MultiModalData(
        modality=Modality.IMAGE,
        content=b"data",
        mime_type="image/png",
        metadata={"width": 100, "height": 200},
    )
    assert d.metadata["width"] == 100
    assert d.metadata["height"] == 200


def test_embedding_stored() -> None:
    d = MultiModalData(modality=Modality.TEXT, content="hi", embedding=[0.1, 0.2, 0.3])
    assert d.embedding == [0.1, 0.2, 0.3]


# ---------------------------------------------------------------------------
# MultiModalInputs
# ---------------------------------------------------------------------------

def test_add_and_text_items() -> None:
    mi = MultiModalInputs()
    mi.add(MultiModalData(Modality.TEXT, "hello"))
    mi.add(MultiModalData(Modality.IMAGE, b"\x00\x01\x02", mime_type="image/png"))
    assert len(mi.text_items()) == 1
    assert len(mi.by_modality(Modality.IMAGE)) == 1


def test_to_prompt_parts_with_context() -> None:
    mi = MultiModalInputs(context="system context")
    mi.add(MultiModalData(Modality.TEXT, "user message"))
    parts = mi.to_prompt_parts()
    assert parts[0] == "system context"
    assert parts[1] == "user message"


def test_to_prompt_parts_binary_placeholder() -> None:
    mi = MultiModalInputs()
    mi.add(MultiModalData(Modality.IMAGE, b"\xff\xfe", mime_type="image/jpeg"))
    parts = mi.to_prompt_parts()
    assert "image/jpeg omitted" in parts[0]


def test_empty_inputs_no_context() -> None:
    mi = MultiModalInputs()
    assert mi.to_prompt_parts() == []


# ---------------------------------------------------------------------------
# Processor tests
# ---------------------------------------------------------------------------

def test_text_processor() -> None:
    proc = TextProcessor()
    d = MultiModalData(Modality.TEXT, "hi there")
    result = proc.process(d)
    assert result["type"] == "text"
    assert result["text"] == "hi there"


def test_image_processor_bytes() -> None:
    proc = ImageProcessor()
    d = MultiModalData(Modality.IMAGE, b"\x00\x01", mime_type="image/png")
    result = proc.process(d)
    assert result["type"] == "image_url"
    assert result["image_url"]["url"].startswith("data:image/png;base64,")


def test_image_processor_url_passthrough() -> None:
    proc = ImageProcessor()
    d = MultiModalData(Modality.IMAGE, "https://example.com/img.png", mime_type="image/png")
    result = proc.process(d)
    assert result["image_url"]["url"] == "https://example.com/img.png"


def test_audio_processor() -> None:
    proc = AudioProcessor()
    d = MultiModalData(Modality.AUDIO, b"\x01\x02\x03", mime_type="audio/mp3")
    result = proc.process(d)
    assert result["type"] == "audio"
    assert result["audio"]["mime_type"] == "audio/mp3"
    assert "data" in result["audio"]


def test_multimodal_processor_full_pipeline() -> None:
    proc = MultiModalProcessor()
    mi = MultiModalInputs(context="context string")
    mi.add(MultiModalData(Modality.TEXT, "text part"))
    mi.add(MultiModalData(Modality.IMAGE, b"\x89PNG", mime_type="image/png"))

    parts = proc.process(mi)
    types = [p["type"] for p in parts]
    assert types[0] == "text"   # context
    assert types[1] == "text"   # text item
    assert types[2] == "image_url"  # image item


def test_multimodal_processor_unsupported_modality() -> None:
    proc = MultiModalProcessor()
    d = MultiModalData(Modality.VIDEO, b"\x00", mime_type="video/mp4")
    result = proc.process_item(d)
    assert result["type"] == "text"
    assert "VIDEO" in result["text"]


def test_multimodal_processor_register_custom() -> None:
    class UpperTextProcessor:
        def process(self, data: MultiModalData) -> dict:
            return {"type": "text", "text": data.as_text().upper()}

    proc = MultiModalProcessor()
    proc.register(Modality.TEXT, UpperTextProcessor())
    d = MultiModalData(Modality.TEXT, "hello")
    result = proc.process_item(d)
    assert result["text"] == "HELLO"


def test_validate_returns_true() -> None:
    assert MultiModalProcessor.validate() is True
