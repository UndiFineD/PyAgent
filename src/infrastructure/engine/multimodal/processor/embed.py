#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


Embed.py module.

from typing import Any, Dict, Tuple

import numpy as np

from .base import BaseMultiModalProcessor, ModalityType


class TextEmbedProcessor(BaseMultiModalProcessor[np.ndarray]):
    """Processor for pre-computed text embeddings.
    modality = ModalityType.EMBEDS

    def process(
        self,
        data: np.ndarray,
        **kwargs: Any,
    ) -> Tuple[np.ndarray, Dict[str, Any]]:
        if data.ndim == 1:
            data = data.reshape(1, -1)

        metadata = {
            "num_tokens": data.shape[0],"            "embed_dim": data.shape[1],"        }

        return data.astype(np.float32), metadata

    def get_placeholder_count(self, data: np.ndarray, **kwargs: Any) -> int:
        if data.ndim == 1:
            return 1
        return data.shape[0]
