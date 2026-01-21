# Copyright (c) 2026 PyAgent Authors. All rights reserved.
# Phase 40: Media IO Engine Tests

"""
Tests for MediaIOEngine - unified media loading.
"""

import pytest
import asyncio
import inspect
import numpy as np
from pathlib import Path
from typing import List

from src.infrastructure.services.mediaio import (
    MediaType,
    ImageFormat,
    VideoFormat,
    AudioFormat,
    ResizeMode,
    MediaMetadata,
    ImageData,
    VideoData,
    AudioData,
    MediaLoadConfig,
    MediaLoader,
    ImageLoader,
    VideoLoader,
    AudioLoader,
    MediaIOEngine,
    create_media_engine,
    load_image,
    load_video,
    load_audio,
)


class TestEnums:
    """Test enum values."""
    
    def test_media_type_values(self):
        """Test MediaType enum."""
        assert MediaType.IMAGE is not None
        assert MediaType.VIDEO is not None
        assert MediaType.AUDIO is not None
        assert MediaType.DOCUMENT is not None
    
    def test_image_format_values(self):
        """Test ImageFormat enum."""
        assert ImageFormat.JPEG is not None
        assert ImageFormat.PNG is not None
        assert ImageFormat.WEBP is not None
        assert ImageFormat.GIF is not None
    
    def test_video_format_values(self):
        """Test VideoFormat enum."""
        assert VideoFormat.MP4 is not None
        assert VideoFormat.WEBM is not None
        assert VideoFormat.AVI is not None
    
    def test_audio_format_values(self):
        """Test AudioFormat enum."""
        assert AudioFormat.WAV is not None
        assert AudioFormat.MP3 is not None
        assert AudioFormat.FLAC is not None
    
    def test_resize_mode_values(self):
        """Test ResizeMode enum."""
        assert ResizeMode.CROP is not None
        assert ResizeMode.PAD is not None
        assert ResizeMode.STRETCH is not None
        assert ResizeMode.SHORTEST is not None


class TestMediaMetadata:
    """Test MediaMetadata dataclass."""
    
    def test_create_image_metadata(self):
        """Test creating image metadata."""
        meta = MediaMetadata(
            media_type=MediaType.IMAGE,
            format=ImageFormat.JPEG,
            width=640,
            height=480,
            channels=3,
        )
        
        assert meta.media_type == MediaType.IMAGE
        assert meta.width == 640
        assert meta.height == 480
    
    def test_create_video_metadata(self):
        """Test creating video metadata."""
        meta = MediaMetadata(
            media_type=MediaType.VIDEO,
            format=VideoFormat.MP4,
            width=1920,
            height=1080,
            duration=30.0,
            frame_count=900,
        )
        
        assert meta.duration == 30.0
        assert meta.frame_count == 900
    
    def test_create_audio_metadata(self):
        """Test creating audio metadata."""
        meta = MediaMetadata(
            media_type=MediaType.AUDIO,
            format=AudioFormat.WAV,
            duration=5.0,
            sample_rate=16000,
        )
        
        assert meta.sample_rate == 16000


class TestImageData:
    """Test ImageData dataclass."""
    
    def test_create_image_data(self):
        """Test creating ImageData."""
        data = np.random.randn(480, 640, 3).astype(np.float32)
        meta = MediaMetadata(
            media_type=MediaType.IMAGE,
            format=ImageFormat.PNG,
            width=640,
            height=480,
        )
        
        img = ImageData(data=data, metadata=meta, source="test.png")
        
        assert img.width == 640
        assert img.height == 480
        assert img.shape == (480, 640, 3)
    
    def test_batch_image_data(self):
        """Test batch ImageData."""
        data = np.random.randn(4, 224, 224, 3).astype(np.float32)
        meta = MediaMetadata(
            media_type=MediaType.IMAGE,
            format=ImageFormat.JPEG,
        )
        
        img = ImageData(data=data, metadata=meta, source="batch")
        
        assert img.shape[0] == 4


