# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\stream_omni.py\stream_omni.py\model.py\multimodal_resampler.py\builder_456560aa711a.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\Stream-Omni\stream_omni\model\multimodal_resampler\builder.py

import torch

from .masked_drop import MaskedDrop

from .perceiver import PerceiverResampler

from .qformer import Qformer

from .spatial_pool import SpatialPool


class IdentityMap(torch.nn.Module):
    def __init__(self):
        super().__init__()

    def forward(self, x, *args, **kwargs):
        return x

    @property
    def config(self):
        return {"mm_resampler_type": None}


def build_vision_resampler(model_args, delay_load=False, **kwargs):
    resampler_type = getattr(model_args, "mm_resampler_type", None)

    if resampler_type == "masked_drop":
        return MaskedDrop(model_args)

    elif resampler_type == "spatial_pool":
        return SpatialPool(model_args, **kwargs)

    elif resampler_type == "perceiver":
        return PerceiverResampler(model_args, **kwargs)

    elif resampler_type == "qformer":
        return Qformer(model_args, **kwargs)

    elif resampler_type is None:
        return IdentityMap()

    raise ValueError(f"Unknown resampler type: {resampler_type}")
