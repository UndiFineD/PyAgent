#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Unit tests for Phase 51: Multimedia & Attention.

import pytest
import numpy as np
from src.core.base.common.multimodal_core import MultimodalCore, MultimodalStreamSession
from src.infrastructure.engine.multimodal.muxer import Muxer
from src.infrastructure.engine.multimodal.quantized_engine import QuantizedMultimediaEngine

def test_muxer_binary_sync():
    muxer = Muxer()
    audio = b"\x01\x02\x03\x04"
    video = b"\x05\x06\x07\x08"
    text = "Hello Phase 51"
    
    packet = muxer.synchronize_tick(audio, video, text)
    
    # Check Magic Header (0xDEADBEEF in Little Endian is EF BE AD DE)
    assert packet.startswith(b"\xef\xbe\xad\xde")
    assert len(packet) > 12 # Header + lengths + some data

def test_ia3_scaling_fallback():
    engine = QuantizedMultimediaEngine(mode="FP8")
    activations = np.ones((1, 10), dtype=np.float32)
    scaling = np.array([2.0] * 10, dtype=np.float32)
    
    # Simple Python fallback check
    result = engine.apply_stream_ia3(activations, scaling)
    assert np.allclose(result, 2.0)

def test_multimodal_core_initialization():
    core = MultimodalCore()
    assert core.muxer is not None
    assert core.q_engine is not None
    assert "Audio" in core.active_channels

def test_cross_modal_alignment_logic():
    engine = QuantizedMultimediaEngine()
    # Mock some features
    video_feat = np.random.rand(5, 128).astype(np.float32)
    audio_feat = np.random.rand(5, 128).astype(np.float32)
    
    # Should work (returns range if Rust not compiled, or aligned indices if it is)
    alignment = engine.align_streams(video_feat, audio_feat)
    assert len(alignment) == 5

@pytest.mark.asyncio
async def test_tensorrt_loader_stub():
    from src.infrastructure.engine.multimodal.tensorrt_loader import TensorRTLoader
    loader = TensorRTLoader()
    # Should return False for nonexistent engine but not crash
    success = await loader.load_engine("dummy_model")
    assert success is False