class TestVideoData:
    """Test VideoData dataclass."""
    
    def test_create_video_data(self):
        """Test creating VideoData."""
        frames = np.random.randn(32, 224, 224, 3).astype(np.float32)
        meta = MediaMetadata(
            media_type=MediaType.VIDEO,
            format=VideoFormat.MP4,
            frame_count=32,
        )
        
        video = VideoData(frames=frames, metadata=meta, source="test.mp4")
        
        assert video.frame_count == 32
    
    def test_video_with_timestamps(self):
        """Test VideoData with timestamps."""
        frames = np.random.randn(10, 224, 224, 3).astype(np.float32)
        timestamps = np.linspace(0, 1, 10)
        meta = MediaMetadata(
            media_type=MediaType.VIDEO,
            format=VideoFormat.MP4,
        )
        
        video = VideoData(
            frames=frames,
            metadata=meta,
            source="test.mp4",
            timestamps=timestamps,
        )
        
        assert len(video.timestamps) == 10


class TestAudioData:
    """Test AudioData dataclass."""
    
    def test_create_audio_data(self):
        """Test creating AudioData."""
        waveform = np.random.randn(16000).astype(np.float32)
        meta = MediaMetadata(
            media_type=MediaType.AUDIO,
            format=AudioFormat.WAV,
            sample_rate=16000,
        )
        
        audio = AudioData(waveform=waveform, metadata=meta, source="test.wav")
        
        assert audio.duration == 1.0  # 16000 samples / 16000 Hz
    
    def test_stereo_audio(self):
        """Test stereo AudioData."""
        waveform = np.random.randn(2, 16000).astype(np.float32)
        meta = MediaMetadata(
            media_type=MediaType.AUDIO,
            format=AudioFormat.WAV,
            sample_rate=16000,
            channels=2,
        )
        
        audio = AudioData(waveform=waveform, metadata=meta, source="stereo.wav")
        
        assert audio.waveform.shape[0] == 2


class TestMediaLoadConfig:
    """Test MediaLoadConfig dataclass."""
    
    def test_default_config(self):
        """Test default config."""
        config = MediaLoadConfig()
        
        assert config.normalize is True
        assert config.max_frames == 32
        assert config.target_sample_rate == 16000
    
    def test_custom_config(self):
        """Test custom config."""
        config = MediaLoadConfig(
            target_size=(224, 224),
            resize_mode=ResizeMode.CROP,
            normalize=True,
            max_frames=64,
            use_gpu_decode=False,
        )
        
        assert config.target_size == (224, 224)
        assert config.max_frames == 64
    
    def test_clip_normalization(self):
        """Test CLIP normalization values."""
        config = MediaLoadConfig()
        
        # Default should be CLIP values
        assert len(config.mean) == 3
        assert len(config.std) == 3


class TestImageLoader:
    """Test ImageLoader class."""
    
    def test_create_loader(self):
        """Test creating loader."""
        loader = ImageLoader()
        assert loader is not None
    
    def test_supports_image(self):
        """Test supports image type."""
        loader = ImageLoader()
        
        assert loader.supports(MediaType.IMAGE) is True
        assert loader.supports(MediaType.VIDEO) is False
    
    @pytest.mark.asyncio
    async def test_load_bytes(self):
        """Test loading from bytes."""
        loader = ImageLoader()
        config = MediaLoadConfig()
        
        # Create minimal PNG bytes (1x1 red pixel)
        # This is a valid 1x1 PNG
        png_data = bytes([
            0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A,  # PNG signature
            # ... minimal valid PNG would be needed here
        ])
        
        # Just test that the loader exists and method is callable
        # Actual loading would require valid image bytes
        assert hasattr(loader, 'load')


class TestVideoLoader:
    """Test VideoLoader class."""
    
    def test_create_loader(self):
        """Test creating loader."""
        loader = VideoLoader()
        assert loader is not None
    
    def test_supports_video(self):
        """Test supports video type."""
        loader = VideoLoader()
        
        assert loader.supports(MediaType.VIDEO) is True
        assert loader.supports(MediaType.IMAGE) is False


class TestAudioLoader:
    """Test AudioLoader class."""
    
    def test_create_loader(self):
        """Test creating loader."""
        loader = AudioLoader()
        assert loader is not None
    
    def test_supports_audio(self):
        """Test supports audio type."""
        loader = AudioLoader()
        
        assert loader.supports(MediaType.AUDIO) is True
        assert loader.supports(MediaType.IMAGE) is False


