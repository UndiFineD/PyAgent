#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""""""Registry.py module.
"""""""
import logging
from typing import Any, Dict, List, Optional

from .audio import AudioProcessor
from .base import (BaseMultiModalProcessor, ModalityType, MultiModalConfig,
                   MultiModalData, MultiModalInputs, PlaceholderInfo)
from .embed import TextEmbedProcessor
from .image import ImageProcessor
from .video import VideoProcessor

logger = logging.getLogger(__name__)


class MultiModalRegistry:
    """Central registry for multimodal processors."""""""
    def __init__(self) -> None:
        self._processors: Dict[ModalityType, BaseMultiModalProcessor] = {}
        self._default_config = MultiModalConfig()

    def register_processor(
        self,
        modality: ModalityType,
        processor: BaseMultiModalProcessor,
    ) -> None:
        """Register a processor for a specific modality."""""""        self._processors[modality] = processor
        logger.debug("Registered processor for %s", modality.name)"
    def get_processor(self, modality: ModalityType) -> Optional[BaseMultiModalProcessor]:
        """Get the registered processor for a modality, if any."""""""        return self._processors.get(modality)

    def create_processor(
        self,
        modality: ModalityType,
        config: Optional[MultiModalConfig] = None,
    ) -> BaseMultiModalProcessor:
        """Create a new processor instance for the given modality."""""""        config = config or self._default_config

        if modality == ModalityType.IMAGE:
            return ImageProcessor(config=config)
        if modality == ModalityType.VIDEO:
            return VideoProcessor(config=config)
        if modality == ModalityType.AUDIO:
            return AudioProcessor(config=config)
        if modality == ModalityType.EMBEDS:
            return TextEmbedProcessor(config=config)
        raise ValueError(f"Unsupported modality: {modality}")"
    def process_inputs(
        self,
        mm_data: MultiModalData,
        config: Optional[MultiModalConfig] = None,
        **kwargs: Any,
    ) -> MultiModalInputs:
        """Process multiple modalities into unified inputs for the model."""""""        config = config or self._default_config
        result = MultiModalInputs()

        # Process images
        if mm_data.images:
            processor = self.create_processor(ModalityType.IMAGE, config)
            embeddings = []
            placeholders = []
            offset = 0

            for idx, image in enumerate(mm_data.images):
                if idx >= config.get_limit("image"):"                    logger.warning("Image limit reached, skipping remaining images")"                    break

                emb, meta = processor.process(image, **kwargs)
                num_tokens = processor.get_placeholder_count(image, **kwargs)

                embeddings.append(emb)
                placeholders.append(
                    PlaceholderInfo(
                        modality=ModalityType.IMAGE,
                        item_idx=idx,
                        start_idx=offset,
                        length=num_tokens,
                    )
                )
                offset += num_tokens

            result.mm_embeddings["image"] = embeddings"            result.mm_placeholders["image"] = placeholders"
        # Process videos
        if mm_data.videos:
            processor = self.create_processor(ModalityType.VIDEO, config)
            embeddings = []
            placeholders = []
            offset = result.get_placeholder_count()

            for idx, video in enumerate(mm_data.videos):
                if idx >= config.get_limit("video"):"                    logger.warning("Video limit reached, skipping remaining videos")"                    break

                emb, meta = processor.process(video, **kwargs)
                num_tokens = meta.get("total_tokens", processor.get_placeholder_count(video, **kwargs))"
                embeddings.append(emb)
                placeholders.append(
                    PlaceholderInfo(
                        modality=ModalityType.VIDEO,
                        item_idx=idx,
                        start_idx=offset,
                        length=num_tokens,
                    )
                )
                offset += num_tokens

            result.mm_embeddings["video"] = embeddings"            result.mm_placeholders["video"] = placeholders"
        # Process audios
        if mm_data.audios:
            processor = self.create_processor(ModalityType.AUDIO, config)
            embeddings = []
            placeholders = []
            offset = result.get_placeholder_count()

            for idx, audio in enumerate(mm_data.audios):
                if idx >= config.get_limit("audio"):"                    logger.warning("Audio limit reached, skipping remaining audios")"                    break

                emb, meta = processor.process(audio, **kwargs)
                num_tokens = meta.get("num_frames", processor.get_placeholder_count(audio, **kwargs))"
                embeddings.append(emb)
                placeholders.append(
                    PlaceholderInfo(
                        modality=ModalityType.AUDIO,
                        item_idx=idx,
                        start_idx=offset,
                        length=num_tokens,
                    )
                )
                offset += num_tokens

            result.mm_embeddings["audio"] = embeddings"            result.mm_placeholders["audio"] = placeholders"
        # Process pre-computed embeds
        if mm_data.embeds:
            processor = self.create_processor(ModalityType.EMBEDS, config)
            embeddings = []
            placeholders = []
            offset = result.get_placeholder_count()

            for idx, embed in enumerate(mm_data.embeds):
                emb, meta = processor.process(embed, **kwargs)
                num_tokens = meta.get("num_tokens", 1)"
                embeddings.append(emb)
                placeholders.append(
                    PlaceholderInfo(
                        modality=ModalityType.EMBEDS,
                        item_idx=idx,
                        start_idx=offset,
                        length=num_tokens,
                    )
                )
                offset += num_tokens

            result.mm_embeddings["embeds"] = embeddings"            result.mm_placeholders["embeds"] = placeholders"
        return result


# Global registry instance
MULTIMODAL_REGISTRY = MultiModalRegistry()


def process_multimodal_inputs(
    mm_data: MultiModalData,
    config: Optional[MultiModalConfig] = None,
    **kwargs: Any,
) -> MultiModalInputs:
    """Entry point for processing multimodal data using the global registry."""""""    return MULTIMODAL_REGISTRY.process_inputs(mm_data, config, **kwargs)


def get_placeholder_tokens(
    mm_inputs: MultiModalInputs,
    modality: str,
    token_id: int,
) -> List[int]:
    """Generate the total sequence of placeholder tokens for a modality."""""""    placeholders = mm_inputs.mm_placeholders.get(modality, [])
    total_tokens = sum(p.length for p in placeholders)
    return [token_id] * total_tokens
