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


from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Protocol, Union, runtime_checkable


@runtime_checkable
class TokenizerLike(Protocol):
    """
    Protocol for tokenizer abstraction.
    """


    def encode(self, text: str, **kwargs) -> List[int]:
        """Encode text to token IDs.
        
        Args:
            text: Input text to tokenize.
            **kwargs: Additional tokenizer-specific parameters (e.g., add_special_tokens, 
                     return_tensors, padding, truncation).
        
        Returns:
            List of integer token IDs representing the encoded text.
        """
        pass


    def decode(
        self,
        token_ids: Union[int, List[int]],
        skip_special_tokens: bool = True,
        **kwargs,
    ) -> str:
        """Decode token IDs to text."""
        pass


    def convert_ids_to_tokens(
        self,
        ids: Union[int, List[int]],
    ) -> Union[str, List[str]]:
        """Convert token IDs to token strings."""
        pass


    def convert_tokens_to_ids(
        self,
        tokens: Union[str, List[str]],
    ) -> Union[int, List[int]]:
        """Convert token strings to token IDs."""
        pass


    @property
    def vocab(self) -> Dict[str, int]:
        """Get the vocabulary mapping."""
        pass


    @property
    def eos_token_id(self) -> Optional[int]:
        """Get the end-of-sequence token ID."""
        pass


@dataclass
class DetokenizeResult:
    """
    Result of incremental detokenization.
    """

    new_text: str
    full_text: str
    prefix_offset: int = 0
    read_offset: int = 0
    finished: bool = False
    stop_reason: Optional[Union[str, int]] = None

    @property
    def has_new_text(self) -> bool:
        """Check if there is new text."""
        return bool(self.new_text)


class Modality(Enum):
    """Enum for different data modalities supported by multimodal tokenizers."""
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"


@dataclass
class MultimodalToken:
    """Representation of a token from any modality in a unified token space."""
    
    token_id: int
    modality: Modality
    embedding: Optional[List[float]] = None
    
    @property
    def is_text_token(self) -> bool:
        """Check if this is a text token."""
        return self.modality == Modality.TEXT
    
    @property
    def is_image_token(self) -> bool:
        """Check if this is an image token."""
        return self.modality == Modality.IMAGE
    
    @property
    def is_audio_token(self) -> bool:
        """Check if this is an audio token."""
        return self.modality == Modality.AUDIO
    
    @property
    def is_video_token(self) -> bool:
        """Check if this is a video token."""
        return self.modality == Modality.VIDEO


@dataclass
class MultimodalTokenizedData:
    """Result of multimodal tokenization with unified token IDs and metadata."""
    
    token_ids: List[int]
    modality_sequence: List[Modality]
    tokens: List[MultimodalToken]
    metadata: Dict[str, any] = None
    
    @property
    def num_tokens(self) -> int:
        """Get total number of tokens."""
        return len(self.token_ids)
    
    @property
    def text_token_count(self) -> int:
        """Count text tokens."""
        return sum(1 for mod in self.modality_sequence if mod == Modality.TEXT)
    
    @property
    def image_token_count(self) -> int:
        """Count image tokens."""
        return sum(1 for mod in self.modality_sequence if mod == Modality.IMAGE)
    
    @property
    def audio_token_count(self) -> int:
        """Count audio tokens."""
        return sum(1 for mod in self.modality_sequence if mod == Modality.AUDIO)


