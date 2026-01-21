import logging
from typing import Dict, Optional, Any, List
from .base import (
    ModalityType,
    MultiModalConfig,
    MultiModalData,
    MultiModalInputs,
    BaseMultiModalProcessor,
    PlaceholderInfo,
)
from .image import ImageProcessor
from .video import VideoProcessor
from .audio import AudioProcessor
from .embed import TextEmbedProcessor

logger = logging.getLogger(__name__)

class MultiModalRegistry:
    """Central registry for multimodal processors."""
    
    def __init__(self):
        self._processors: Dict[ModalityType, BaseMultiModalProcessor] = {}
        self._default_config = MultiModalConfig()
    
    def register_processor(
        self,
        modality: ModalityType,
        processor: BaseMultiModalProcessor,
    ) -> None:
        self._processors[modality] = processor
        logger.debug("Registered processor for %s", modality.name)
    
    def get_processor(self, modality: ModalityType) -> Optional[BaseMultiModalProcessor]:
        return self._processors.get(modality)
    
    def create_processor(
        self,
        modality: ModalityType,
        config: Optional[MultiModalConfig] = None,
    ) -> BaseMultiModalProcessor:
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

def process_multimodal_inputs(
    mm_data: MultiModalData,
    config: Optional[MultiModalConfig] = None,
    **kwargs: Any,
) -> MultiModalInputs:
    return MULTIMODAL_REGISTRY.process_inputs(mm_data, config, **kwargs)

def get_placeholder_tokens(
    mm_inputs: MultiModalInputs,
    modality: str,
    token_id: int,
) -> List[int]:
    placeholders = mm_inputs.mm_placeholders.get(modality, [])
    total_tokens = sum(p.length for p in placeholders)
    return [token_id] * total_tokens
