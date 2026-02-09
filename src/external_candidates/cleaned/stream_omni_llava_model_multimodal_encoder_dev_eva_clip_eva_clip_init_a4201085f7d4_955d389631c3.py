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

# Extracted from: C:\DEV\PyAgent\.external\Stream-Omni\llava\model\multimodal_encoder\dev_eva_clip\eva_clip\__init__.py
from .constants import OPENAI_DATASET_MEAN, OPENAI_DATASET_STD
from .factory import (
    add_model_config,
    create_model,
    create_model_and_transforms,
    create_model_from_pretrained,
    get_model_config,
    get_tokenizer,
    list_models,
    load_checkpoint,
)
from .loss import ClipLoss
from .model import (
    CLIP,
    CLIPTextCfg,
    CLIPVisionCfg,
    CustomCLIP,
    convert_weights_to_fp16,
    convert_weights_to_lp,
    get_cast_dtype,
    trace_model,
)
from .openai import list_openai_models, load_openai_model
from .pretrained import (
    download_pretrained,
    download_pretrained_from_url,
    get_pretrained_cfg,
    get_pretrained_url,
    is_pretrained_cfg,
    list_pretrained,
    list_pretrained_models_by_tag,
    list_pretrained_tags_by_model,
)
from .tokenizer import SimpleTokenizer, tokenize
from .transform import image_transform
