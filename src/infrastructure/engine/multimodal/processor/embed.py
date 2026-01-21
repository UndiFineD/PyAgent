from typing import Tuple, Any, Dict, Optional
import numpy as np
from .base import BaseMultiModalProcessor, ModalityType, MultiModalConfig

class TextEmbedProcessor(BaseMultiModalProcessor[np.ndarray]):
    """Processor for pre-computed text embeddings."""
    modality = ModalityType.EMBEDS

    def process(
        self,
        data: np.ndarray,
        **kwargs: Any,
    ) -> Tuple[np.ndarray, Dict[str, Any]]:
        if data.ndim == 1:
            data = data.reshape(1, -1)

        metadata = {
            "num_tokens": data.shape[0],
            "embed_dim": data.shape[1],
        }

        return data.astype(np.float32), metadata

    def get_placeholder_count(self, data: np.ndarray, **kwargs: Any) -> int:
        if data.ndim == 1:
            return 1
        return data.shape[0]