class TestMediaIOEngine:
    """Test MediaIOEngine class."""
    
    def test_create_engine(self):
        """Test creating engine."""
        engine = MediaIOEngine()
        assert engine is not None
    
    def test_create_with_config(self):
        """Test creating engine with config."""
        config = MediaLoadConfig(
            target_size=(224, 224),
            normalize=True,
        )
        engine = MediaIOEngine(config)
        
        assert engine.config.target_size == (224, 224)
    
    def test_register_loader(self):
        """Test registering custom loader."""
        engine = MediaIOEngine()
        
        class CustomLoader(MediaLoader):
            def supports(self, media_type):
                return media_type == MediaType.DOCUMENT
            
            async def load(self, source, config):
                return None
        
        engine.register_loader(MediaType.DOCUMENT, CustomLoader())
        
        # Should not raise
        assert True
    
    def test_detect_media_type(self):
        """Test media type detection."""
        engine = MediaIOEngine()
        
        assert engine._detect_media_type("test.jpg") == MediaType.IMAGE
        assert engine._detect_media_type("test.png") == MediaType.IMAGE
        assert engine._detect_media_type("test.mp4") == MediaType.VIDEO
        assert engine._detect_media_type("test.wav") == MediaType.AUDIO
    
    def test_compute_cache_key(self):
        """Test cache key computation."""
        engine = MediaIOEngine()
        
        key1 = engine._compute_cache_key("image.jpg", MediaType.IMAGE)
        key2 = engine._compute_cache_key("image.jpg", MediaType.IMAGE)
        key3 = engine._compute_cache_key("other.jpg", MediaType.IMAGE)
        
        assert key1 == key2
        assert key1 != key3
    
    def test_clear_cache(self):
        """Test clearing cache."""
        engine = MediaIOEngine()
        
        engine.clear_cache()
        
        # Should not raise
        assert True
    
    @pytest.mark.asyncio
    async def test_load_batch(self):
        """Test batch loading."""
        engine = MediaIOEngine()
        
        # Just verify the method exists and is async
        assert inspect.iscoroutinefunction(engine.load_batch)


class TestFactoryFunctions:
    """Test factory functions."""
    
    def test_create_media_engine(self):
        """Test create_media_engine."""
        engine = create_media_engine(
            target_size=(224, 224),
            normalize=True,
            use_gpu=False,
        )
        
        assert engine is not None
        assert engine.config.target_size == (224, 224)
    
    def test_create_default_engine(self):
        """Test creating default engine."""
        engine = create_media_engine()
        
        assert engine is not None
    
    @pytest.mark.asyncio
    async def test_load_image_function(self):
        """Test load_image convenience function."""
        # Just verify the function is async
        assert inspect.iscoroutinefunction(load_image)
    
    @pytest.mark.asyncio
    async def test_load_video_function(self):
        """Test load_video convenience function."""
        assert inspect.iscoroutinefunction(load_video)
    
    @pytest.mark.asyncio
    async def test_load_audio_function(self):
        """Test load_audio convenience function."""
        assert inspect.iscoroutinefunction(load_audio)


class TestResizeModes:
    """Test different resize modes."""
    
    def test_resize_mode_crop(self):
        """Test crop resize mode."""
        config = MediaLoadConfig(
            target_size=(224, 224),
            resize_mode=ResizeMode.CROP,
        )
        
        assert config.resize_mode == ResizeMode.CROP
    
    def test_resize_mode_pad(self):
        """Test pad resize mode."""
        config = MediaLoadConfig(
            target_size=(224, 224),
            resize_mode=ResizeMode.PAD,
        )
        
        assert config.resize_mode == ResizeMode.PAD
    
    def test_resize_mode_stretch(self):
        """Test stretch resize mode."""
        config = MediaLoadConfig(
            target_size=(224, 224),
            resize_mode=ResizeMode.STRETCH,
        )
        
        assert config.resize_mode == ResizeMode.STRETCH


# Run pytest if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