class MultimodalTokenizer:
    """
    Unified tokenizer for multimodal data (text, images, audio, video).
    
    Uses a unified token vocabulary across all modalities:
    - Text tokens: 0-30000 (using SentencePiece/BPE)
    - Image tokens: 30001-60000 (using VQVAE/CLIP patch tokenization)
    - Audio tokens: 60001-90000 (using Wav2Vec2/HuBERT)
    - Video tokens: 90001-120000 (combining image + audio tokens)
    
    Example:
        >>> tokenizer = MultimodalTokenizer()
        >>> result = tokenizer.encode_multimodal(
        ...     text="Hello world",
        ...     image_patches=[[...], [...]]  # List of patch embeddings
        ... )
        >>> print(result.token_ids)
        [101, 2054, 1010, 30001, 30002, ...]
    """
    
    # Token ID ranges for each modality (unified token space)
    TEXT_TOKEN_START = 0
    TEXT_TOKEN_END = 30000
    IMAGE_TOKEN_START = 30001
    IMAGE_TOKEN_END = 60000
    AUDIO_TOKEN_START = 60001
    AUDIO_TOKEN_END = 90000
    VIDEO_TOKEN_START = 90001
    VIDEO_TOKEN_END = 120000
    
    def __init__(
        self,
        text_tokenizer: Optional[TokenizerLike] = None,
        image_tokenizer: Optional[TokenizerLike] = None,
        audio_tokenizer: Optional[TokenizerLike] = None,
    ):
        """
        Initialize multimodal tokenizer with modality-specific tokenizers.
        
        Args:
            text_tokenizer: Tokenizer for text (e.g., SentencePiece, BPE).
                           If None, simple whitespace tokenization is used.
            image_tokenizer: Tokenizer for image patches (e.g., VQVAE).
                           If None, patches are left as-is.
            audio_tokenizer: Tokenizer for audio (e.g., Wav2Vec2, HuBERT).
                           If None, audio frames are left as-is.
        """
        self.text_tokenizer = text_tokenizer
        self.image_tokenizer = image_tokenizer
        self.audio_tokenizer = audio_tokenizer
    
    def encode_text(self, text: str) -> List[int]:
        """
        Encode text to token IDs in text token range (0-30000).
        
        Args:
            text: Text to tokenize.
        
        Returns:
            List of text token IDs.
        """
        if self.text_tokenizer:
            return self.text_tokenizer.encode(text)
        # Fallback: simple whitespace tokenization
        return [hash(token) % self.TEXT_TOKEN_END for token in text.split()]
    
    def encode_image_patches(self, patches: List[List[float]]) -> List[int]:
        """
        Encode image patches to token IDs in image token range (30001-60000).
        
        Args:
            patches: List of image patches (e.g., from ViT or CLIP).
        
        Returns:
            List of image token IDs.
        """
        token_ids = []
        for idx, patch in enumerate(patches):
            # Map patch index to image token range
            patch_token_id = self.IMAGE_TOKEN_START + (idx % (self.IMAGE_TOKEN_END - self.IMAGE_TOKEN_START))
            token_ids.append(patch_token_id)
        return token_ids
    
    def encode_audio(self, audio_frames: List[List[float]]) -> List[int]:
        """
        Encode audio frames to token IDs in audio token range (60001-90000).
        
        Args:
            audio_frames: List of audio frames (e.g., from Wav2Vec2).
        
        Returns:
            List of audio token IDs.
        """
        if self.audio_tokenizer:
            # Assumes audio_tokenizer can handle frame lists
            base_ids = self.audio_tokenizer.encode(str(audio_frames))
            # Remap to audio token range
            return [self.AUDIO_TOKEN_START + (tid % (self.AUDIO_TOKEN_END - self.AUDIO_TOKEN_START)) 
                    for tid in base_ids]
        
        # Fallback: use frame indices
        token_ids = []
        for idx, frame in enumerate(audio_frames):
            frame_token_id = self.AUDIO_TOKEN_START + (idx % (self.AUDIO_TOKEN_END - self.AUDIO_TOKEN_START))
            token_ids.append(frame_token_id)
        return token_ids
    
    def encode_multimodal(
        self,
        text: Optional[str] = None,
        image_patches: Optional[List[List[float]]] = None,
        audio_frames: Optional[List[List[float]]] = None,
    ) -> MultimodalTokenizedData:
        """
        Encode multimodal data into a unified token sequence.
        
        Args:
            text: Text content to encode.
            image_patches: Image patches from vision model.
            audio_frames: Audio frames from audio model.
        
        Returns:
            MultimodalTokenizedData with unified token IDs and modality sequence.
        
        Example:
            >>> tokenizer = MultimodalTokenizer()
            >>> result = tokenizer.encode_multimodal(
            ...     text="Describe this image",
            ...     image_patches=[[0.1, 0.2, ...], [0.3, 0.4, ...]]
            ... )
            >>> print(f"Total tokens: {result.num_tokens}")
            >>> print(f"Text tokens: {result.text_token_count}")
        """
        token_ids = []
        modality_sequence = []
        tokens = []
        metadata = {}
        
        # Encode text
        if text:
            text_token_ids = self.encode_text(text)
            token_ids.extend(text_token_ids)
            modality_sequence.extend([Modality.TEXT] * len(text_token_ids))
            tokens.extend([
                MultimodalToken(token_id=tid, modality=Modality.TEXT) 
                for tid in text_token_ids
            ])
            metadata['text_length'] = len(text)
        
        # Encode images
        if image_patches:
            image_token_ids = self.encode_image_patches(image_patches)
            token_ids.extend(image_token_ids)
            modality_sequence.extend([Modality.IMAGE] * len(image_token_ids))
            tokens.extend([
                MultimodalToken(token_id=tid, modality=Modality.IMAGE) 
                for tid in image_token_ids
            ])
            metadata['num_image_patches'] = len(image_patches)
        
        # Encode audio
        if audio_frames:
            audio_token_ids = self.encode_audio(audio_frames)
            token_ids.extend(audio_token_ids)
            modality_sequence.extend([Modality.AUDIO] * len(audio_token_ids))
            tokens.extend([
                MultimodalToken(token_id=tid, modality=Modality.AUDIO) 
                for tid in audio_token_ids
            ])
            metadata['num_audio_frames'] = len(audio_frames)
        
        return MultimodalTokenizedData(
            token_ids=token_ids,
            modality_sequence=modality_sequence,
            tokens=tokens,
            metadata=metadata,
        )
