# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
MultiModalProcessor - Unified multimodal input handling.

Inspired by vLLM's multimodal/processing/processor.py.
Provides image, video, audio, and text embedding processing with placeholder injection.
"""

from __future__ import annotations

import hashlib
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Generic,
    List,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    TypeVar,
    Union,
)

import numpy as np

if TYPE_CHECKING:
    try:
        from PIL import Image
    except ImportError:
        Image = Any  # type: ignore


logger = logging.getLogger(__name__)


# =============================================================================
# Enums and Configuration
# =============================================================================


class ModalityType(Enum):
    """Supported modality types for multimodal inputs."""
    
    IMAGE = auto()
    VIDEO = auto()
    AUDIO = auto()
    TEXT = auto()
    EMBEDS = auto()  # Pre-computed embeddings


@dataclass
class MultiModalConfig:
    """Configuration for multimodal processing.
    
    Inspired by vLLM's MultiModalConfig.
    
    Attributes:
        limit_per_prompt: Maximum items per modality per prompt.
        media_io_kwargs: Additional args for media loading (e.g., {"video": {"num_frames": 40}}).
        mm_processor_kwargs: Override processor arguments for each modality.
        trust_remote_code: Allow loading untrusted processor code.
        image_token: Token string for image placeholders.
        video_token: Token string for video placeholders.
        audio_token: Token string for audio placeholders.
    """
    
    limit_per_prompt: Dict[str, int] = field(default_factory=lambda: {
        "image": 8,
        "video": 1,
        "audio": 4,
    })
    media_io_kwargs: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    mm_processor_kwargs: Optional[Dict[str, Any]] = None
    trust_remote_code: bool = False
    
    # Placeholder tokens
    image_token: str = "<image>"
    video_token: str = "<video>"
    audio_token: str = "<audio>"
    
    def get_limit(self, modality: str) -> int:
        """Get item limit for a modality."""
        return self.limit_per_prompt.get(modality, 1)
    
    def get_media_kwargs(self, modality: str) -> Dict[str, Any]:
        """Get media IO kwargs for a modality."""
        return self.media_io_kwargs.get(modality, {})


# =============================================================================
# Data Classes for Multimodal Inputs
# =============================================================================


@dataclass
class PlaceholderInfo:
    """Information about a placeholder in the token sequence.
    
    Attributes:
        modality: Type of multimodal content.
        item_idx: Index of the item within this modality (0-indexed).
        start_idx: Starting position in token sequence.
        length: Number of placeholder tokens.
        is_embed: Boolean mask indicating which tokens are embeddings.
    """
    
    modality: ModalityType
    item_idx: int
    start_idx: int
    length: int
    is_embed: Optional[np.ndarray] = None  # Boolean mask
    
    @property
    def end_idx(self) -> int:
        """Ending position (exclusive) in token sequence."""
        return self.start_idx + self.length


@dataclass
class MultiModalData:
    """Raw multimodal data before processing.
    
    Attributes:
        images: List of PIL Images or numpy arrays (H, W, C).
        videos: List of video data as (frames, metadata) tuples.
        audios: List of (waveform, sample_rate) tuples.
        embeds: List of pre-computed embedding arrays.
    """
    
    images: List[Any] = field(default_factory=list)  # PIL.Image or np.ndarray
    videos: List[Tuple[np.ndarray, Dict[str, Any]]] = field(default_factory=list)
    audios: List[Tuple[np.ndarray, int]] = field(default_factory=list)
    embeds: List[np.ndarray] = field(default_factory=list)
    
    def is_empty(self) -> bool:
        """Check if no multimodal data is present."""
        return (
            len(self.images) == 0
            and len(self.videos) == 0
            and len(self.audios) == 0
            and len(self.embeds) == 0
        )
    
    def get_modality_count(self, modality: ModalityType) -> int:
        """Get count of items for a modality."""
        if modality == ModalityType.IMAGE:
            return len(self.images)
        elif modality == ModalityType.VIDEO:
            return len(self.videos)
        elif modality == ModalityType.AUDIO:
            return len(self.audios)
        elif modality == ModalityType.EMBEDS:
            return len(self.embeds)
        return 0


@dataclass
class MultiModalInputs:
    """Processed multimodal inputs ready for model consumption.
    
    Attributes:
        prompt_token_ids: Token IDs including placeholders.
        mm_embeddings: Dict mapping modality to list of embedding tensors.
        mm_placeholders: Dict mapping modality to list of PlaceholderInfo.
        mm_kwargs: Additional keyword arguments for model forward.
    """
    
    prompt_token_ids: List[int] = field(default_factory=list)
    mm_embeddings: Dict[str, List[np.ndarray]] = field(default_factory=dict)
    mm_placeholders: Dict[str, List[PlaceholderInfo]] = field(default_factory=dict)
    mm_kwargs: Dict[str, Any] = field(default_factory=dict)
    
    def has_multimodal(self) -> bool:
        """Check if any multimodal embeddings are present."""
        return any(len(embeds) > 0 for embeds in self.mm_embeddings.values())
    
    def get_placeholder_count(self) -> int:
        """Get total number of placeholder tokens."""
        return sum(
            sum(p.length for p in placeholders)
            for placeholders in self.mm_placeholders.values()
        )


# =============================================================================
# Base Processor
# =============================================================================

T = TypeVar("T")


class BaseMultiModalProcessor(ABC, Generic[T]):
    """Abstract base class for modality-specific processors.
    
    Subclasses implement processing logic for images, videos, audio, etc.
    Inspired by vLLM's BaseMultiModalProcessor.
    """
    
    modality: ModalityType
    
    def __init__(self, config: Optional[MultiModalConfig] = None):
        self.config = config or MultiModalConfig()
    
    @abstractmethod
    def process(
        self,
        data: T,
        **kwargs: Any,
    ) -> Tuple[np.ndarray, Dict[str, Any]]:
        """Process raw input data into embeddings.
        
        Args:
            data: Raw input data (image, video, audio, etc.).
            **kwargs: Additional processing arguments.
        
        Returns:
            Tuple of (embeddings, metadata).
        """
        ...
    
    @abstractmethod
    def get_placeholder_count(self, data: T, **kwargs: Any) -> int:
        """Get number of placeholder tokens needed for this input.
        
        Args:
            data: Raw input data.
            **kwargs: Additional arguments.
        
        Returns:
            Number of placeholder tokens to inject.
        """
        ...
    
    def compute_hash(self, data: T) -> str:
        """Compute content hash for caching.
        
        Args:
            data: Input data.
        
        Returns:
            Hex digest of content hash.
        """
        # Default implementation for numpy arrays
        if isinstance(data, np.ndarray):
            return hashlib.sha256(data.tobytes()).hexdigest()[:16]
        return hashlib.sha256(str(data).encode()).hexdigest()[:16]


# =============================================================================
# Image Processor
# =============================================================================


class ImageProcessor(BaseMultiModalProcessor[Any]):
    """Processor for image inputs.
    
    Handles PIL Images and numpy arrays, with resize and normalization.
    """
    
    modality = ModalityType.IMAGE
    
    def __init__(
        self,
        config: Optional[MultiModalConfig] = None,
        target_size: Tuple[int, int] = (224, 224),
        mean: Tuple[float, ...] = (0.485, 0.456, 0.406),
        std: Tuple[float, ...] = (0.229, 0.224, 0.225),
        patch_size: int = 14,
    ):
        super().__init__(config)
        self.target_size = target_size
        self.mean = np.array(mean).reshape(1, 1, 3)
        self.std = np.array(std).reshape(1, 1, 3)
        self.patch_size = patch_size
    
    def process(
        self,
        data: Any,
        **kwargs: Any,
    ) -> Tuple[np.ndarray, Dict[str, Any]]:
        """Process image to normalized embeddings.
        
        Args:
            data: PIL Image or numpy array (H, W, C).
            **kwargs: Override target_size, mean, std.
        
        Returns:
            Tuple of (normalized_image, metadata).
        """
        # Convert PIL to numpy if needed
        if hasattr(data, "convert"):
            # PIL Image
            data = data.convert("RGB")
            image_np = np.array(data, dtype=np.float32) / 255.0
        elif isinstance(data, np.ndarray):
            if data.dtype == np.uint8:
                image_np = data.astype(np.float32) / 255.0
            else:
                image_np = data.astype(np.float32)
        else:
            raise TypeError(f"Unsupported image type: {type(data)}")
        
        original_size = image_np.shape[:2]
        
        # Resize
        target = kwargs.get("target_size", self.target_size)
        image_resized = self._resize(image_np, target)
        
        # Normalize
        mean = kwargs.get("mean", self.mean)
        std = kwargs.get("std", self.std)
        image_normalized = (image_resized - mean) / std
        
        # Calculate grid size
        h, w = image_normalized.shape[:2]
        num_patches_h = h // self.patch_size
        num_patches_w = w // self.patch_size
        
        metadata = {
            "original_size": original_size,
            "processed_size": (h, w),
            "grid_hw": (num_patches_h, num_patches_w),
            "num_patches": num_patches_h * num_patches_w,
        }
        
        return image_normalized, metadata
    
    def get_placeholder_count(self, data: Any, **kwargs: Any) -> int:
        """Get number of visual tokens for this image."""
        target = kwargs.get("target_size", self.target_size)
        h, w = target
        num_patches_h = h // self.patch_size
        num_patches_w = w // self.patch_size
        return num_patches_h * num_patches_w
    
    def _resize(
        self,
        image: np.ndarray,
        target_size: Tuple[int, int],
    ) -> np.ndarray:
        """Resize image using bilinear interpolation.
        
        Simple numpy-based resize (for GPU, use rust_core acceleration).
        """
        src_h, src_w = image.shape[:2]
        tgt_h, tgt_w = target_size
        
        if (src_h, src_w) == (tgt_h, tgt_w):
            return image
        
        # Simple bilinear interpolation
        y_scale = src_h / tgt_h
        x_scale = src_w / tgt_w
        
        y_coords = np.arange(tgt_h) * y_scale
        x_coords = np.arange(tgt_w) * x_scale
        
        y0 = np.floor(y_coords).astype(int)
        x0 = np.floor(x_coords).astype(int)
        y1 = np.minimum(y0 + 1, src_h - 1)
        x1 = np.minimum(x0 + 1, src_w - 1)
        
        wy = (y_coords - y0).reshape(-1, 1, 1)
        wx = (x_coords - x0).reshape(1, -1, 1)
        
        result = (
            image[y0][:, x0] * (1 - wy) * (1 - wx)
            + image[y0][:, x1] * (1 - wy) * wx
            + image[y1][:, x0] * wy * (1 - wx)
            + image[y1][:, x1] * wy * wx
        )
        
        return result.astype(np.float32)


# =============================================================================
# Video Processor
# =============================================================================


class VideoProcessor(BaseMultiModalProcessor[Tuple[np.ndarray, Dict[str, Any]]]):
    """Processor for video inputs.
    
    Handles frame extraction with temporal sampling.
    """
    
    modality = ModalityType.VIDEO
    
    def __init__(
        self,
        config: Optional[MultiModalConfig] = None,
        num_frames: int = 8,
        target_size: Tuple[int, int] = (224, 224),
        patch_size: int = 14,
    ):
        super().__init__(config)
        self.num_frames = num_frames
        self.target_size = target_size
        self.patch_size = patch_size
        self.image_processor = ImageProcessor(
            config=config,
            target_size=target_size,
            patch_size=patch_size,
        )
    
    def process(
        self,
        data: Tuple[np.ndarray, Dict[str, Any]],
        **kwargs: Any,
    ) -> Tuple[np.ndarray, Dict[str, Any]]:
        """Process video to frame embeddings.
        
        Args:
            data: Tuple of (frames, metadata) where frames is (N, H, W, C).
            **kwargs: Override num_frames, target_size.
        
        Returns:
            Tuple of (processed_frames, metadata).
        """
        frames, meta = data
        num_frames = kwargs.get("num_frames", self.num_frames)
        
        # Temporal sampling
        total_frames = len(frames)
        if total_frames > num_frames:
            indices = np.linspace(0, total_frames - 1, num_frames, dtype=int)
            frames = frames[indices]
        elif total_frames < num_frames:
            # Pad with last frame
            padding = np.tile(frames[-1:], (num_frames - total_frames, 1, 1, 1))
            frames = np.concatenate([frames, padding], axis=0)
        
        # Process each frame
        processed_frames = []
        for frame in frames:
            processed, _ = self.image_processor.process(frame, **kwargs)
            processed_frames.append(processed)
        
        processed_array = np.stack(processed_frames, axis=0)
        
        # Calculate tokens per frame
        h, w = processed_array.shape[1:3]
        num_patches_h = h // self.patch_size
        num_patches_w = w // self.patch_size
        tokens_per_frame = num_patches_h * num_patches_w
        
        metadata = {
            "original_frames": total_frames,
            "sampled_frames": num_frames,
            "frame_size": (h, w),
            "grid_thw": (num_frames, num_patches_h, num_patches_w),
            "tokens_per_frame": tokens_per_frame,
            "total_tokens": num_frames * tokens_per_frame,
            "fps": meta.get("fps", 30),
        }
        
        return processed_array, metadata
    
    def get_placeholder_count(
        self,
        data: Tuple[np.ndarray, Dict[str, Any]],
        **kwargs: Any,
    ) -> int:
        """Get total visual tokens for this video."""
        num_frames = kwargs.get("num_frames", self.num_frames)
        h, w = self.target_size
        tokens_per_frame = (h // self.patch_size) * (w // self.patch_size)
        return num_frames * tokens_per_frame


# =============================================================================
# Audio Processor
# =============================================================================


class AudioProcessor(BaseMultiModalProcessor[Tuple[np.ndarray, int]]):
    """Processor for audio inputs.
    
    Handles waveform processing with sample rate conversion.
    """
    
    modality = ModalityType.AUDIO
    
    def __init__(
        self,
        config: Optional[MultiModalConfig] = None,
        target_sample_rate: int = 16000,
        max_length_seconds: float = 30.0,
        feature_size: int = 80,  # Mel bins
        hop_length: int = 160,
    ):
        super().__init__(config)
        self.target_sample_rate = target_sample_rate
        self.max_length_seconds = max_length_seconds
        self.feature_size = feature_size
        self.hop_length = hop_length
    
    def process(
        self,
        data: Tuple[np.ndarray, int],
        **kwargs: Any,
    ) -> Tuple[np.ndarray, Dict[str, Any]]:
        """Process audio waveform.
        
        Args:
            data: Tuple of (waveform, sample_rate).
            **kwargs: Override target_sample_rate, max_length_seconds.
        
        Returns:
            Tuple of (mel_features, metadata).
        """
        waveform, sample_rate = data
        target_sr = kwargs.get("target_sample_rate", self.target_sample_rate)
        max_len = kwargs.get("max_length_seconds", self.max_length_seconds)
        
        # Ensure 1D
        if waveform.ndim > 1:
            waveform = waveform.mean(axis=-1) if waveform.shape[-1] < waveform.shape[0] else waveform.mean(axis=0)
        
        # Resample if needed
        if sample_rate != target_sr:
            waveform = self._resample(waveform, sample_rate, target_sr)
            sample_rate = target_sr
        
        # Truncate to max length
        max_samples = int(max_len * sample_rate)
        original_length = len(waveform)
        if len(waveform) > max_samples:
            waveform = waveform[:max_samples]
        
        # Compute simple features (log mel spectrogram placeholder)
        # Real implementation would use librosa or torchaudio
        num_frames = max(1, len(waveform) // self.hop_length)
        features = np.zeros((num_frames, self.feature_size), dtype=np.float32)
        
        # Simple energy-based feature for testing
        for i in range(num_frames):
            start = i * self.hop_length
            end = min(start + self.hop_length * 2, len(waveform))
            segment = waveform[start:end]
            if len(segment) > 0:
                features[i, 0] = np.sqrt(np.mean(segment ** 2))  # RMS energy
        
        metadata = {
            "original_sample_rate": sample_rate,
            "original_length": original_length,
            "processed_length": len(waveform),
            "num_frames": num_frames,
            "feature_size": self.feature_size,
            "duration_seconds": len(waveform) / sample_rate,
        }
        
        return features, metadata
    
    def get_placeholder_count(
        self,
        data: Tuple[np.ndarray, int],
        **kwargs: Any,
    ) -> int:
        """Get audio token count based on duration."""
        waveform, sample_rate = data
        target_sr = kwargs.get("target_sample_rate", self.target_sample_rate)
        max_len = kwargs.get("max_length_seconds", self.max_length_seconds)
        
        # Estimate duration
        duration = min(len(waveform) / sample_rate, max_len)
        num_samples = int(duration * target_sr)
        num_frames = max(1, num_samples // self.hop_length)
        
        return num_frames
    
    def _resample(
        self,
        waveform: np.ndarray,
        src_rate: int,
        tgt_rate: int,
    ) -> np.ndarray:
        """Simple linear resampling."""
        if src_rate == tgt_rate:
            return waveform
        
        ratio = tgt_rate / src_rate
        new_length = int(len(waveform) * ratio)
        indices = np.arange(new_length) / ratio
        indices = np.clip(indices, 0, len(waveform) - 1)
        
        # Linear interpolation
        idx_floor = np.floor(indices).astype(int)
        idx_ceil = np.minimum(idx_floor + 1, len(waveform) - 1)
        weights = indices - idx_floor
        
        resampled = waveform[idx_floor] * (1 - weights) + waveform[idx_ceil] * weights
        return resampled.astype(np.float32)


# =============================================================================
# Text Embed Processor
# =============================================================================


class TextEmbedProcessor(BaseMultiModalProcessor[np.ndarray]):
    """Processor for pre-computed text embeddings."""
    
    modality = ModalityType.EMBEDS
    
    def process(
        self,
        data: np.ndarray,
        **kwargs: Any,
    ) -> Tuple[np.ndarray, Dict[str, Any]]:
        """Pass through pre-computed embeddings.
        
        Args:
            data: Pre-computed embedding array.
            **kwargs: Unused.
        
        Returns:
            Tuple of (embeddings, metadata).
        """
        if data.ndim == 1:
            data = data.reshape(1, -1)
        
        metadata = {
            "num_tokens": data.shape[0],
            "embed_dim": data.shape[1],
        }
        
        return data.astype(np.float32), metadata
    
    def get_placeholder_count(self, data: np.ndarray, **kwargs: Any) -> int:
        """Get number of embedding tokens."""
        if data.ndim == 1:
            return 1
        return data.shape[0]


# =============================================================================
# Registry
# =============================================================================


class MultiModalRegistry:
    """Central registry for multimodal processors.
    
    Inspired by vLLM's MULTIMODAL_REGISTRY.
    """
    
    def __init__(self):
        self._processors: Dict[ModalityType, BaseMultiModalProcessor] = {}
        self._default_config = MultiModalConfig()
    
    def register_processor(
        self,
        modality: ModalityType,
        processor: BaseMultiModalProcessor,
    ) -> None:
        """Register a processor for a modality."""
        self._processors[modality] = processor
        logger.debug("Registered processor for %s", modality.name)
    
    def get_processor(self, modality: ModalityType) -> Optional[BaseMultiModalProcessor]:
        """Get processor for a modality."""
        return self._processors.get(modality)
    
    def create_processor(
        self,
        modality: ModalityType,
        config: Optional[MultiModalConfig] = None,
    ) -> BaseMultiModalProcessor:
        """Create a new processor instance for a modality."""
        config = config or self._default_config
        
        if modality == ModalityType.IMAGE:
            return ImageProcessor(config=config)
        elif modality == ModalityType.VIDEO:
            return VideoProcessor(config=config)
        elif modality == ModalityType.AUDIO:
            return AudioProcessor(config=config)
        elif modality == ModalityType.EMBEDS:
            return TextEmbedProcessor(config=config)
        else:
            raise ValueError(f"Unsupported modality: {modality}")
    
    def process_inputs(
        self,
        mm_data: MultiModalData,
        config: Optional[MultiModalConfig] = None,
        **kwargs: Any,
    ) -> MultiModalInputs:
        """Process all multimodal inputs.
        
        Args:
            mm_data: Raw multimodal data.
            config: Processing configuration.
            **kwargs: Additional processing arguments.
        
        Returns:
            Processed multimodal inputs.
        """
        config = config or self._default_config
        result = MultiModalInputs()
        
        # Process images
        if mm_data.images:
            processor = self.create_processor(ModalityType.IMAGE, config)
            embeddings = []
            placeholders = []
            offset = 0
            
            for idx, image in enumerate(mm_data.images):
                if idx >= config.get_limit("image"):
                    logger.warning("Image limit reached, skipping remaining images")
                    break
                
                emb, meta = processor.process(image, **kwargs)
                num_tokens = processor.get_placeholder_count(image, **kwargs)
                
                embeddings.append(emb)
                placeholders.append(PlaceholderInfo(
                    modality=ModalityType.IMAGE,
                    item_idx=idx,
                    start_idx=offset,
                    length=num_tokens,
                ))
                offset += num_tokens
            
            result.mm_embeddings["image"] = embeddings
            result.mm_placeholders["image"] = placeholders
        
        # Process videos
        if mm_data.videos:
            processor = self.create_processor(ModalityType.VIDEO, config)
            embeddings = []
            placeholders = []
            offset = result.get_placeholder_count()
            
            for idx, video in enumerate(mm_data.videos):
                if idx >= config.get_limit("video"):
                    logger.warning("Video limit reached, skipping remaining videos")
                    break
                
                emb, meta = processor.process(video, **kwargs)
                num_tokens = meta.get("total_tokens", processor.get_placeholder_count(video, **kwargs))
                
                embeddings.append(emb)
                placeholders.append(PlaceholderInfo(
                    modality=ModalityType.VIDEO,
                    item_idx=idx,
                    start_idx=offset,
                    length=num_tokens,
                ))
                offset += num_tokens
            
            result.mm_embeddings["video"] = embeddings
            result.mm_placeholders["video"] = placeholders
        
        # Process audios
        if mm_data.audios:
            processor = self.create_processor(ModalityType.AUDIO, config)
            embeddings = []
            placeholders = []
            offset = result.get_placeholder_count()
            
            for idx, audio in enumerate(mm_data.audios):
                if idx >= config.get_limit("audio"):
                    logger.warning("Audio limit reached, skipping remaining audios")
                    break
                
                emb, meta = processor.process(audio, **kwargs)
                num_tokens = meta.get("num_frames", processor.get_placeholder_count(audio, **kwargs))
                
                embeddings.append(emb)
                placeholders.append(PlaceholderInfo(
                    modality=ModalityType.AUDIO,
                    item_idx=idx,
                    start_idx=offset,
                    length=num_tokens,
                ))
                offset += num_tokens
            
            result.mm_embeddings["audio"] = embeddings
            result.mm_placeholders["audio"] = placeholders
        
        # Process pre-computed embeds
        if mm_data.embeds:
            processor = self.create_processor(ModalityType.EMBEDS, config)
            embeddings = []
            placeholders = []
            offset = result.get_placeholder_count()
            
            for idx, embed in enumerate(mm_data.embeds):
                emb, meta = processor.process(embed, **kwargs)
                num_tokens = meta.get("num_tokens", 1)
                
                embeddings.append(emb)
                placeholders.append(PlaceholderInfo(
                    modality=ModalityType.EMBEDS,
                    item_idx=idx,
                    start_idx=offset,
                    length=num_tokens,
                ))
                offset += num_tokens
            
            result.mm_embeddings["embeds"] = embeddings
            result.mm_placeholders["embeds"] = placeholders
        
        return result


# Global registry instance
MULTIMODAL_REGISTRY = MultiModalRegistry()


# =============================================================================
# Convenience Functions
# =============================================================================


def process_multimodal_inputs(
    mm_data: MultiModalData,
    config: Optional[MultiModalConfig] = None,
    **kwargs: Any,
) -> MultiModalInputs:
    """Process multimodal inputs using the global registry.
    
    Args:
        mm_data: Raw multimodal data.
        config: Optional processing configuration.
        **kwargs: Additional processing arguments.
    
    Returns:
        Processed multimodal inputs.
    """
    return MULTIMODAL_REGISTRY.process_inputs(mm_data, config, **kwargs)


def get_placeholder_tokens(
    mm_inputs: MultiModalInputs,
    modality: str,
    token_id: int,
) -> List[int]:
    """Generate placeholder token IDs for a modality.
    
    Args:
        mm_inputs: Processed multimodal inputs.
        modality: Modality name ("image", "video", "audio").
        token_id: Token ID to use as placeholder.
    
    Returns:
        List of placeholder token IDs.
    """
    placeholders = mm_inputs.mm_placeholders.get(modality, [])
    total_tokens = sum(p.length for p in placeholders)
    return [token_id] * total_tokens
