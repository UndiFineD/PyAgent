# Extracted from: C:\DEV\PyAgent\.external\ACTalker\src\models\base\TransformerSTmodel.py
# Copyright 2024 The HuggingFace Team. All rights reserved.
#
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

import math
import pdb
from typing import Any, Dict, Optional, Tuple, Union

import torch
from diffusers.models.attention import Attention
from diffusers.models.embeddings import TimestepEmbedding
from diffusers.models.resnet import (  # AlphaBlender
    Downsample2D,
    ResnetBlock2D,
    SpatioTemporalResBlock,
    TemporalConvLayer,
    Upsample2D,
)
from diffusers.models.transformers.dual_transformer_2d import DualTransformer2DModel
from diffusers.models.transformers.transformer_2d import Transformer2DModel
from diffusers.models.transformers.transformer_temporal import (
    TransformerTemporalModel,
    TransformerTemporalModelOutput,
)
from diffusers.utils import deprecate, is_torch_version, logging
from diffusers.utils.torch_utils import apply_freeu
from torch import nn

from .attention import BasicTransformerBlock, TemporalBasicTransformerBlock
from .mamba_layer import (
    SS2D_cond,
    SS2D_cond_v2,
    SS2D_cond_v3,
    SS2D_cond_v4,
    SS2D_cond_v4_wo_ssd,
    SS2D_cond_v5,
    SS2D_cond_v6,
    SS2D_cond_v7,
    SS2D_cond_v8,
    SS2D_cond_v9,
    SS2D_cond_v10,
    SS2D_cond_v10_wo_id,
    SS2D_seq,
)

logger = logging.get_logger(__name__)  # pylint: disable=invalid-name


def get_timestep_embedding(
    timesteps: torch.Tensor,
    embedding_dim: int,
    flip_sin_to_cos: bool = False,
    downscale_freq_shift: float = 1,
    scale: float = 1,
    max_period: int = 10000,
):
    """
    This matches the implementation in Denoising Diffusion Probabilistic Models: Create sinusoidal timestep embeddings.

    Args
        timesteps (torch.Tensor):
            a 1-D Tensor of N indices, one per batch element. These may be fractional.
        embedding_dim (int):
            the dimension of the output.
        flip_sin_to_cos (bool):
            Whether the embedding order should be `cos, sin` (if True) or `sin, cos` (if False)
        downscale_freq_shift (float):
            Controls the delta between frequencies between dimensions
        scale (float):
            Scaling factor applied to the embeddings.
        max_period (int):
            Controls the maximum frequency of the embeddings
    Returns
        torch.Tensor: an [N x dim] Tensor of positional embeddings.
    """
    assert len(timesteps.shape) == 1, "Timesteps should be a 1d-array"

    half_dim = embedding_dim // 2
    exponent = -math.log(max_period) * torch.arange(
        start=0, end=half_dim, dtype=torch.float32, device=timesteps.device
    )
    exponent = exponent / (half_dim - downscale_freq_shift)
    # import ipdb
    # ipdb.set_trace()

    emb = torch.exp(exponent)
    emb = timesteps[:, None].float() * emb[None, :]

    # scale embeddings
    emb = scale * emb

    # concat sine and cosine embeddings
    emb = torch.cat([torch.sin(emb), torch.cos(emb)], dim=-1)

    # flip sine and cosine embeddings
    if flip_sin_to_cos:
        emb = torch.cat([emb[:, half_dim:], emb[:, :half_dim]], dim=-1)

    # zero pad
    if embedding_dim % 2 == 1:
        emb = torch.nn.functional.pad(emb, (0, 1, 0, 0))
    return emb


class Timesteps(nn.Module):
    def __init__(
        self,
        num_channels: int,
        flip_sin_to_cos: bool,
        downscale_freq_shift: float,
        scale: int = 1,
    ):
        super().__init__()
        self.num_channels = num_channels
        self.flip_sin_to_cos = flip_sin_to_cos
        self.downscale_freq_shift = downscale_freq_shift
        self.scale = scale

    def forward(self, timesteps):
        t_emb = get_timestep_embedding(
            timesteps,
            self.num_channels,
            flip_sin_to_cos=self.flip_sin_to_cos,
            downscale_freq_shift=self.downscale_freq_shift,
            scale=self.scale,
        )
        return t_emb


class AlphaBlender(nn.Module):
    r"""
    A module to blend spatial and temporal features.

    Parameters:
        alpha (`float`): The initial value of the blending factor.
        merge_strategy (`str`, *optional*, defaults to `learned_with_images`):
            The merge strategy to use for the temporal mixing.
        switch_spatial_to_temporal_mix (`bool`, *optional*, defaults to `False`):
            If `True`, switch the spatial and temporal mixing.
    """

    strategies = ["learned", "fixed", "learned_with_images"]

    def __init__(
        self,
        alpha: float,
        merge_strategy: str = "learned_with_images",
        switch_spatial_to_temporal_mix: bool = False,
    ):
        super().__init__()
        self.merge_strategy = merge_strategy
        self.switch_spatial_to_temporal_mix = (
            switch_spatial_to_temporal_mix  # For TemporalVAE
        )

        if merge_strategy not in self.strategies:
            raise ValueError(f"merge_strategy needs to be in {self.strategies}")

        if self.merge_strategy == "fixed":
            self.register_buffer("mix_factor", torch.Tensor([alpha]))
        elif (
            self.merge_strategy == "learned"
            or self.merge_strategy == "learned_with_images"
        ):
            self.register_parameter(
                "mix_factor", torch.nn.Parameter(torch.Tensor([alpha]))
            )
        else:
            raise ValueError(f"Unknown merge strategy {self.merge_strategy}")

    def get_alpha(self, image_only_indicator: torch.Tensor, ndims: int) -> torch.Tensor:
        if self.merge_strategy == "fixed":
            alpha = self.mix_factor

        elif self.merge_strategy == "learned":
            alpha = torch.sigmoid(self.mix_factor)

        elif self.merge_strategy == "learned_with_images":
            if image_only_indicator is None:
                raise ValueError(
                    "Please provide image_only_indicator to use learned_with_images merge strategy"
                )

            alpha = torch.where(
                image_only_indicator.bool(),
                torch.ones(1, 1, device=image_only_indicator.device),
                torch.sigmoid(self.mix_factor)[..., None],
            )

            # (batch, channel, frames, height, width)
            if ndims == 5:
                alpha = alpha[:, None, :, None, None]
            # (batch*frames, height*width, channels)
            elif ndims == 3:
                alpha = alpha.reshape(-1)[:, None, None]
            else:
                raise ValueError(
                    f"Unexpected ndims {ndims}. Dimensions should be 3 or 5"
                )

        else:
            raise NotImplementedError

        return alpha

    def forward(
        self,
        x_spatial: torch.Tensor,
        x_temporal: torch.Tensor,
        image_only_indicator: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:
        alpha = self.get_alpha(image_only_indicator, x_spatial.ndim)
        alpha = alpha.to(x_spatial.dtype)

        # print(alpha[:2])
        # print( 1 - alpha[0,1])

        if self.switch_spatial_to_temporal_mix:
            alpha = 1.0 - alpha

        x = alpha * x_spatial + (1.0 - alpha) * x_temporal
        return x


class TransformerSpatioTemporalModel(nn.Module):
    """
    A Transformer model for video-like data.

    Parameters:
        num_attention_heads (`int`, *optional*, defaults to 16): The number of heads to use for multi-head attention.
        attention_head_dim (`int`, *optional*, defaults to 88): The number of channels in each head.
        in_channels (`int`, *optional*):
            The number of channels in the input and output (specify if the input is **continuous**).
        out_channels (`int`, *optional*):
            The number of channels in the output (specify if the input is **continuous**).
        num_layers (`int`, *optional*, defaults to 1): The number of layers of Transformer blocks to use.
        cross_attention_dim (`int`, *optional*): The number of `encoder_hidden_states` dimensions to use.
    """

    def __init__(
        self,
        num_attention_heads: int = 16,
        attention_head_dim: int = 88,
        in_channels: int = 320,
        out_channels: Optional[int] = None,
        num_layers: int = 1,
        cross_attention_dim: Optional[int] = None,
    ):
        super().__init__()
        self.num_attention_heads = num_attention_heads
        self.attention_head_dim = attention_head_dim

        inner_dim = num_attention_heads * attention_head_dim
        self.inner_dim = inner_dim

        # 2. Define input layers
        self.in_channels = in_channels
        self.norm = torch.nn.GroupNorm(
            num_groups=32, num_channels=in_channels, eps=1e-6
        )
        self.proj_in = nn.Linear(in_channels, inner_dim)

        # 3. Define transformers blocks
        self.transformer_blocks = nn.ModuleList(
            [
                BasicTransformerBlock(
                    inner_dim,
                    num_attention_heads,
                    attention_head_dim,
                    cross_attention_dim=cross_attention_dim,
                )
                for d in range(num_layers)
            ]
        )

        time_mix_inner_dim = inner_dim
        self.temporal_transformer_blocks = nn.ModuleList(
            [
                TemporalBasicTransformerBlock(
                    inner_dim,
                    time_mix_inner_dim,
                    num_attention_heads,
                    attention_head_dim,
                    cross_attention_dim=cross_attention_dim,
                )
                for _ in range(num_layers)
            ]
        )

        time_embed_dim = in_channels * 4
        self.time_pos_embed = TimestepEmbedding(
            in_channels, time_embed_dim, out_dim=in_channels
        )
        self.time_proj = Timesteps(in_channels, True, 0)
        self.time_mixer = AlphaBlender(alpha=0.5, merge_strategy="learned_with_images")

        # 4. Define output layers
        self.out_channels = in_channels if out_channels is None else out_channels
        # TODO: should use out_channels for continuous projections
        self.proj_out = nn.Linear(inner_dim, in_channels)

        self.gradient_checkpointing = False

    def forward(
        self,
        hidden_states: torch.Tensor,
        encoder_hidden_states: Optional[torch.Tensor] = None,
        cross_attention_kwargs: Optional[Dict[str, Any]] = None,
        image_only_indicator: Optional[torch.Tensor] = None,
        return_dict: bool = True,
    ):
        """
        Args:
            hidden_states (`torch.FloatTensor` of shape `(batch size, channel, height, width)`):
                Input hidden_states.
            num_frames (`int`):
                The number of frames to be processed per batch. This is used to reshape the hidden states.
            encoder_hidden_states ( `torch.LongTensor` of shape `(batch size, encoder_hidden_states dim)`, *optional*):
                Conditional embeddings for cross attention layer. If not given, cross-attention defaults to
                self-attention.
            image_only_indicator (`torch.LongTensor` of shape `(batch size, num_frames)`, *optional*):
                A tensor indicating whether the input contains only images. 1 indicates that the input contains only
                images, 0 indicates that the input contains video frames.
            return_dict (`bool`, *optional*, defaults to `True`):
                Whether or not to return a [`~models.transformer_temporal.TransformerTemporalModelOutput`] instead of a plain
                tuple.

        Returns:
            [`~models.transformer_temporal.TransformerTemporalModelOutput`] or `tuple`:
                If `return_dict` is True, an [`~models.transformer_temporal.TransformerTemporalModelOutput`] is
                returned, otherwise a `tuple` where the first element is the sample tensor.
        """

        # 1. Input
        batch_frames, _, height, width = hidden_states.shape
        num_frames = image_only_indicator.shape[-1]
        batch_size = batch_frames // num_frames

        def spatial2time(time_context):
            # print(time_context.shape)

            time_context = time_context.reshape(
                batch_size, num_frames, time_context.shape[-2], time_context.shape[-1]
            )
            time_context = time_context.mean(dim=(1,), keepdim=True)

            # time_context = time_context.flatten(1,2)
            # time_context = time_context[:, None].repeat(
            #     1, height * width, 1, 1
            # )
            time_context = time_context.repeat(1, height * width, 1, 1)
            time_context = time_context.reshape(
                batch_size * height * width, -1, time_context.shape[-1]
            )
            # print(time_context.shape)
            return time_context

        # clip_context, ip_contexts = encoder_hidden_states
        # clip_context_new = spatial2time(clip_context)
        # ip_contexts_new = []
        # for ip_context in ip_contexts:
        #     ip_context_new = spatial2time(ip_context)
        #     ip_contexts_new.append(ip_context_new)

        if isinstance(encoder_hidden_states, tuple):
            clip_hidden_states, ip_hidden_states = encoder_hidden_states
            encoder_hidden_states_time = (
                spatial2time(clip_hidden_states),
                [spatial2time(ip_hidden_state) for ip_hidden_state in ip_hidden_states],
            )
        else:
            encoder_hidden_states_time = spatial2time(encoder_hidden_states)

        residual = hidden_states

        hidden_states = self.norm(hidden_states)
        inner_dim = hidden_states.shape[1]
        hidden_states = hidden_states.permute(0, 2, 3, 1).reshape(
            batch_frames, height * width, inner_dim
        )
        hidden_states = self.proj_in(hidden_states)

        num_frames_emb = torch.arange(num_frames, device=hidden_states.device)
        num_frames_emb = num_frames_emb
        num_frames_emb = num_frames_emb.repeat(batch_size, 1)
        num_frames_emb = num_frames_emb.reshape(-1)
        t_emb = self.time_proj(num_frames_emb)
        # import ipdb
        # ipdb.set_trace()

        # `Timesteps` does not contain any weights and will always return f32 tensors
        # but time_embedding might actually be running in fp16. so we need to cast here.
        # there might be better ways to encapsulate this.
        t_emb = t_emb.to(dtype=hidden_states.dtype)

        emb = self.time_pos_embed(t_emb)
        emb = emb[:, None, :]
        # print(self.time_mixer.alpha)
        # 2. Blocks
        for block, temporal_block in zip(
            self.transformer_blocks, self.temporal_transformer_blocks
        ):
            if self.training and self.gradient_checkpointing:
                hidden_states = torch.utils.checkpoint.checkpoint(
                    block,
                    hidden_states,
                    None,
                    encoder_hidden_states,
                    None,
                    None,
                    cross_attention_kwargs,
                    use_reentrant=False,
                )
            else:
                hidden_states = block(
                    hidden_states,
                    encoder_hidden_states=encoder_hidden_states,
                    cross_attention_kwargs=cross_attention_kwargs,
                )

            hidden_states_mix = hidden_states
            hidden_states_mix = hidden_states_mix + emb

            if self.training and self.gradient_checkpointing:

                hidden_states_mix = torch.utils.checkpoint.checkpoint(
                    temporal_block,
                    hidden_states_mix,
                    num_frames,
                    encoder_hidden_states_time,
                    use_reentrant=False,
                )

            else:
                hidden_states_mix = temporal_block(
                    hidden_states_mix,
                    num_frames=num_frames,
                    encoder_hidden_states=encoder_hidden_states_time,
                )
            hidden_states = self.time_mixer(
                x_spatial=hidden_states,
                x_temporal=hidden_states_mix,
                image_only_indicator=image_only_indicator,
            )

        # 3. Output
        hidden_states = self.proj_out(hidden_states)
        hidden_states = (
            hidden_states.reshape(batch_frames, height, width, inner_dim)
            .permute(0, 3, 1, 2)
            .contiguous()
        )

        output = hidden_states + residual

        if not return_dict:
            return (output,)

        return TransformerTemporalModelOutput(sample=output)


# only use the unet feature after spatial attn
class TransformerSpatioTemporalModel_mambav1(nn.Module):
    """
    A Transformer model for video-like data.

    Parameters:
        num_attention_heads (`int`, *optional*, defaults to 16): The number of heads to use for multi-head attention.
        attention_head_dim (`int`, *optional*, defaults to 88): The number of channels in each head.
        in_channels (`int`, *optional*):
            The number of channels in the input and output (specify if the input is **continuous**).
        out_channels (`int`, *optional*):
            The number of channels in the output (specify if the input is **continuous**).
        num_layers (`int`, *optional*, defaults to 1): The number of layers of Transformer blocks to use.
        cross_attention_dim (`int`, *optional*): The number of `encoder_hidden_states` dimensions to use.
    """

    def __init__(
        self,
        num_attention_heads: int = 16,
        attention_head_dim: int = 88,
        in_channels: int = 320,
        out_channels: Optional[int] = None,
        num_layers: int = 1,
        cross_attention_dim: Optional[int] = None,
    ):
        super().__init__()
        self.num_attention_heads = num_attention_heads
        self.attention_head_dim = attention_head_dim

        inner_dim = num_attention_heads * attention_head_dim
        self.inner_dim = inner_dim

        # 2. Define input layers
        self.in_channels = in_channels
        self.norm = torch.nn.GroupNorm(
            num_groups=32, num_channels=in_channels, eps=1e-6
        )
        self.proj_in = nn.Linear(in_channels, inner_dim)

        # 3. Define transformers blocks
        self.transformer_blocks = nn.ModuleList(
            [
                BasicTransformerBlock(
                    inner_dim,
                    num_attention_heads,
                    attention_head_dim,
                    cross_attention_dim=cross_attention_dim,
                )
                for d in range(num_layers)
            ]
        )

        # 3. Define transformers blocks
        # self_attention_cond = SS2D_cond(d_model=320,d_cond=1024, dropout=0.1, d_state=16, size=36, scan_type='scan', num_direction=4)
        # self_attention_cond = SS2D_cond(d_model=320,d_cond=1024,cond_size=32, dropout=0.1, d_state=16, size=72, scan_type='sweep', num_direction=2).cuda()
        self.mamba_blocks = nn.ModuleList(
            [
                SS2D_seq(
                    d_model=in_channels,
                    d_cond=cross_attention_dim,
                    cond_size=32,
                    dropout=0.1,
                    d_state=16,
                    size=int(72 / (in_channels / 320)),
                    scan_type="sweep",
                    num_direction=2,
                )
                for d in range(num_layers)
            ]
        )
        time_mix_inner_dim = inner_dim
        self.temporal_transformer_blocks = nn.ModuleList(
            [
                TemporalBasicTransformerBlock(
                    inner_dim,
                    time_mix_inner_dim,
                    num_attention_heads,
                    attention_head_dim,
                    cross_attention_dim=cross_attention_dim,
                )
                for _ in range(num_layers)
            ]
        )

        time_embed_dim = in_channels * 4
        self.time_pos_embed = TimestepEmbedding(
            in_channels, time_embed_dim, out_dim=in_channels
        )
        self.time_proj = Timesteps(in_channels, True, 0)
        self.time_mixer = AlphaBlender(alpha=0.5, merge_strategy="learned_with_images")

        # 4. Define output layers
        self.out_channels = in_channels if out_channels is None else out_channels
        # TODO: should use out_channels for continuous projections
        self.proj_out = nn.Linear(inner_dim, in_channels)

        self.gradient_checkpointing = False

    def forward(
        self,
        hidden_states: torch.Tensor,
        encoder_hidden_states: Optional[torch.Tensor] = None,
        cross_attention_kwargs: Optional[Dict[str, Any]] = None,
        image_only_indicator: Optional[torch.Tensor] = None,
        return_dict: bool = True,
    ):
        """
        Args:
            hidden_states (`torch.FloatTensor` of shape `(batch size, channel, height, width)`):
                Input hidden_states.
            num_frames (`int`):
                The number of frames to be processed per batch. This is used to reshape the hidden states.
            encoder_hidden_states ( `torch.LongTensor` of shape `(batch size, encoder_hidden_states dim)`, *optional*):
                Conditional embeddings for cross attention layer. If not given, cross-attention defaults to
                self-attention.
            image_only_indicator (`torch.LongTensor` of shape `(batch size, num_frames)`, *optional*):
                A tensor indicating whether the input contains only images. 1 indicates that the input contains only
                images, 0 indicates that the input contains video frames.
            return_dict (`bool`, *optional*, defaults to `True`):
                Whether or not to return a [`~models.transformer_temporal.TransformerTemporalModelOutput`] instead of a plain
                tuple.

        Returns:
            [`~models.transformer_temporal.TransformerTemporalModelOutput`] or `tuple`:
                If `return_dict` is True, an [`~models.transformer_temporal.TransformerTemporalModelOutput`] is
                returned, otherwise a `tuple` where the first element is the sample tensor.
        """

        # 1. Input
        batch_frames, _, height, width = hidden_states.shape
        num_frames = image_only_indicator.shape[-1]
        batch_size = batch_frames // num_frames

        def spatial2time(time_context):
            # print(time_context.shape)

            time_context = time_context.reshape(
                batch_size, num_frames, time_context.shape[-2], time_context.shape[-1]
            )
            time_context = time_context.mean(dim=(1,), keepdim=True)

            # time_context = time_context.flatten(1,2)
            # time_context = time_context[:, None].repeat(
            #     1, height * width, 1, 1
            # )
            time_context = time_context.repeat(1, height * width, 1, 1)
            time_context = time_context.reshape(
                batch_size * height * width, -1, time_context.shape[-1]
            )
            # print(time_context.shape)
            return time_context

        # clip_context, ip_contexts = encoder_hidden_states
        # clip_context_new = spatial2time(clip_context)
        # ip_contexts_new = []
        # for ip_context in ip_contexts:
        #     ip_context_new = spatial2time(ip_context)
        #     ip_contexts_new.append(ip_context_new)

        if isinstance(encoder_hidden_states, tuple):
            clip_hidden_states, ip_hidden_states = encoder_hidden_states
            encoder_hidden_states_time = (
                spatial2time(clip_hidden_states),
                [spatial2time(ip_hidden_state) for ip_hidden_state in ip_hidden_states],
            )
        else:
            encoder_hidden_states_time = spatial2time(encoder_hidden_states)

        residual = hidden_states

        hidden_states = self.norm(hidden_states)
        inner_dim = hidden_states.shape[1]
        hidden_states = hidden_states.permute(0, 2, 3, 1).reshape(
            batch_frames, height * width, inner_dim
        )
        hidden_states = self.proj_in(hidden_states)

        num_frames_emb = torch.arange(num_frames, device=hidden_states.device)
        num_frames_emb = num_frames_emb
        num_frames_emb = num_frames_emb.repeat(batch_size, 1)
        num_frames_emb = num_frames_emb.reshape(-1)
        t_emb = self.time_proj(num_frames_emb)
        # import ipdb
        # ipdb.set_trace()

        # `Timesteps` does not contain any weights and will always return f32 tensors
        # but time_embedding might actually be running in fp16. so we need to cast here.
        # there might be better ways to encapsulate this.
        t_emb = t_emb.to(dtype=hidden_states.dtype)

        emb = self.time_pos_embed(t_emb)
        emb = emb[:, None, :]
        # print(self.time_mixer.alpha)
        # 2. Blocks
        for block, mamba_block, temporal_block in zip(
            self.transformer_blocks, self.mamba_blocks, self.temporal_transformer_blocks
        ):
            if self.training and self.gradient_checkpointing:
                hidden_states = torch.utils.checkpoint.checkpoint(
                    block,
                    hidden_states,
                    None,
                    encoder_hidden_states,
                    None,
                    None,
                    cross_attention_kwargs,
                    use_reentrant=False,
                )
            else:
                hidden_states = block(
                    hidden_states,
                    encoder_hidden_states=encoder_hidden_states,
                    cross_attention_kwargs=cross_attention_kwargs,
                )
            if self.training and self.gradient_checkpointing:
                hidden_states = torch.utils.checkpoint.checkpoint(
                    mamba_block,
                    hidden_states,
                    encoder_hidden_states[0][0],
                )
            else:
                hidden_states = mamba_block(hidden_states, encoder_hidden_states[1][0])
            hidden_states_mix = hidden_states
            hidden_states_mix = hidden_states_mix + emb

            if self.training and self.gradient_checkpointing:

                hidden_states_mix = torch.utils.checkpoint.checkpoint(
                    temporal_block,
                    hidden_states_mix,
                    num_frames,
                    encoder_hidden_states_time,
                    use_reentrant=False,
                )

            else:
                hidden_states_mix = temporal_block(
                    hidden_states_mix,
                    num_frames=num_frames,
                    encoder_hidden_states=encoder_hidden_states_time,
                )
            hidden_states = self.time_mixer(
                x_spatial=hidden_states,
                x_temporal=hidden_states_mix,
                image_only_indicator=image_only_indicator,
            )

        # 3. Output
        hidden_states = self.proj_out(hidden_states)
        hidden_states = (
            hidden_states.reshape(batch_frames, height, width, inner_dim)
            .permute(0, 3, 1, 2)
            .contiguous()
        )

        output = hidden_states + residual

        if not return_dict:
            return (output,)

        return TransformerTemporalModelOutput(sample=output)


# use the unet feature conditioned by clip feature after spatial attn
class TransformerSpatioTemporalModel_mambav2(nn.Module):
    """
    A Transformer model for video-like data.

    Parameters:
        num_attention_heads (`int`, *optional*, defaults to 16): The number of heads to use for multi-head attention.
        attention_head_dim (`int`, *optional*, defaults to 88): The number of channels in each head.
        in_channels (`int`, *optional*):
            The number of channels in the input and output (specify if the input is **continuous**).
        out_channels (`int`, *optional*):
            The number of channels in the output (specify if the input is **continuous**).
        num_layers (`int`, *optional*, defaults to 1): The number of layers of Transformer blocks to use.
        cross_attention_dim (`int`, *optional*): The number of `encoder_hidden_states` dimensions to use.
    """

    def __init__(
        self,
        num_attention_heads: int = 16,
        attention_head_dim: int = 88,
        in_channels: int = 320,
        out_channels: Optional[int] = None,
        num_layers: int = 1,
        cross_attention_dim: Optional[int] = None,
    ):
        super().__init__()
        self.num_attention_heads = num_attention_heads
        self.attention_head_dim = attention_head_dim

        inner_dim = num_attention_heads * attention_head_dim
        self.inner_dim = inner_dim

        # 2. Define input layers
        self.in_channels = in_channels
        self.norm = torch.nn.GroupNorm(
            num_groups=32, num_channels=in_channels, eps=1e-6
        )
        self.proj_in = nn.Linear(in_channels, inner_dim)

        # 3. Define transformers blocks
        self.transformer_blocks = nn.ModuleList(
            [
                BasicTransformerBlock(
                    inner_dim,
                    num_attention_heads,
                    attention_head_dim,
                    cross_attention_dim=cross_attention_dim,
                )
                for d in range(num_layers)
            ]
        )

        # 3. Define transformers blocks
        # self_attention_cond = SS2D_cond(d_model=320,d_cond=1024, dropout=0.1, d_state=16, size=36, scan_type='scan', num_direction=4)
        # self_attention_cond = SS2D_cond(d_model=320,d_cond=1024,cond_size=32, dropout=0.1, d_state=16, size=72, scan_type='sweep', num_direction=2).cuda()
        self.mamba_blocks = nn.ModuleList(
            [
                SS2D_cond_v3(
                    d_model=in_channels,
                    d_cond=cross_attention_dim,
                    cond_size=32,
                    dropout=0.1,
                    d_state=16,
                    size=int(72 / (in_channels / 320)),
                    scan_type="sweep",
                    num_direction=2,
                )
                for d in range(num_layers)
            ]
        )
        time_mix_inner_dim = inner_dim
        self.temporal_transformer_blocks = nn.ModuleList(
            [
                TemporalBasicTransformerBlock(
                    inner_dim,
                    time_mix_inner_dim,
                    num_attention_heads,
                    attention_head_dim,
                    cross_attention_dim=cross_attention_dim,
                )
                for _ in range(num_layers)
            ]
        )

        time_embed_dim = in_channels * 4
        self.time_pos_embed = TimestepEmbedding(
            in_channels, time_embed_dim, out_dim=in_channels
        )
        self.time_proj = Timesteps(in_channels, True, 0)
        self.time_mixer = AlphaBlender(alpha=0.5, merge_strategy="learned_with_images")

        # 4. Define output layers
        self.out_channels = in_channels if out_channels is None else out_channels
        # TODO: should use out_channels for continuous projections
        self.proj_out = nn.Linear(inner_dim, in_channels)

        self.gradient_checkpointing = False

    def forward(
        self,
        hidden_states: torch.Tensor,
        encoder_hidden_states: Optional[torch.Tensor] = None,
        cross_attention_kwargs: Optional[Dict[str, Any]] = None,
        image_only_indicator: Optional[torch.Tensor] = None,
        return_dict: bool = True,
    ):
        """
        Args:
            hidden_states (`torch.FloatTensor` of shape `(batch size, channel, height, width)`):
                Input hidden_states.
            num_frames (`int`):
                The number of frames to be processed per batch. This is used to reshape the hidden states.
            encoder_hidden_states ( `torch.LongTensor` of shape `(batch size, encoder_hidden_states dim)`, *optional*):
                Conditional embeddings for cross attention layer. If not given, cross-attention defaults to
                self-attention.
            image_only_indicator (`torch.LongTensor` of shape `(batch size, num_frames)`, *optional*):
                A tensor indicating whether the input contains only images. 1 indicates that the input contains only
                images, 0 indicates that the input contains video frames.
            return_dict (`bool`, *optional*, defaults to `True`):
                Whether or not to return a [`~models.transformer_temporal.TransformerTemporalModelOutput`] instead of a plain
                tuple.

        Returns:
            [`~models.transformer_temporal.TransformerTemporalModelOutput`] or `tuple`:
                If `return_dict` is True, an [`~models.transformer_temporal.TransformerTemporalModelOutput`] is
                returned, otherwise a `tuple` where the first element is the sample tensor.
        """

        # 1. Input
        batch_frames, _, height, width = hidden_states.shape
        num_frames = image_only_indicator.shape[-1]
        batch_size = batch_frames // num_frames

        def spatial2time(time_context):
            # print(time_context.shape)

            time_context = time_context.reshape(
                batch_size, num_frames, time_context.shape[-2], time_context.shape[-1]
            )
            time_context = time_context.mean(dim=(1,), keepdim=True)

            # time_context = time_context.flatten(1,2)
            # time_context = time_context[:, None].repeat(
            #     1, height * width, 1, 1
            # )
            time_context = time_context.repeat(1, height * width, 1, 1)
            time_context = time_context.reshape(
                batch_size * height * width, -1, time_context.shape[-1]
            )
            # print(time_context.shape)
            return time_context

        # clip_context, ip_contexts = encoder_hidden_states
        # clip_context_new = spatial2time(clip_context)
        # ip_contexts_new = []
        # for ip_context in ip_contexts:
        #     ip_context_new = spatial2time(ip_context)
        #     ip_contexts_new.append(ip_context_new)

        if isinstance(encoder_hidden_states, tuple):
            clip_hidden_states, ip_hidden_states = encoder_hidden_states
            encoder_hidden_states_time = (
                spatial2time(clip_hidden_states),
                [spatial2time(ip_hidden_state) for ip_hidden_state in ip_hidden_states],
            )
        else:
            encoder_hidden_states_time = spatial2time(encoder_hidden_states)

        residual = hidden_states

        hidden_states = self.norm(hidden_states)
        inner_dim = hidden_states.shape[1]
        hidden_states = hidden_states.permute(0, 2, 3, 1).reshape(
            batch_frames, height * width, inner_dim
        )
        hidden_states = self.proj_in(hidden_states)

        num_frames_emb = torch.arange(num_frames, device=hidden_states.device)
        num_frames_emb = num_frames_emb
        num_frames_emb = num_frames_emb.repeat(batch_size, 1)
        num_frames_emb = num_frames_emb.reshape(-1)
        t_emb = self.time_proj(num_frames_emb)
        # import ipdb
        # ipdb.set_trace()

        # `Timesteps` does not contain any weights and will always return f32 tensors
        # but time_embedding might actually be running in fp16. so we need to cast here.
        # there might be better ways to encapsulate this.
        t_emb = t_emb.to(dtype=hidden_states.dtype)

        emb = self.time_pos_embed(t_emb)
        emb = emb[:, None, :]
        # print(self.time_mixer.alpha)
        # 2. Blocks
        for block, mamba_block, temporal_block in zip(
            self.transformer_blocks, self.mamba_blocks, self.temporal_transformer_blocks
        ):
            if self.training and self.gradient_checkpointing:
                hidden_states = torch.utils.checkpoint.checkpoint(
                    block,
                    hidden_states,
                    None,
                    encoder_hidden_states,
                    None,
                    None,
                    cross_attention_kwargs,
                    use_reentrant=False,
                )
            else:
                hidden_states = block(
                    hidden_states,
                    encoder_hidden_states=encoder_hidden_states,
                    cross_attention_kwargs=cross_attention_kwargs,
                )
            if self.training and self.gradient_checkpointing:
                hidden_states = torch.utils.checkpoint.checkpoint(
                    mamba_block,
                    hidden_states,
                    encoder_hidden_states[0],
                )
            else:
                hidden_states = mamba_block(hidden_states, encoder_hidden_states[0])
            hidden_states_mix = hidden_states
            hidden_states_mix = hidden_states_mix + emb
            if self.training and self.gradient_checkpointing:

                hidden_states_mix = torch.utils.checkpoint.checkpoint(
                    temporal_block,
                    hidden_states_mix,
                    num_frames,
                    encoder_hidden_states_time,
                    use_reentrant=False,
                )

            else:
                hidden_states_mix = temporal_block(
                    hidden_states_mix,
                    num_frames=num_frames,
                    encoder_hidden_states=encoder_hidden_states_time,
                )
            hidden_states = self.time_mixer(
                x_spatial=hidden_states,
                x_temporal=hidden_states_mix,
                image_only_indicator=image_only_indicator,
            )

        # 3. Output
        hidden_states = self.proj_out(hidden_states)
        hidden_states = (
            hidden_states.reshape(batch_frames, height, width, inner_dim)
            .permute(0, 3, 1, 2)
            .contiguous()
        )

        output = hidden_states + residual

        if not return_dict:
            return (output,)

        return TransformerTemporalModelOutput(sample=output)


# use the unet feature conditioned by clip feature after spatial attn
class TransformerSpatioTemporalModel_mambaID_v3(nn.Module):
    """
    A Transformer model for video-like data.

    Parameters:
        num_attention_heads (`int`, *optional*, defaults to 16): The number of heads to use for multi-head attention.
        attention_head_dim (`int`, *optional*, defaults to 88): The number of channels in each head.
        in_channels (`int`, *optional*):
            The number of channels in the input and output (specify if the input is **continuous**).
        out_channels (`int`, *optional*):
            The number of channels in the output (specify if the input is **continuous**).
        num_layers (`int`, *optional*, defaults to 1): The number of layers of Transformer blocks to use.
        cross_attention_dim (`int`, *optional*): The number of `encoder_hidden_states` dimensions to use.
    """

    def __init__(
        self,
        num_attention_heads: int = 16,
        attention_head_dim: int = 88,
        in_channels: int = 320,
        out_channels: Optional[int] = None,
        num_layers: int = 1,
        cross_attention_dim: Optional[int] = None,
    ):
        super().__init__()
        self.num_attention_heads = num_attention_heads
        self.attention_head_dim = attention_head_dim

        inner_dim = num_attention_heads * attention_head_dim
        self.inner_dim = inner_dim

        # 2. Define input layers
        self.in_channels = in_channels
        self.norm = torch.nn.GroupNorm(
            num_groups=32, num_channels=in_channels, eps=1e-6
        )
        self.proj_in = nn.Linear(in_channels, inner_dim)

        # 3. Define transformers blocks
        self.transformer_blocks = nn.ModuleList(
            [
                BasicTransformerBlock(
                    inner_dim,
                    num_attention_heads,
                    attention_head_dim,
                    cross_attention_dim=cross_attention_dim,
                )
                for d in range(num_layers)
            ]
        )

        # 3. Define transformers blocks
        # self_attention_cond = SS2D_cond(d_model=320,d_cond=1024, dropout=0.1, d_state=16, size=36, scan_type='scan', num_direction=4)
        # self_attention_cond = SS2D_cond(d_model=320,d_cond=1024,cond_size=32, dropout=0.1, d_state=16, size=72, scan_type='sweep', num_direction=2).cuda()
        self.mamba_blocks = nn.ModuleList(
            [
                SS2D_cond_v3(
                    d_model=in_channels,
                    d_cond=cross_attention_dim,
                    cond_size=32,
                    dropout=0.1,
                    d_state=16,
                    size=int(72 / (in_channels / 320)),
                    scan_type="sweep",
                    num_direction=2,
                )
                for d in range(num_layers)
            ]
        )
        time_mix_inner_dim = inner_dim
        self.temporal_transformer_blocks = nn.ModuleList(
            [
                TemporalBasicTransformerBlock(
                    inner_dim,
                    time_mix_inner_dim,
                    num_attention_heads,
                    attention_head_dim,
                    cross_attention_dim=cross_attention_dim,
                )
                for _ in range(num_layers)
            ]
        )

        time_embed_dim = in_channels * 4
        self.time_pos_embed = TimestepEmbedding(
            in_channels, time_embed_dim, out_dim=in_channels
        )
        self.time_proj = Timesteps(in_channels, True, 0)
        self.time_mixer = AlphaBlender(alpha=0.5, merge_strategy="learned_with_images")

        # 4. Define output layers
        self.out_channels = in_channels if out_channels is None else out_channels
        # TODO: should use out_channels for continuous projections
        self.proj_out = nn.Linear(inner_dim, in_channels)

        self.gradient_checkpointing = False

    def forward(
        self,
        hidden_states: torch.Tensor,
        encoder_hidden_states: Optional[torch.Tensor] = None,
        cross_attention_kwargs: Optional[Dict[str, Any]] = None,
        image_only_indicator: Optional[torch.Tensor] = None,
        return_dict: bool = True,
    ):
        """
        Args:
            hidden_states (`torch.FloatTensor` of shape `(batch size, channel, height, width)`):
                Input hidden_states.
            num_frames (`int`):
                The number of frames to be processed per batch. This is used to reshape the hidden states.
            encoder_hidden_states ( `torch.LongTensor` of shape `(batch size, encoder_hidden_states dim)`, *optional*):
                Conditional embeddings for cross attention layer. If not given, cross-attention defaults to
                self-attention.
            image_only_indicator (`torch.LongTensor` of shape `(batch size, num_frames)`, *optional*):
                A tensor indicating whether the input contains only images. 1 indicates that the input contains only
                images, 0 indicates that the input contains video frames.
            return_dict (`bool`, *optional*, defaults to `True`):
                Whether or not to return a [`~models.transformer_temporal.TransformerTemporalModelOutput`] instead of a plain
                tuple.

        Returns:
            [`~models.transformer_temporal.TransformerTemporalModelOutput`] or `tuple`:
                If `return_dict` is True, an [`~models.transformer_temporal.TransformerTemporalModelOutput`] is
                returned, otherwise a `tuple` where the first element is the sample tensor.
        """

        # 1. Input
        batch_frames, _, height, width = hidden_states.shape
        num_frames = image_only_indicator.shape[-1]
        batch_size = batch_frames // num_frames

        def spatial2time(time_context):
            # print(time_context.shape)

            time_context = time_context.reshape(
                batch_size, num_frames, time_context.shape[-2], time_context.shape[-1]
            )
            time_context = time_context.mean(dim=(1,), keepdim=True)

            # time_context = time_context.flatten(1,2)
            # time_context = time_context[:, None].repeat(
            #     1, height * width, 1, 1
            # )
            time_context = time_context.repeat(1, height * width, 1, 1)
            time_context = time_context.reshape(
                batch_size * height * width, -1, time_context.shape[-1]
            )
            # print(time_context.shape)
            return time_context

        # clip_context, ip_contexts = encoder_hidden_states
        # clip_context_new = spatial2time(clip_context)
        # ip_contexts_new = []
        # for ip_context in ip_contexts:
        #     ip_context_new = spatial2time(ip_context)
        #     ip_contexts_new.append(ip_context_new)

        if isinstance(encoder_hidden_states, tuple):
            clip_hidden_states, ip_hidden_states = encoder_hidden_states
            encoder_hidden_states_time = (
                spatial2time(clip_hidden_states),
                [spatial2time(ip_hidden_state) for ip_hidden_state in ip_hidden_states],
            )
        else:
            encoder_hidden_states_time = spatial2time(encoder_hidden_states)

        residual = hidden_states

        hidden_states = self.norm(hidden_states)
        inner_dim = hidden_states.shape[1]
        hidden_states = hidden_states.permute(0, 2, 3, 1).reshape(
            batch_frames, height * width, inner_dim
        )
        hidden_states = self.proj_in(hidden_states)

        num_frames_emb = torch.arange(num_frames, device=hidden_states.device)
        num_frames_emb = num_frames_emb
        num_frames_emb = num_frames_emb.repeat(batch_size, 1)
        num_frames_emb = num_frames_emb.reshape(-1)
        t_emb = self.time_proj(num_frames_emb)
        # import ipdb
        # ipdb.set_trace()

        # `Timesteps` does not contain any weights and will always return f32 tensors
        # but time_embedding might actually be running in fp16. so we need to cast here.
        # there might be better ways to encapsulate this.
        t_emb = t_emb.to(dtype=hidden_states.dtype)

        emb = self.time_pos_embed(t_emb)
        emb = emb[:, None, :]
        # print(self.time_mixer.alpha)
        # 2. Blocks
        for block, mamba_block, temporal_block in zip(
            self.transformer_blocks, self.mamba_blocks, self.temporal_transformer_blocks
        ):
            if self.training and self.gradient_checkpointing:
                hidden_states = torch.utils.checkpoint.checkpoint(
                    block,
                    hidden_states,
                    None,
                    encoder_hidden_states,
                    None,
                    None,
                    cross_attention_kwargs,
                    use_reentrant=False,
                )
            else:
                hidden_states = block(
                    hidden_states,
                    encoder_hidden_states=encoder_hidden_states,
                    cross_attention_kwargs=cross_attention_kwargs,
                )
            if self.training and self.gradient_checkpointing:
                hidden_states = torch.utils.checkpoint.checkpoint(
                    mamba_block,
                    hidden_states,
                    torch.cat(
                        [
                            encoder_hidden_states[0],
                            encoder_hidden_states[1][0].squeeze(1),
                        ],
                        dim=1,
                    ),
                )
            else:
                hidden_states = mamba_block(
                    hidden_states,
                    torch.cat(
                        [
                            encoder_hidden_states[0],
                            encoder_hidden_states[1][0].squeeze(1),
                        ],
                        dim=1,
                    ),
                )
            hidden_states_mix = hidden_states
            hidden_states_mix = hidden_states_mix + emb
            if self.training and self.gradient_checkpointing:

                hidden_states_mix = torch.utils.checkpoint.checkpoint(
                    temporal_block,
                    hidden_states_mix,
                    num_frames,
                    encoder_hidden_states_time,
                    use_reentrant=False,
                )

            else:
                hidden_states_mix = temporal_block(
                    hidden_states_mix,
                    num_frames=num_frames,
                    encoder_hidden_states=encoder_hidden_states_time,
                )
            hidden_states = self.time_mixer(
                x_spatial=hidden_states,
                x_temporal=hidden_states_mix,
                image_only_indicator=image_only_indicator,
            )

        # 3. Output
        hidden_states = self.proj_out(hidden_states)
        hidden_states = (
            hidden_states.reshape(batch_frames, height, width, inner_dim)
            .permute(0, 3, 1, 2)
            .contiguous()
        )

        output = hidden_states + residual

        if not return_dict:
            return (output,)

        return TransformerTemporalModelOutput(sample=output)


# use the unet feature conditioned by clip feature after spatial attn, 更改了mamba的结构
class TransformerSpatioTemporalModel_mambaID_v4(nn.Module):
    """
    A Transformer model for video-like data.

    Parameters:
        num_attention_heads (`int`, *optional*, defaults to 16): The number of heads to use for multi-head attention.
        attention_head_dim (`int`, *optional*, defaults to 88): The number of channels in each head.
        in_channels (`int`, *optional*):
            The number of channels in the input and output (specify if the input is **continuous**).
        out_channels (`int`, *optional*):
            The number of channels in the output (specify if the input is **continuous**).
        num_layers (`int`, *optional*, defaults to 1): The number of layers of Transformer blocks to use.
        cross_attention_dim (`int`, *optional*): The number of `encoder_hidden_states` dimensions to use.
    """

    def __init__(
        self,
        num_attention_heads: int = 16,
        attention_head_dim: int = 88,
        in_channels: int = 320,
        out_channels: Optional[int] = None,
        num_layers: int = 1,
        cross_attention_dim: Optional[int] = None,
    ):
        super().__init__()
        self.num_attention_heads = num_attention_heads
        self.attention_head_dim = attention_head_dim

        inner_dim = num_attention_heads * attention_head_dim
        self.inner_dim = inner_dim

        # 2. Define input layers
        self.in_channels = in_channels
        self.norm = torch.nn.GroupNorm(
            num_groups=32, num_channels=in_channels, eps=1e-6
        )
        self.proj_in = nn.Linear(in_channels, inner_dim)

        # 3. Define transformers blocks
        self.transformer_blocks = nn.ModuleList(
            [
                BasicTransformerBlock(
                    inner_dim,
                    num_attention_heads,
                    attention_head_dim,
                    cross_attention_dim=cross_attention_dim,
                )
                for d in range(num_layers)
            ]
        )

        # 3. Define transformers blocks
        # self_attention_cond = SS2D_cond(d_model=320,d_cond=1024, dropout=0.1, d_state=16, size=36, scan_type='scan', num_direction=4)
        # self_attention_cond = SS2D_cond(d_model=320,d_cond=1024,cond_size=32, dropout=0.1, d_state=16, size=72, scan_type='sweep', num_direction=2).cuda()
        self.mamba_blocks = nn.ModuleList(
            [
                SS2D_cond_v4(
                    d_model=in_channels,
                    d_cond=cross_attention_dim,
                    cond_size=32,
                    dropout=0.1,
                    d_state=16,
                    size=int(72 / (in_channels / 320)),
                    scan_type="sweep",
                    num_direction=2,
                )
                for d in range(num_layers)
            ]
        )
        time_mix_inner_dim = inner_dim
        self.temporal_transformer_blocks = nn.ModuleList(
            [
                TemporalBasicTransformerBlock(
                    inner_dim,
                    time_mix_inner_dim,
                    num_attention_heads,
                    attention_head_dim,
                    cross_attention_dim=cross_attention_dim,
                )
                for _ in range(num_layers)
            ]
        )

        time_embed_dim = in_channels * 4
        self.time_pos_embed = TimestepEmbedding(
            in_channels, time_embed_dim, out_dim=in_channels
        )
        self.time_proj = Timesteps(in_channels, True, 0)
        self.time_mixer = AlphaBlender(alpha=0.5, merge_strategy="learned_with_images")

        # 4. Define output layers
        self.out_channels = in_channels if out_channels is None else out_channels
        # TODO: should use out_channels for continuous projections
        self.proj_out = nn.Linear(inner_dim, in_channels)

        self.gradient_checkpointing = False

    def forward(
        self,
        hidden_states: torch.Tensor,
        encoder_hidden_states: Optional[torch.Tensor] = None,
        cross_attention_kwargs: Optional[Dict[str, Any]] = None,
        image_only_indicator: Optional[torch.Tensor] = None,
        return_dict: bool = True,
    ):
        """
        Args:
            hidden_states (`torch.FloatTensor` of shape `(batch size, channel, height, width)`):
                Input hidden_states.
            num_frames (`int`):
                The number of frames to be processed per batch. This is used to reshape the hidden states.
            encoder_hidden_states ( `torch.LongTensor` of shape `(batch size, encoder_hidden_states dim)`, *optional*):
                Conditional embeddings for cross attention layer. If not given, cross-attention defaults to
                self-attention.
            image_only_indicator (`torch.LongTensor` of shape `(batch size, num_frames)`, *optional*):
                A tensor indicating whether the input contains only images. 1 indicates that the input contains only
                images, 0 indicates that the input contains video frames.
            return_dict (`bool`, *optional*, defaults to `True`):
                Whether or not to return a [`~models.transformer_temporal.TransformerTemporalModelOutput`] instead of a plain
                tuple.

        Returns:
            [`~models.transformer_temporal.TransformerTemporalModelOutput`] or `tuple`:
                If `return_dict` is True, an [`~models.transformer_temporal.TransformerTemporalModelOutput`] is
                returned, otherwise a `tuple` where the first element is the sample tensor.
        """

        # 1. Input
        batch_frames, _, height, width = hidden_states.shape
        num_frames = image_only_indicator.shape[-1]
        batch_size = batch_frames // num_frames

        def spatial2time(time_context):
            # print(time_context.shape)

            time_context = time_context.reshape(
                batch_size, num_frames, time_context.shape[-2], time_context.shape[-1]
            )
            time_context = time_context.mean(dim=(1,), keepdim=True)

            # time_context = time_context.flatten(1,2)
            # time_context = time_context[:, None].repeat(
            #     1, height * width, 1, 1
            # )
            time_context = time_context.repeat(1, height * width, 1, 1)
            time_context = time_context.reshape(
                batch_size * height * width, -1, time_context.shape[-1]
            )
            # print(time_context.shape)
            return time_context

        # clip_context, ip_contexts = encoder_hidden_states
        # clip_context_new = spatial2time(clip_context)
        # ip_contexts_new = []
        # for ip_context in ip_contexts:
        #     ip_context_new = spatial2time(ip_context)
        #     ip_contexts_new.append(ip_context_new)

        if isinstance(encoder_hidden_states, tuple):
            clip_hidden_states, ip_hidden_states = encoder_hidden_states
            encoder_hidden_states_time = (
                spatial2time(clip_hidden_states),
                [spatial2time(ip_hidden_state) for ip_hidden_state in ip_hidden_states],
            )
        else:
            encoder_hidden_states_time = spatial2time(encoder_hidden_states)

        residual = hidden_states

        hidden_states = self.norm(hidden_states)
        inner_dim = hidden_states.shape[1]
        hidden_states = hidden_states.permute(0, 2, 3, 1).reshape(
            batch_frames, height * width, inner_dim
        )
        hidden_states = self.proj_in(hidden_states)

        num_frames_emb = torch.arange(num_frames, device=hidden_states.device)
        num_frames_emb = num_frames_emb
        num_frames_emb = num_frames_emb.repeat(batch_size, 1)
        num_frames_emb = num_frames_emb.reshape(-1)
        t_emb = self.time_proj(num_frames_emb)
        # import ipdb
        # ipdb.set_trace()

        # `Timesteps` does not contain any weights and will always return f32 tensors
        # but time_embedding might actually be running in fp16. so we need to cast here.
        # there might be better ways to encapsulate this.
        t_emb = t_emb.to(dtype=hidden_states.dtype)

        emb = self.time_pos_embed(t_emb)
        emb = emb[:, None, :]
        # print(self.time_mixer.alpha)
        # 2. Blocks
        for block, mamba_block, temporal_block in zip(
            self.transformer_blocks, self.mamba_blocks, self.temporal_transformer_blocks
        ):
            if self.training and self.gradient_checkpointing:
                hidden_states = torch.utils.checkpoint.checkpoint(
                    block,
                    hidden_states,
                    None,
                    encoder_hidden_states,
                    None,
                    None,
                    cross_attention_kwargs,
                    use_reentrant=False,
                )
            else:
                hidden_states = block(
                    hidden_states,
                    encoder_hidden_states=encoder_hidden_states,
                    cross_attention_kwargs=cross_attention_kwargs,
                )
            if self.training and self.gradient_checkpointing:
                hidden_states = torch.utils.checkpoint.checkpoint(
                    mamba_block,
                    hidden_states,
                    torch.cat(
                        [
                            encoder_hidden_states[0],
                            encoder_hidden_states[1][0].squeeze(1),
                        ],
                        dim=1,
                    ),
                )
            else:
                hidden_states = mamba_block(
                    hidden_states,
                    torch.cat(
                        [
                            encoder_hidden_states[0],
                            encoder_hidden_states[1][0].squeeze(1),
                        ],
                        dim=1,
                    ),
                )
            hidden_states_mix = hidden_states
            hidden_states_mix = hidden_states_mix + emb
            if self.training and self.gradient_checkpointing:

                hidden_states_mix = torch.utils.checkpoint.checkpoint(
                    temporal_block,
                    hidden_states_mix,
                    num_frames,
                    encoder_hidden_states_time,
                    use_reentrant=False,
                )

            else:
                hidden_states_mix = temporal_block(
                    hidden_states_mix,
                    num_frames=num_frames,
                    encoder_hidden_states=encoder_hidden_states_time,
                )
            hidden_states = self.time_mixer(
                x_spatial=hidden_states,
                x_temporal=hidden_states_mix,
                image_only_indicator=image_only_indicator,
            )

        # 3. Output
        hidden_states = self.proj_out(hidden_states)
        hidden_states = (
            hidden_states.reshape(batch_frames, height, width, inner_dim)
            .permute(0, 3, 1, 2)
            .contiguous()
        )

        output = hidden_states + residual

        if not return_dict:
            return (output,)

        return TransformerTemporalModelOutput(sample=output)


# use the unet feature conditioned by clip feature after spatial attn, 更改了mamba的结构, 在spatial attn后，没有cross attn
class TransformerSpatioTemporalModel_mambaID_v4_wo_cross_attn(nn.Module):
    """
    A Transformer model for video-like data.

    Parameters:
        num_attention_heads (`int`, *optional*, defaults to 16): The number of heads to use for multi-head attention.
        attention_head_dim (`int`, *optional*, defaults to 88): The number of channels in each head.
        in_channels (`int`, *optional*):
            The number of channels in the input and output (specify if the input is **continuous**).
        out_channels (`int`, *optional*):
            The number of channels in the output (specify if the input is **continuous**).
        num_layers (`int`, *optional*, defaults to 1): The number of layers of Transformer blocks to use.
        cross_attention_dim (`int`, *optional*): The number of `encoder_hidden_states` dimensions to use.
    """

    def __init__(
        self,
        num_attention_heads: int = 16,
        attention_head_dim: int = 88,
        in_channels: int = 320,
        out_channels: Optional[int] = None,
        num_layers: int = 1,
        cross_attention_dim: Optional[int] = None,
    ):
        super().__init__()
        self.num_attention_heads = num_attention_heads
        self.attention_head_dim = attention_head_dim

        inner_dim = num_attention_heads * attention_head_dim
        self.inner_dim = inner_dim

        # 2. Define input layers
        self.in_channels = in_channels
        self.norm = torch.nn.GroupNorm(
            num_groups=32, num_channels=in_channels, eps=1e-6
        )
        self.proj_in = nn.Linear(in_channels, inner_dim)

        # 3. Define transformers blocks
        self.transformer_blocks = nn.ModuleList(
            [
                BasicTransformerBlock(
                    inner_dim,
                    num_attention_heads,
                    attention_head_dim,
                )
                for d in range(num_layers)
            ]
        )

        # 3. Define transformers blocks
        # self_attention_cond = SS2D_cond(d_model=320,d_cond=1024, dropout=0.1, d_state=16, size=36, scan_type='scan', num_direction=4)
        # self_attention_cond = SS2D_cond(d_model=320,d_cond=1024,cond_size=32, dropout=0.1, d_state=16, size=72, scan_type='sweep', num_direction=2).cuda()
        self.mamba_blocks = nn.ModuleList(
            [
                SS2D_cond_v4(
                    d_model=in_channels,
                    d_cond=cross_attention_dim,
                    cond_size=32,
                    dropout=0.1,
                    d_state=16,
                    size=int(72 / (in_channels / 320)),
                    scan_type="sweep",
                    num_direction=2,
                )
                for d in range(num_layers)
            ]
        )
        time_mix_inner_dim = inner_dim
        self.temporal_transformer_blocks = nn.ModuleList(
            [
                TemporalBasicTransformerBlock(
                    inner_dim,
                    time_mix_inner_dim,
                    num_attention_heads,
                    attention_head_dim,
                )
                for _ in range(num_layers)
            ]
        )

        time_embed_dim = in_channels * 4
        self.time_pos_embed = TimestepEmbedding(
            in_channels, time_embed_dim, out_dim=in_channels
        )
        self.time_proj = Timesteps(in_channels, True, 0)
        self.time_mixer = AlphaBlender(alpha=0.5, merge_strategy="learned_with_images")

        # 4. Define output layers
        self.out_channels = in_channels if out_channels is None else out_channels
        # TODO: should use out_channels for continuous projections
        self.proj_out = nn.Linear(inner_dim, in_channels)

        self.gradient_checkpointing = False

    def forward(
        self,
        hidden_states: torch.Tensor,
        encoder_hidden_states: Optional[torch.Tensor] = None,
        cross_attention_kwargs: Optional[Dict[str, Any]] = None,
        image_only_indicator: Optional[torch.Tensor] = None,
        return_dict: bool = True,
    ):
        """
        Args:
            hidden_states (`torch.FloatTensor` of shape `(batch size, channel, height, width)`):
                Input hidden_states.
            num_frames (`int`):
                The number of frames to be processed per batch. This is used to reshape the hidden states.
            encoder_hidden_states ( `torch.LongTensor` of shape `(batch size, encoder_hidden_states dim)`, *optional*):
                Conditional embeddings for cross attention layer. If not given, cross-attention defaults to
                self-attention.
            image_only_indicator (`torch.LongTensor` of shape `(batch size, num_frames)`, *optional*):
                A tensor indicating whether the input contains only images. 1 indicates that the input contains only
                images, 0 indicates that the input contains video frames.
            return_dict (`bool`, *optional*, defaults to `True`):
                Whether or not to return a [`~models.transformer_temporal.TransformerTemporalModelOutput`] instead of a plain
                tuple.

        Returns:
            [`~models.transformer_temporal.TransformerTemporalModelOutput`] or `tuple`:
                If `return_dict` is True, an [`~models.transformer_temporal.TransformerTemporalModelOutput`] is
                returned, otherwise a `tuple` where the first element is the sample tensor.
        """

        # 1. Input
        batch_frames, _, height, width = hidden_states.shape
        num_frames = image_only_indicator.shape[-1]
        batch_size = batch_frames // num_frames

        def spatial2time(time_context):
            # print(time_context.shape)

            time_context = time_context.reshape(
                batch_size, num_frames, time_context.shape[-2], time_context.shape[-1]
            )
            time_context = time_context.mean(dim=(1,), keepdim=True)

            # time_context = time_context.flatten(1,2)
            # time_context = time_context[:, None].repeat(
            #     1, height * width, 1, 1
            # )
            time_context = time_context.repeat(1, height * width, 1, 1)
            time_context = time_context.reshape(
                batch_size * height * width, -1, time_context.shape[-1]
            )
            # print(time_context.shape)
            return time_context

        # clip_context, ip_contexts = encoder_hidden_states
        # clip_context_new = spatial2time(clip_context)
        # ip_contexts_new = []
        # for ip_context in ip_contexts:
        #     ip_context_new = spatial2time(ip_context)
        #     ip_contexts_new.append(ip_context_new)

        if isinstance(encoder_hidden_states, tuple):
            clip_hidden_states, ip_hidden_states = encoder_hidden_states
            encoder_hidden_states_time = (
                spatial2time(clip_hidden_states),
                [spatial2time(ip_hidden_state) for ip_hidden_state in ip_hidden_states],
            )
        else:
            encoder_hidden_states_time = spatial2time(encoder_hidden_states)

        residual = hidden_states

        hidden_states = self.norm(hidden_states)
        inner_dim = hidden_states.shape[1]
        hidden_states = hidden_states.permute(0, 2, 3, 1).reshape(
            batch_frames, height * width, inner_dim
        )
        hidden_states = self.proj_in(hidden_states)

        num_frames_emb = torch.arange(num_frames, device=hidden_states.device)
        num_frames_emb = num_frames_emb
        num_frames_emb = num_frames_emb.repeat(batch_size, 1)
        num_frames_emb = num_frames_emb.reshape(-1)
        t_emb = self.time_proj(num_frames_emb)
        # import ipdb
        # ipdb.set_trace()

        # `Timesteps` does not contain any weights and will always return f32 tensors
        # but time_embedding might actually be running in fp16. so we need to cast here.
        # there might be better ways to encapsulate this.
        t_emb = t_emb.to(dtype=hidden_states.dtype)

        emb = self.time_pos_embed(t_emb)
        emb = emb[:, None, :]
        # print(self.time_mixer.alpha)
        # 2. Blocks
        for block, mamba_block, temporal_block in zip(
            self.transformer_blocks, self.mamba_blocks, self.temporal_transformer_blocks
        ):
            if self.training and self.gradient_checkpointing:
                hidden_states = torch.utils.checkpoint.checkpoint(
                    block,
                    hidden_states,
                    None,
                    encoder_hidden_states,
                    None,
                    None,
                    cross_attention_kwargs,
                    use_reentrant=False,
                )
            else:
                hidden_states = block(
                    hidden_states,
                    encoder_hidden_states=encoder_hidden_states,
                    cross_attention_kwargs=cross_attention_kwargs,
                )
            if self.training and self.gradient_checkpointing:
                hidden_states = torch.utils.checkpoint.checkpoint(
                    mamba_block,
                    hidden_states,
                    torch.cat(
                        [
                            encoder_hidden_states[0],
                            encoder_hidden_states[1][0].squeeze(1),
                        ],
                        dim=1,
                    ),
                )
            else:
                hidden_states = mamba_block(
                    hidden_states,
                    torch.cat(
                        [
                            encoder_hidden_states[0],
                            encoder_hidden_states[1][0].squeeze(1),
                        ],
                        dim=1,
                    ),
                )
            hidden_states_mix = hidden_states
            hidden_states_mix = hidden_states_mix + emb
            if self.training and self.gradient_checkpointing:

                hidden_states_mix = torch.utils.checkpoint.checkpoint(
                    temporal_block,
                    hidden_states_mix,
                    num_frames,
                    encoder_hidden_states_time,
                    use_reentrant=False,
                )

            else:
                hidden_states_mix = temporal_block(
                    hidden_states_mix,
                    num_frames=num_frames,
                    encoder_hidden_states=encoder_hidden_states_time,
                )
            hidden_states = self.time_mixer(
                x_spatial=hidden_states,
                x_temporal=hidden_states_mix,
                image_only_indicator=image_only_indicator,
            )

        # 3. Output
        hidden_states = self.proj_out(hidden_states)
        hidden_states = (
            hidden_states.reshape(batch_frames, height, width, inner_dim)
            .permute(0, 3, 1, 2)
            .contiguous()
        )

        output = hidden_states + residual

        if not return_dict:
            return (output,)

        return TransformerTemporalModelOutput(sample=output)


# use the unet feature conditioned by clip feature after spatial attn, 更改了mamba的结构
class TransformerSpatioTemporalModel_mambaID_v5(nn.Module):
    """
    A Transformer model for video-like data.

    Parameters:
        num_attention_heads (`int`, *optional*, defaults to 16): The number of heads to use for multi-head attention.
        attention_head_dim (`int`, *optional*, defaults to 88): The number of channels in each head.
        in_channels (`int`, *optional*):
            The number of channels in the input and output (specify if the input is **continuous**).
        out_channels (`int`, *optional*):
            The number of channels in the output (specify if the input is **continuous**).
        num_layers (`int`, *optional*, defaults to 1): The number of layers of Transformer blocks to use.
        cross_attention_dim (`int`, *optional*): The number of `encoder_hidden_states` dimensions to use.
    """

    def __init__(
        self,
        num_attention_heads: int = 16,
        attention_head_dim: int = 88,
        in_channels: int = 320,
        out_channels: Optional[int] = None,
        num_layers: int = 1,
        cross_attention_dim: Optional[int] = None,
    ):
        super().__init__()
        self.num_attention_heads = num_attention_heads
        self.attention_head_dim = attention_head_dim

        inner_dim = num_attention_heads * attention_head_dim
        self.inner_dim = inner_dim

        # 2. Define input layers
        self.in_channels = in_channels
        self.norm = torch.nn.GroupNorm(
            num_groups=32, num_channels=in_channels, eps=1e-6
        )
        self.proj_in = nn.Linear(in_channels, inner_dim)

        # 3. Define transformers blocks
        self.transformer_blocks = nn.ModuleList(
            [
                BasicTransformerBlock(
                    inner_dim,
                    num_attention_heads,
                    attention_head_dim,
                    cross_attention_dim=cross_attention_dim,
                )
                for d in range(num_layers)
            ]
        )

        # 3. Define transformers blocks
        # self_attention_cond = SS2D_cond(d_model=320,d_cond=1024, dropout=0.1, d_state=16, size=36, scan_type='scan', num_direction=4)
        # self_attention_cond = SS2D_cond(d_model=320,d_cond=1024,cond_size=32, dropout=0.1, d_state=16, size=72, scan_type='sweep', num_direction=2).cuda()
        self.mamba_blocks = nn.ModuleList(
            [
                SS2D_cond_v5(
                    d_model=in_channels,
                    d_cond=cross_attention_dim,
                    cond_size=32,
                    dropout=0.1,
                    d_state=16,
                    size=int(72 / (in_channels / 320)),
                    scan_type="sweep",
                    num_direction=2,
                )
                for d in range(num_layers)
            ]
        )
        time_mix_inner_dim = inner_dim
        self.temporal_transformer_blocks = nn.ModuleList(
            [
                TemporalBasicTransformerBlock(
                    inner_dim,
                    time_mix_inner_dim,
                    num_attention_heads,
                    attention_head_dim,
                    cross_attention_dim=cross_attention_dim,
                )
                for _ in range(num_layers)
            ]
        )

        time_embed_dim = in_channels * 4
        self.time_pos_embed = TimestepEmbedding(
            in_channels, time_embed_dim, out_dim=in_channels
        )
        self.time_proj = Timesteps(in_channels, True, 0)
        self.time_mixer = AlphaBlender(alpha=0.5, merge_strategy="learned_with_images")

        # 4. Define output layers
        self.out_channels = in_channels if out_channels is None else out_channels
        # TODO: should use out_channels for continuous projections
        self.proj_out = nn.Linear(inner_dim, in_channels)

        self.gradient_checkpointing = False

    def forward(
        self,
        hidden_states: torch.Tensor,
        encoder_hidden_states: Optional[torch.Tensor] = None,
        cross_attention_kwargs: Optional[Dict[str, Any]] = None,
        image_only_indicator: Optional[torch.Tensor] = None,
        return_dict: bool = True,
    ):
        """
        Args:
            hidden_states (`torch.FloatTensor` of shape `(batch size, channel, height, width)`):
                Input hidden_states.
            num_frames (`int`):
                The number of frames to be processed per batch. This is used to reshape the hidden states.
            encoder_hidden_states ( `torch.LongTensor` of shape `(batch size, encoder_hidden_states dim)`, *optional*):
                Conditional embeddings for cross attention layer. If not given, cross-attention defaults to
                self-attention.
            image_only_indicator (`torch.LongTensor` of shape `(batch size, num_frames)`, *optional*):
                A tensor indicating whether the input contains only images. 1 indicates that the input contains only
                images, 0 indicates that the input contains video frames.
            return_dict (`bool`, *optional*, defaults to `True`):
                Whether or not to return a [`~models.transformer_temporal.TransformerTemporalModelOutput`] instead of a plain
                tuple.

        Returns:
            [`~models.transformer_temporal.TransformerTemporalModelOutput`] or `tuple`:
                If `return_dict` is True, an [`~models.transformer_temporal.TransformerTemporalModelOutput`] is
                returned, otherwise a `tuple` where the first element is the sample tensor.
        """

        # 1. Input
        batch_frames, _, height, width = hidden_states.shape
        num_frames = image_only_indicator.shape[-1]
        batch_size = batch_frames // num_frames

        def spatial2time(time_context):
            # print(time_context.shape)

            time_context = time_context.reshape(
                batch_size, num_frames, time_context.shape[-2], time_context.shape[-1]
            )
            time_context = time_context.mean(dim=(1,), keepdim=True)

            # time_context = time_context.flatten(1,2)
            # time_context = time_context[:, None].repeat(
            #     1, height * width, 1, 1
            # )
            time_context = time_context.repeat(1, height * width, 1, 1)
            time_context = time_context.reshape(
                batch_size * height * width, -1, time_context.shape[-1]
            )
            # print(time_context.shape)
            return time_context

        # clip_context, ip_contexts = encoder_hidden_states
        # clip_context_new = spatial2time(clip_context)
        # ip_contexts_new = []
        # for ip_context in ip_contexts:
        #     ip_context_new = spatial2time(ip_context)
        #     ip_contexts_new.append(ip_context_new)

        if isinstance(encoder_hidden_states, tuple):
            clip_hidden_states, ip_hidden_states = encoder_hidden_states
            encoder_hidden_states_time = (
                spatial2time(clip_hidden_states),
                [spatial2time(ip_hidden_state) for ip_hidden_state in ip_hidden_states],
            )
        else:
            encoder_hidden_states_time = spatial2time(encoder_hidden_states)

        residual = hidden_states

        hidden_states = self.norm(hidden_states)
        inner_dim = hidden_states.shape[1]
        hidden_states = hidden_states.permute(0, 2, 3, 1).reshape(
            batch_frames, height * width, inner_dim
        )
        hidden_states = self.proj_in(hidden_states)

        num_frames_emb = torch.arange(num_frames, device=hidden_states.device)
        num_frames_emb = num_frames_emb
        num_frames_emb = num_frames_emb.repeat(batch_size, 1)
        num_frames_emb = num_frames_emb.reshape(-1)
        t_emb = self.time_proj(num_frames_emb)
        # import ipdb
        # ipdb.set_trace()

        # `Timesteps` does not contain any weights and will always return f32 tensors
        # but time_embedding might actually be running in fp16. so we need to cast here.
        # there might be better ways to encapsulate this.
        t_emb = t_emb.to(dtype=hidden_states.dtype)

        emb = self.time_pos_embed(t_emb)
        emb = emb[:, None, :]
        # print(self.time_mixer.alpha)
        # 2. Blocks
        for block, mamba_block, temporal_block in zip(
            self.transformer_blocks, self.mamba_blocks, self.temporal_transformer_blocks
        ):
            if self.training and self.gradient_checkpointing:
                hidden_states = torch.utils.checkpoint.checkpoint(
                    block,
                    hidden_states,
                    None,
                    encoder_hidden_states,
                    None,
                    None,
                    cross_attention_kwargs,
                    use_reentrant=False,
                )
            else:
                hidden_states = block(
                    hidden_states,
                    encoder_hidden_states=encoder_hidden_states,
                    cross_attention_kwargs=cross_attention_kwargs,
                )
            if self.training and self.gradient_checkpointing:
                hidden_states = torch.utils.checkpoint.checkpoint(
                    mamba_block,
                    hidden_states,
                    torch.cat(
                        [
                            encoder_hidden_states[0],
                            encoder_hidden_states[1][0].squeeze(1),
                        ],
                        dim=1,
                    ),
                )
            else:
                hidden_states = mamba_block(
                    hidden_states,
                    torch.cat(
                        [
                            encoder_hidden_states[0],
                            encoder_hidden_states[1][0].squeeze(1),
                        ],
                        dim=1,
                    ),
                )
            hidden_states_mix = hidden_states
            hidden_states_mix = hidden_states_mix + emb
            if self.training and self.gradient_checkpointing:

                hidden_states_mix = torch.utils.checkpoint.checkpoint(
                    temporal_block,
                    hidden_states_mix,
                    num_frames,
                    encoder_hidden_states_time,
                    use_reentrant=False,
                )

            else:
                hidden_states_mix = temporal_block(
                    hidden_states_mix,
                    num_frames=num_frames,
                    encoder_hidden_states=encoder_hidden_states_time,
                )
            hidden_states = self.time_mixer(
                x_spatial=hidden_states,
                x_temporal=hidden_states_mix,
                image_only_indicator=image_only_indicator,
            )

        # 3. Output
        hidden_states = self.proj_out(hidden_states)
        hidden_states = (
            hidden_states.reshape(batch_frames, height, width, inner_dim)
            .permute(0, 3, 1, 2)
            .contiguous()
        )

        output = hidden_states + residual

        if not return_dict:
            return (output,)

        return TransformerTemporalModelOutput(sample=output)


# use the unet feature conditioned by clip feature after spatial attn, 更改了mamba的结构, 自己做一次ssd，再和cond_ssm做一次ssd
class TransformerSpatioTemporalModel_mambaID_v6(nn.Module):
    """
    A Transformer model for video-like data.

    Parameters:
        num_attention_heads (`int`, *optional*, defaults to 16): The number of heads to use for multi-head attention.
        attention_head_dim (`int`, *optional*, defaults to 88): The number of channels in each head.
        in_channels (`int`, *optional*):
            The number of channels in the input and output (specify if the input is **continuous**).
        out_channels (`int`, *optional*):
            The number of channels in the output (specify if the input is **continuous**).
        num_layers (`int`, *optional*, defaults to 1): The number of layers of Transformer blocks to use.
        cross_attention_dim (`int`, *optional*): The number of `encoder_hidden_states` dimensions to use.
    """

    def __init__(
        self,
        num_attention_heads: int = 16,
        attention_head_dim: int = 88,
        in_channels: int = 320,
        out_channels: Optional[int] = None,
        num_layers: int = 1,
        cross_attention_dim: Optional[int] = None,
    ):
        super().__init__()
        self.num_attention_heads = num_attention_heads
        self.attention_head_dim = attention_head_dim

        inner_dim = num_attention_heads * attention_head_dim
        self.inner_dim = inner_dim

        # 2. Define input layers
        self.in_channels = in_channels
        self.norm = torch.nn.GroupNorm(
            num_groups=32, num_channels=in_channels, eps=1e-6
        )
        self.proj_in = nn.Linear(in_channels, inner_dim)

        # 3. Define transformers blocks
        self.transformer_blocks = nn.ModuleList(
            [
                BasicTransformerBlock(
                    inner_dim,
                    num_attention_heads,
                    attention_head_dim,
                    cross_attention_dim=cross_attention_dim,
                )
                for d in range(num_layers)
            ]
        )

        # 3. Define transformers blocks
        # self_attention_cond = SS2D_cond(d_model=320,d_cond=1024, dropout=0.1, d_state=16, size=36, scan_type='scan', num_direction=4)
        # self_attention_cond = SS2D_cond(d_model=320,d_cond=1024,cond_size=32, dropout=0.1, d_state=16, size=72, scan_type='sweep', num_direction=2).cuda()
        self.mamba_blocks = nn.ModuleList(
            [
                SS2D_cond_v6(
                    d_model=in_channels,
                    d_cond=cross_attention_dim,
                    cond_size=32,
                    dropout=0.1,
                    d_state=16,
                    size=int(72 / (in_channels / 320)),
                    scan_type="sweep",
                    num_direction=2,
                )
                for d in range(num_layers)
            ]
        )
        time_mix_inner_dim = inner_dim
        self.temporal_transformer_blocks = nn.ModuleList(
            [
                TemporalBasicTransformerBlock(
                    inner_dim,
                    time_mix_inner_dim,
                    num_attention_heads,
                    attention_head_dim,
                    cross_attention_dim=cross_attention_dim,
                )
                for _ in range(num_layers)
            ]
        )

        time_embed_dim = in_channels * 4
        self.time_pos_embed = TimestepEmbedding(
            in_channels, time_embed_dim, out_dim=in_channels
        )
        self.time_proj = Timesteps(in_channels, True, 0)
        self.time_mixer = AlphaBlender(alpha=0.5, merge_strategy="learned_with_images")

        # 4. Define output layers
        self.out_channels = in_channels if out_channels is None else out_channels
        # TODO: should use out_channels for continuous projections
        self.proj_out = nn.Linear(inner_dim, in_channels)

        self.gradient_checkpointing = False

    def forward(
        self,
        hidden_states: torch.Tensor,
        encoder_hidden_states: Optional[torch.Tensor] = None,
        cross_attention_kwargs: Optional[Dict[str, Any]] = None,
        image_only_indicator: Optional[torch.Tensor] = None,
        return_dict: bool = True,
    ):
        """
        Args:
            hidden_states (`torch.FloatTensor` of shape `(batch size, channel, height, width)`):
                Input hidden_states.
            num_frames (`int`):
                The number of frames to be processed per batch. This is used to reshape the hidden states.
            encoder_hidden_states ( `torch.LongTensor` of shape `(batch size, encoder_hidden_states dim)`, *optional*):
                Conditional embeddings for cross attention layer. If not given, cross-attention defaults to
                self-attention.
            image_only_indicator (`torch.LongTensor` of shape `(batch size, num_frames)`, *optional*):
                A tensor indicating whether the input contains only images. 1 indicates that the input contains only
                images, 0 indicates that the input contains video frames.
            return_dict (`bool`, *optional*, defaults to `True`):
                Whether or not to return a [`~models.transformer_temporal.TransformerTemporalModelOutput`] instead of a plain
                tuple.

        Returns:
            [`~models.transformer_temporal.TransformerTemporalModelOutput`] or `tuple`:
                If `return_dict` is True, an [`~models.transformer_temporal.TransformerTemporalModelOutput`] is
                returned, otherwise a `tuple` where the first element is the sample tensor.
        """

        # 1. Input
        batch_frames, _, height, width = hidden_states.shape
        num_frames = image_only_indicator.shape[-1]
        batch_size = batch_frames // num_frames

        def spatial2time(time_context):
            # print(time_context.shape)

            time_context = time_context.reshape(
                batch_size, num_frames, time_context.shape[-2], time_context.shape[-1]
            )
            time_context = time_context.mean(dim=(1,), keepdim=True)

            # time_context = time_context.flatten(1,2)
            # time_context = time_context[:, None].repeat(
            #     1, height * width, 1, 1
            # )
            time_context = time_context.repeat(1, height * width, 1, 1)
            time_context = time_context.reshape(
                batch_size * height * width, -1, time_context.shape[-1]
            )
            # print(time_context.shape)
            return time_context

        # clip_context, ip_contexts = encoder_hidden_states
        # clip_context_new = spatial2time(clip_context)
        # ip_contexts_new = []
        # for ip_context in ip_contexts:
        #     ip_context_new = spatial2time(ip_context)
        #     ip_contexts_new.append(ip_context_new)

        if isinstance(encoder_hidden_states, tuple):
            clip_hidden_states, ip_hidden_states = encoder_hidden_states
            encoder_hidden_states_time = (
                spatial2time(clip_hidden_states),
                [spatial2time(ip_hidden_state) for ip_hidden_state in ip_hidden_states],
            )
        else:
            encoder_hidden_states_time = spatial2time(encoder_hidden_states)

        residual = hidden_states

        hidden_states = self.norm(hidden_states)
        inner_dim = hidden_states.shape[1]
        hidden_states = hidden_states.permute(0, 2, 3, 1).reshape(
            batch_frames, height * width, inner_dim
        )
        hidden_states = self.proj_in(hidden_states)

        num_frames_emb = torch.arange(num_frames, device=hidden_states.device)
        num_frames_emb = num_frames_emb
        num_frames_emb = num_frames_emb.repeat(batch_size, 1)
        num_frames_emb = num_frames_emb.reshape(-1)
        t_emb = self.time_proj(num_frames_emb)
        # import ipdb
        # ipdb.set_trace()

        # `Timesteps` does not contain any weights and will always return f32 tensors
        # but time_embedding might actually be running in fp16. so we need to cast here.
        # there might be better ways to encapsulate this.
        t_emb = t_emb.to(dtype=hidden_states.dtype)

        emb = self.time_pos_embed(t_emb)
        emb = emb[:, None, :]
        # print(self.time_mixer.alpha)
        # 2. Blocks
        for block, mamba_block, temporal_block in zip(
            self.transformer_blocks, self.mamba_blocks, self.temporal_transformer_blocks
        ):
            if self.training and self.gradient_checkpointing:
                hidden_states = torch.utils.checkpoint.checkpoint(
                    block,
                    hidden_states,
                    None,
                    encoder_hidden_states,
                    None,
                    None,
                    cross_attention_kwargs,
                    use_reentrant=False,
                )
            else:
                hidden_states = block(
                    hidden_states,
                    encoder_hidden_states=encoder_hidden_states,
                    cross_attention_kwargs=cross_attention_kwargs,
                )
            if self.training and self.gradient_checkpointing:
                hidden_states = torch.utils.checkpoint.checkpoint(
                    mamba_block,
                    hidden_states,
                    torch.cat(
                        [
                            encoder_hidden_states[0],
                            encoder_hidden_states[1][0].squeeze(1),
                        ],
                        dim=1,
                    ),
                )
            else:
                hidden_states = mamba_block(
                    hidden_states,
                    torch.cat(
                        [
                            encoder_hidden_states[0],
                            encoder_hidden_states[1][0].squeeze(1),
                        ],
                        dim=1,
                    ),
                )
            hidden_states_mix = hidden_states
            hidden_states_mix = hidden_states_mix + emb
            if self.training and self.gradient_checkpointing:

                hidden_states_mix = torch.utils.checkpoint.checkpoint(
                    temporal_block,
                    hidden_states_mix,
                    num_frames,
                    encoder_hidden_states_time,
                    use_reentrant=False,
                )

            else:
                hidden_states_mix = temporal_block(
                    hidden_states_mix,
                    num_frames=num_frames,
                    encoder_hidden_states=encoder_hidden_states_time,
                )
            hidden_states = self.time_mixer(
                x_spatial=hidden_states,
                x_temporal=hidden_states_mix,
                image_only_indicator=image_only_indicator,
            )

        # 3. Output
        hidden_states = self.proj_out(hidden_states)
        hidden_states = (
            hidden_states.reshape(batch_frames, height, width, inner_dim)
            .permute(0, 3, 1, 2)
            .contiguous()
        )

        output = hidden_states + residual

        if not return_dict:
            return (output,)

        return TransformerTemporalModelOutput(sample=output)


# 在v4的基础上，调用v7, v7和v4一样，只不过是把参数放到forward中
class TransformerSpatioTemporalModel_mambaID_v7(nn.Module):
    """
    A Transformer model for video-like data.

    Parameters:
        num_attention_heads (`int`, *optional*, defaults to 16): The number of heads to use for multi-head attention.
        attention_head_dim (`int`, *optional*, defaults to 88): The number of channels in each head.
        in_channels (`int`, *optional*):
            The number of channels in the input and output (specify if the input is **continuous**).
        out_channels (`int`, *optional*):
            The number of channels in the output (specify if the input is **continuous**).
        num_layers (`int`, *optional*, defaults to 1): The number of layers of Transformer blocks to use.
        cross_attention_dim (`int`, *optional*): The number of `encoder_hidden_states` dimensions to use.
    """

    def __init__(
        self,
        num_attention_heads: int = 16,
        attention_head_dim: int = 88,
        in_channels: int = 320,
        out_channels: Optional[int] = None,
        num_layers: int = 1,
        cross_attention_dim: Optional[int] = None,
    ):
        super().__init__()
        self.num_attention_heads = num_attention_heads
        self.attention_head_dim = attention_head_dim

        inner_dim = num_attention_heads * attention_head_dim
        self.inner_dim = inner_dim

        # 2. Define input layers
        self.in_channels = in_channels
        self.norm = torch.nn.GroupNorm(
            num_groups=32, num_channels=in_channels, eps=1e-6
        )
        self.proj_in = nn.Linear(in_channels, inner_dim)

        # 3. Define transformers blocks
        self.transformer_blocks = nn.ModuleList(
            [
                BasicTransformerBlock(
                    inner_dim,
                    num_attention_heads,
                    attention_head_dim,
                    cross_attention_dim=cross_attention_dim,
                )
                for d in range(num_layers)
            ]
        )

        # 3. Define transformers blocks
        # self_attention_cond = SS2D_cond(d_model=320,d_cond=1024, dropout=0.1, d_state=16, size=36, scan_type='scan', num_direction=4)
        # self_attention_cond = SS2D_cond(d_model=320,d_cond=1024,cond_size=32, dropout=0.1, d_state=16, size=72, scan_type='sweep', num_direction=2).cuda()
        self.mamba_blocks = nn.ModuleList(
            [
                SS2D_cond_v4(
                    d_model=in_channels,
                    d_cond=cross_attention_dim,
                    cond_size=32,
                    dropout=0.1,
                    d_state=16,
                    size=int(72 / (in_channels / 320)),
                    scan_type="sweep",
                    num_direction=2,
                )
                for d in range(num_layers)
            ]
        )
        time_mix_inner_dim = inner_dim
        self.temporal_transformer_blocks = nn.ModuleList(
            [
                TemporalBasicTransformerBlock(
                    inner_dim,
                    time_mix_inner_dim,
                    num_attention_heads,
                    attention_head_dim,
                    cross_attention_dim=cross_attention_dim,
                )
                for _ in range(num_layers)
            ]
        )

        time_embed_dim = in_channels * 4
        self.time_pos_embed = TimestepEmbedding(
            in_channels, time_embed_dim, out_dim=in_channels
        )
        self.time_proj = Timesteps(in_channels, True, 0)
        self.time_mixer = AlphaBlender(alpha=0.5, merge_strategy="learned_with_images")

        # 4. Define output layers
        self.out_channels = in_channels if out_channels is None else out_channels
        # TODO: should use out_channels for continuous projections
        self.proj_out = nn.Linear(inner_dim, in_channels)

        self.gradient_checkpointing = False

    def forward(
        self,
        hidden_states: torch.Tensor,
        encoder_hidden_states: Optional[torch.Tensor] = None,
        cross_attention_kwargs: Optional[Dict[str, Any]] = None,
        image_only_indicator: Optional[torch.Tensor] = None,
        return_dict: bool = True,
    ):
        """
        Args:
            hidden_states (`torch.FloatTensor` of shape `(batch size, channel, height, width)`):
                Input hidden_states.
            num_frames (`int`):
                The number of frames to be processed per batch. This is used to reshape the hidden states.
            encoder_hidden_states ( `torch.LongTensor` of shape `(batch size, encoder_hidden_states dim)`, *optional*):
                Conditional embeddings for cross attention layer. If not given, cross-attention defaults to
                self-attention.
            image_only_indicator (`torch.LongTensor` of shape `(batch size, num_frames)`, *optional*):
                A tensor indicating whether the input contains only images. 1 indicates that the input contains only
                images, 0 indicates that the input contains video frames.
            return_dict (`bool`, *optional*, defaults to `True`):
                Whether or not to return a [`~models.transformer_temporal.TransformerTemporalModelOutput`] instead of a plain
                tuple.

        Returns:
            [`~models.transformer_temporal.TransformerTemporalModelOutput`] or `tuple`:
                If `return_dict` is True, an [`~models.transformer_temporal.TransformerTemporalModelOutput`] is
                returned, otherwise a `tuple` where the first element is the sample tensor.
        """

        # 1. Input
        batch_frames, _, height, width = hidden_states.shape
        num_frames = image_only_indicator.shape[-1]
        batch_size = batch_frames // num_frames

        def spatial2time(time_context):
            # print(time_context.shape)

            time_context = time_context.reshape(
                batch_size, num_frames, time_context.shape[-2], time_context.shape[-1]
            )
            time_context = time_context.mean(dim=(1,), keepdim=True)

            # time_context = time_context.flatten(1,2)
            # time_context = time_context[:, None].repeat(
            #     1, height * width, 1, 1
            # )
            time_context = time_context.repeat(1, height * width, 1, 1)
            time_context = time_context.reshape(
                batch_size * height * width, -1, time_context.shape[-1]
            )
            # print(time_context.shape)
            return time_context

        # clip_context, ip_contexts = encoder_hidden_states
        # clip_context_new = spatial2time(clip_context)
        # ip_contexts_new = []
        # for ip_context in ip_contexts:
        #     ip_context_new = spatial2time(ip_context)
        #     ip_contexts_new.append(ip_context_new)

        if isinstance(encoder_hidden_states, tuple):
            clip_hidden_states, ip_hidden_states = encoder_hidden_states
            encoder_hidden_states_time = (
                spatial2time(clip_hidden_states),
                [spatial2time(ip_hidden_state) for ip_hidden_state in ip_hidden_states],
            )
        else:
            encoder_hidden_states_time = spatial2time(encoder_hidden_states)

        residual = hidden_states

        hidden_states = self.norm(hidden_states)
        inner_dim = hidden_states.shape[1]
        hidden_states = hidden_states.permute(0, 2, 3, 1).reshape(
            batch_frames, height * width, inner_dim
        )
        hidden_states = self.proj_in(hidden_states)

        num_frames_emb = torch.arange(num_frames, device=hidden_states.device)
        num_frames_emb = num_frames_emb
        num_frames_emb = num_frames_emb.repeat(batch_size, 1)
        num_frames_emb = num_frames_emb.reshape(-1)
        t_emb = self.time_proj(num_frames_emb)
        # import ipdb
        # ipdb.set_trace()

        # `Timesteps` does not contain any weights and will always return f32 tensors
        # but time_embedding might actually be running in fp16. so we need to cast here.
        # there might be better ways to encapsulate this.
        t_emb = t_emb.to(dtype=hidden_states.dtype)

        emb = self.time_pos_embed(t_emb)
        emb = emb[:, None, :]
        # print(self.time_mixer.alpha)
        # 2. Blocks
        for block, mamba_block, temporal_block in zip(
            self.transformer_blocks, self.mamba_blocks, self.temporal_transformer_blocks
        ):
            if self.training and self.gradient_checkpointing:
                hidden_states = torch.utils.checkpoint.checkpoint(
                    block,
                    hidden_states,
                    None,
                    encoder_hidden_states,
                    None,
                    None,
                    cross_attention_kwargs,
                    use_reentrant=False,
                )
            else:
                hidden_states = block(
                    hidden_states,
                    encoder_hidden_states=encoder_hidden_states,
                    cross_attention_kwargs=cross_attention_kwargs,
                )
            if self.training and self.gradient_checkpointing:
                hidden_states = torch.utils.checkpoint.checkpoint(
                    mamba_block,
                    hidden_states,
                    torch.cat(
                        [
                            encoder_hidden_states[0],
                            encoder_hidden_states[1][0].squeeze(1),
                        ],
                        dim=1,
                    ),
                )
            else:
                hidden_states = mamba_block(
                    hidden_states,
                    torch.cat(
                        [
                            encoder_hidden_states[0],
                            encoder_hidden_states[1][0].squeeze(1),
                        ],
                        dim=1,
                    ),
                )
            hidden_states_mix = hidden_states
            hidden_states_mix = hidden_states_mix + emb
            if self.training and self.gradient_checkpointing:

                hidden_states_mix = torch.utils.checkpoint.checkpoint(
                    temporal_block,
                    hidden_states_mix,
                    num_frames,
                    encoder_hidden_states_time,
                    use_reentrant=False,
                )

            else:
                hidden_states_mix = temporal_block(
                    hidden_states_mix,
                    num_frames=num_frames,
                    encoder_hidden_states=encoder_hidden_states_time,
                )
            hidden_states = self.time_mixer(
                x_spatial=hidden_states,
                x_temporal=hidden_states_mix,
                image_only_indicator=image_only_indicator,
            )

        # 3. Output
        hidden_states = self.proj_out(hidden_states)
        hidden_states = (
            hidden_states.reshape(batch_frames, height, width, inner_dim)
            .permute(0, 3, 1, 2)
            .contiguous()
        )

        output = hidden_states + residual

        if not return_dict:
            return (output,)

        return TransformerTemporalModelOutput(sample=output)


# ablation
# use the unet feature conditioned by clip feature after spatial attn, 更改了mamba的结构
class TransformerSpatioTemporalModel_mambaID_v4_wo_audio(nn.Module):
    """
    A Transformer model for video-like data.

    Parameters:
        num_attention_heads (`int`, *optional*, defaults to 16): The number of heads to use for multi-head attention.
        attention_head_dim (`int`, *optional*, defaults to 88): The number of channels in each head.
        in_channels (`int`, *optional*):
            The number of channels in the input and output (specify if the input is **continuous**).
        out_channels (`int`, *optional*):
            The number of channels in the output (specify if the input is **continuous**).
        num_layers (`int`, *optional*, defaults to 1): The number of layers of Transformer blocks to use.
        cross_attention_dim (`int`, *optional*): The number of `encoder_hidden_states` dimensions to use.
    """

    def __init__(
        self,
        num_attention_heads: int = 16,
        attention_head_dim: int = 88,
        in_channels: int = 320,
        out_channels: Optional[int] = None,
        num_layers: int = 1,
        cross_attention_dim: Optional[int] = None,
    ):
        super().__init__()
        self.num_attention_heads = num_attention_heads
        self.attention_head_dim = attention_head_dim

        inner_dim = num_attention_heads * attention_head_dim
        self.inner_dim = inner_dim

        # 2. Define input layers
        self.in_channels = in_channels
        self.norm = torch.nn.GroupNorm(
            num_groups=32, num_channels=in_channels, eps=1e-6
        )
        self.proj_in = nn.Linear(in_channels, inner_dim)

        # 3. Define transformers blocks
        self.transformer_blocks = nn.ModuleList(
            [
                BasicTransformerBlock(
                    inner_dim,
                    num_attention_heads,
                    attention_head_dim,
                    cross_attention_dim=cross_attention_dim,
                )
                for d in range(num_layers)
            ]
        )

        # 3. Define transformers blocks
        # self_attention_cond = SS2D_cond(d_model=320,d_cond=1024, dropout=0.1, d_state=16, size=36, scan_type='scan', num_direction=4)
        # self_attention_cond = SS2D_cond(d_model=320,d_cond=1024,cond_size=32, dropout=0.1, d_state=16, size=72, scan_type='sweep', num_direction=2).cuda()
        self.mamba_blocks = nn.ModuleList(
            [
                SS2D_cond_v4(
                    d_model=in_channels,
                    d_cond=cross_attention_dim,
                    cond_size=32,
                    dropout=0.1,
                    d_state=16,
                    size=int(72 / (in_channels / 320)),
                    scan_type="sweep",
                    num_direction=2,
                )
                for d in range(num_layers)
            ]
        )
        time_mix_inner_dim = inner_dim
        self.temporal_transformer_blocks = nn.ModuleList(
            [
                TemporalBasicTransformerBlock(
                    inner_dim,
                    time_mix_inner_dim,
                    num_attention_heads,
                    attention_head_dim,
                    cross_attention_dim=cross_attention_dim,
                )
                for _ in range(num_layers)
            ]
        )

        time_embed_dim = in_channels * 4
        self.time_pos_embed = TimestepEmbedding(
            in_channels, time_embed_dim, out_dim=in_channels
        )
        self.time_proj = Timesteps(in_channels, True, 0)
        self.time_mixer = AlphaBlender(alpha=0.5, merge_strategy="learned_with_images")

        # 4. Define output layers
        self.out_channels = in_channels if out_channels is None else out_channels
        # TODO: should use out_channels for continuous projections
        self.proj_out = nn.Linear(inner_dim, in_channels)

        self.gradient_checkpointing = False

    def forward(
        self,
        hidden_states: torch.Tensor,
        encoder_hidden_states: Optional[torch.Tensor] = None,
        cross_attention_kwargs: Optional[Dict[str, Any]] = None,
        image_only_indicator: Optional[torch.Tensor] = None,
        return_dict: bool = True,
    ):
        """
        Args:
            hidden_states (`torch.FloatTensor` of shape `(batch size, channel, height, width)`):
                Input hidden_states.
            num_frames (`int`):
                The number of frames to be processed per batch. This is used to reshape the hidden states.
            encoder_hidden_states ( `torch.LongTensor` of shape `(batch size, encoder_hidden_states dim)`, *optional*):
                Conditional embeddings for cross attention layer. If not given, cross-attention defaults to
                self-attention.
            image_only_indicator (`torch.LongTensor` of shape `(batch size, num_frames)`, *optional*):
                A tensor indicating whether the input contains only images. 1 indicates that the input contains only
                images, 0 indicates that the input contains video frames.
            return_dict (`bool`, *optional*, defaults to `True`):
                Whether or not to return a [`~models.transformer_temporal.TransformerTemporalModelOutput`] instead of a plain
                tuple.

        Returns:
            [`~models.transformer_temporal.TransformerTemporalModelOutput`] or `tuple`:
                If `return_dict` is True, an [`~models.transformer_temporal.TransformerTemporalModelOutput`] is
                returned, otherwise a `tuple` where the first element is the sample tensor.
        """

        # 1. Input
        batch_frames, _, height, width = hidden_states.shape
        num_frames = image_only_indicator.shape[-1]
        batch_size = batch_frames // num_frames

        def spatial2time(time_context):
            # print(time_context.shape)

            time_context = time_context.reshape(
                batch_size, num_frames, time_context.shape[-2], time_context.shape[-1]
            )
            time_context = time_context.mean(dim=(1,), keepdim=True)

            # time_context = time_context.flatten(1,2)
            # time_context = time_context[:, None].repeat(
            #     1, height * width, 1, 1
            # )
            time_context = time_context.repeat(1, height * width, 1, 1)
            time_context = time_context.reshape(
                batch_size * height * width, -1, time_context.shape[-1]
            )
            # print(time_context.shape)
            return time_context

        # clip_context, ip_contexts = encoder_hidden_states
        # clip_context_new = spatial2time(clip_context)
        # ip_contexts_new = []
        # for ip_context in ip_contexts:
        #     ip_context_new = spatial2time(ip_context)
        #     ip_contexts_new.append(ip_context_new)

        if isinstance(encoder_hidden_states, tuple):
            clip_hidden_states, ip_hidden_states = encoder_hidden_states
            encoder_hidden_states_time = (
                spatial2time(clip_hidden_states),
                [spatial2time(ip_hidden_state) for ip_hidden_state in ip_hidden_states],
            )
        else:
            encoder_hidden_states_time = spatial2time(encoder_hidden_states)

        residual = hidden_states

        hidden_states = self.norm(hidden_states)
        inner_dim = hidden_states.shape[1]
        hidden_states = hidden_states.permute(0, 2, 3, 1).reshape(
            batch_frames, height * width, inner_dim
        )
        hidden_states = self.proj_in(hidden_states)

        num_frames_emb = torch.arange(num_frames, device=hidden_states.device)
        num_frames_emb = num_frames_emb
        num_frames_emb = num_frames_emb.repeat(batch_size, 1)
        num_frames_emb = num_frames_emb.reshape(-1)
        t_emb = self.time_proj(num_frames_emb)
        # import ipdb
        # ipdb.set_trace()

        # `Timesteps` does not contain any weights and will always return f32 tensors
        # but time_embedding might actually be running in fp16. so we need to cast here.
        # there might be better ways to encapsulate this.
        t_emb = t_emb.to(dtype=hidden_states.dtype)

        emb = self.time_pos_embed(t_emb)
        emb = emb[:, None, :]
        # print(self.time_mixer.alpha)
        # 2. Blocks
        for block, mamba_block, temporal_block in zip(
            self.transformer_blocks, self.mamba_blocks, self.temporal_transformer_blocks
        ):
            if self.training and self.gradient_checkpointing:
                hidden_states = torch.utils.checkpoint.checkpoint(
                    block,
                    hidden_states,
                    None,
                    encoder_hidden_states,
                    None,
                    None,
                    cross_attention_kwargs,
                    use_reentrant=False,
                )
            else:
                hidden_states = block(
                    hidden_states,
                    encoder_hidden_states=encoder_hidden_states,
                    cross_attention_kwargs=cross_attention_kwargs,
                )
            if self.training and self.gradient_checkpointing:
                hidden_states = torch.utils.checkpoint.checkpoint(
                    mamba_block, hidden_states, encoder_hidden_states[0]
                )
            else:
                hidden_states = mamba_block(hidden_states, encoder_hidden_states[0])
            hidden_states_mix = hidden_states
            hidden_states_mix = hidden_states_mix + emb
            if self.training and self.gradient_checkpointing:

                hidden_states_mix = torch.utils.checkpoint.checkpoint(
                    temporal_block,
                    hidden_states_mix,
                    num_frames,
                    encoder_hidden_states_time,
                    use_reentrant=False,
                )

            else:
                hidden_states_mix = temporal_block(
                    hidden_states_mix,
                    num_frames=num_frames,
                    encoder_hidden_states=encoder_hidden_states_time,
                )
            hidden_states = self.time_mixer(
                x_spatial=hidden_states,
                x_temporal=hidden_states_mix,
                image_only_indicator=image_only_indicator,
            )

        # 3. Output
        hidden_states = self.proj_out(hidden_states)
        hidden_states = (
            hidden_states.reshape(batch_frames, height, width, inner_dim)
            .permute(0, 3, 1, 2)
            .contiguous()
        )

        output = hidden_states + residual

        if not return_dict:
            return (output,)

        return TransformerTemporalModelOutput(sample=output)


# ablation
# use the unet feature conditioned by clip feature after spatial attn, 更改了mamba的结构
class TransformerSpatioTemporalModel_mambaID_v4_wo_id(nn.Module):
    """
    A Transformer model for video-like data.

    Parameters:
        num_attention_heads (`int`, *optional*, defaults to 16): The number of heads to use for multi-head attention.
        attention_head_dim (`int`, *optional*, defaults to 88): The number of channels in each head.
        in_channels (`int`, *optional*):
            The number of channels in the input and output (specify if the input is **continuous**).
        out_channels (`int`, *optional*):
            The number of channels in the output (specify if the input is **continuous**).
        num_layers (`int`, *optional*, defaults to 1): The number of layers of Transformer blocks to use.
        cross_attention_dim (`int`, *optional*): The number of `encoder_hidden_states` dimensions to use.
    """

    def __init__(
        self,
        num_attention_heads: int = 16,
        attention_head_dim: int = 88,
        in_channels: int = 320,
        out_channels: Optional[int] = None,
        num_layers: int = 1,
        cross_attention_dim: Optional[int] = None,
    ):
        super().__init__()
        self.num_attention_heads = num_attention_heads
        self.attention_head_dim = attention_head_dim

        inner_dim = num_attention_heads * attention_head_dim
        self.inner_dim = inner_dim

        # 2. Define input layers
        self.in_channels = in_channels
        self.norm = torch.nn.GroupNorm(
            num_groups=32, num_channels=in_channels, eps=1e-6
        )
        self.proj_in = nn.Linear(in_channels, inner_dim)

        # 3. Define transformers blocks
        self.transformer_blocks = nn.ModuleList(
            [
                BasicTransformerBlock(
                    inner_dim,
                    num_attention_heads,
                    attention_head_dim,
                    cross_attention_dim=cross_attention_dim,
                )
                for d in range(num_layers)
            ]
        )

        # 3. Define transformers blocks
        # self_attention_cond = SS2D_cond(d_model=320,d_cond=1024, dropout=0.1, d_state=16, size=36, scan_type='scan', num_direction=4)
        # self_attention_cond = SS2D_cond(d_model=320,d_cond=1024,cond_size=32, dropout=0.1, d_state=16, size=72, scan_type='sweep', num_direction=2).cuda()
        self.mamba_blocks = nn.ModuleList(
            [
                SS2D_cond_v4(
                    d_model=in_channels,
                    d_cond=cross_attention_dim,
                    cond_size=32,
                    dropout=0.1,
                    d_state=16,
                    size=int(72 / (in_channels / 320)),
                    scan_type="sweep",
                    num_direction=2,
                )
                for d in range(num_layers)
            ]
        )
        time_mix_inner_dim = inner_dim
        self.temporal_transformer_blocks = nn.ModuleList(
            [
                TemporalBasicTransformerBlock(
                    inner_dim,
                    time_mix_inner_dim,
                    num_attention_heads,
                    attention_head_dim,
                    cross_attention_dim=cross_attention_dim,
                )
                for _ in range(num_layers)
            ]
        )

        time_embed_dim = in_channels * 4
        self.time_pos_embed = TimestepEmbedding(
            in_channels, time_embed_dim, out_dim=in_channels
        )
        self.time_proj = Timesteps(in_channels, True, 0)
        self.time_mixer = AlphaBlender(alpha=0.5, merge_strategy="learned_with_images")

        # 4. Define output layers
        self.out_channels = in_channels if out_channels is None else out_channels
        # TODO: should use out_channels for continuous projections
        self.proj_out = nn.Linear(inner_dim, in_channels)

        self.gradient_checkpointing = False

    def forward(
        self,
        hidden_states: torch.Tensor,
        encoder_hidden_states: Optional[torch.Tensor] = None,
        cross_attention_kwargs: Optional[Dict[str, Any]] = None,
        image_only_indicator: Optional[torch.Tensor] = None,
        return_dict: bool = True,
    ):
        """
        Args:
            hidden_states (`torch.FloatTensor` of shape `(batch size, channel, height, width)`):
                Input hidden_states.
            num_frames (`int`):
                The number of frames to be processed per batch. This is used to reshape the hidden states.
            encoder_hidden_states ( `torch.LongTensor` of shape `(batch size, encoder_hidden_states dim)`, *optional*):
                Conditional embeddings for cross attention layer. If not given, cross-attention defaults to
                self-attention.
            image_only_indicator (`torch.LongTensor` of shape `(batch size, num_frames)`, *optional*):
                A tensor indicating whether the input contains only images. 1 indicates that the input contains only
                images, 0 indicates that the input contains video frames.
            return_dict (`bool`, *optional*, defaults to `True`):
                Whether or not to return a [`~models.transformer_temporal.TransformerTemporalModelOutput`] instead of a plain
                tuple.

        Returns:
            [`~models.transformer_temporal.TransformerTemporalModelOutput`] or `tuple`:
                If `return_dict` is True, an [`~models.transformer_temporal.TransformerTemporalModelOutput`] is
                returned, otherwise a `tuple` where the first element is the sample tensor.
        """

        # 1. Input
        batch_frames, _, height, width = hidden_states.shape
        num_frames = image_only_indicator.shape[-1]
        batch_size = batch_frames // num_frames

        def spatial2time(time_context):
            # print(time_context.shape)

            time_context = time_context.reshape(
                batch_size, num_frames, time_context.shape[-2], time_context.shape[-1]
            )
            time_context = time_context.mean(dim=(1,), keepdim=True)

            # time_context = time_context.flatten(1,2)
            # time_context = time_context[:, None].repeat(
            #     1, height * width, 1, 1
            # )
            time_context = time_context.repeat(1, height * width, 1, 1)
            time_context = time_context.reshape(
                batch_size * height * width, -1, time_context.shape[-1]
            )
            # print(time_context.shape)
            return time_context

        # clip_context, ip_contexts = encoder_hidden_states
        # clip_context_new = spatial2time(clip_context)
        # ip_contexts_new = []
        # for ip_context in ip_contexts:
        #     ip_context_new = spatial2time(ip_context)
        #     ip_contexts_new.append(ip_context_new)

        if isinstance(encoder_hidden_states, tuple):
            clip_hidden_states, ip_hidden_states = encoder_hidden_states
            encoder_hidden_states_time = (
                spatial2time(clip_hidden_states),
                [spatial2time(ip_hidden_state) for ip_hidden_state in ip_hidden_states],
            )
        else:
            encoder_hidden_states_time = spatial2time(encoder_hidden_states)

        residual = hidden_states

        hidden_states = self.norm(hidden_states)
        inner_dim = hidden_states.shape[1]
        hidden_states = hidden_states.permute(0, 2, 3, 1).reshape(
            batch_frames, height * width, inner_dim
        )
        hidden_states = self.proj_in(hidden_states)

        num_frames_emb = torch.arange(num_frames, device=hidden_states.device)
        num_frames_emb = num_frames_emb
        num_frames_emb = num_frames_emb.repeat(batch_size, 1)
        num_frames_emb = num_frames_emb.reshape(-1)
        t_emb = self.time_proj(num_frames_emb)
        # import ipdb
        # ipdb.set_trace()

        # `Timesteps` does not contain any weights and will always return f32 tensors
        # but time_embedding might actually be running in fp16. so we need to cast here.
        # there might be better ways to encapsulate this.
        t_emb = t_emb.to(dtype=hidden_states.dtype)

        emb = self.time_pos_embed(t_emb)
        emb = emb[:, None, :]
        # print(self.time_mixer.alpha)
        # 2. Blocks
        for block, mamba_block, temporal_block in zip(
            self.transformer_blocks, self.mamba_blocks, self.temporal_transformer_blocks
        ):
            if self.training and self.gradient_checkpointing:
                hidden_states = torch.utils.checkpoint.checkpoint(
                    block,
                    hidden_states,
                    None,
                    encoder_hidden_states,
                    None,
                    None,
                    cross_attention_kwargs,
                    use_reentrant=False,
                )
            else:
                hidden_states = block(
                    hidden_states,
                    encoder_hidden_states=encoder_hidden_states,
                    cross_attention_kwargs=cross_attention_kwargs,
                )
            if self.training and self.gradient_checkpointing:
                hidden_states = torch.utils.checkpoint.checkpoint(
                    mamba_block,
                    hidden_states,
                    encoder_hidden_states[1][0].squeeze(1),
                )
            else:
                hidden_states = mamba_block(
                    hidden_states, encoder_hidden_states[1][0].squeeze(1)
                )
            hidden_states_mix = hidden_states
            hidden_states_mix = hidden_states_mix + emb
            if self.training and self.gradient_checkpointing:

                hidden_states_mix = torch.utils.checkpoint.checkpoint(
                    temporal_block,
                    hidden_states_mix,
                    num_frames,
                    encoder_hidden_states_time,
                    use_reentrant=False,
                )

            else:
                hidden_states_mix = temporal_block(
                    hidden_states_mix,
                    num_frames=num_frames,
                    encoder_hidden_states=encoder_hidden_states_time,
                )
            hidden_states = self.time_mixer(
                x_spatial=hidden_states,
                x_temporal=hidden_states_mix,
                image_only_indicator=image_only_indicator,
            )

        # 3. Output
        hidden_states = self.proj_out(hidden_states)
        hidden_states = (
            hidden_states.reshape(batch_frames, height, width, inner_dim)
            .permute(0, 3, 1, 2)
            .contiguous()
        )

        output = hidden_states + residual

        if not return_dict:
            return (output,)

        return TransformerTemporalModelOutput(sample=output)


# ablation
# use the unet feature conditioned by clip feature after spatial attn, 更改了mamba的结构
class TransformerSpatioTemporalModel_mambaID_v4_wo_ssd(nn.Module):
    """
    A Transformer model for video-like data.

    Parameters:
        num_attention_heads (`int`, *optional*, defaults to 16): The number of heads to use for multi-head attention.
        attention_head_dim (`int`, *optional*, defaults to 88): The number of channels in each head.
        in_channels (`int`, *optional*):
            The number of channels in the input and output (specify if the input is **continuous**).
        out_channels (`int`, *optional*):
            The number of channels in the output (specify if the input is **continuous**).
        num_layers (`int`, *optional*, defaults to 1): The number of layers of Transformer blocks to use.
        cross_attention_dim (`int`, *optional*): The number of `encoder_hidden_states` dimensions to use.
    """

    def __init__(
        self,
        num_attention_heads: int = 16,
        attention_head_dim: int = 88,
        in_channels: int = 320,
        out_channels: Optional[int] = None,
        num_layers: int = 1,
        cross_attention_dim: Optional[int] = None,
    ):
        super().__init__()
        self.num_attention_heads = num_attention_heads
        self.attention_head_dim = attention_head_dim

        inner_dim = num_attention_heads * attention_head_dim
        self.inner_dim = inner_dim

        # 2. Define input layers
        self.in_channels = in_channels
        self.norm = torch.nn.GroupNorm(
            num_groups=32, num_channels=in_channels, eps=1e-6
        )
        self.proj_in = nn.Linear(in_channels, inner_dim)

        # 3. Define transformers blocks
        self.transformer_blocks = nn.ModuleList(
            [
                BasicTransformerBlock(
                    inner_dim,
                    num_attention_heads,
                    attention_head_dim,
                    cross_attention_dim=cross_attention_dim,
                )
                for d in range(num_layers)
            ]
        )

        # 3. Define transformers blocks
        # self_attention_cond = SS2D_cond(d_model=320,d_cond=1024, dropout=0.1, d_state=16, size=36, scan_type='scan', num_direction=4)
        # self_attention_cond = SS2D_cond(d_model=320,d_cond=1024,cond_size=32, dropout=0.1, d_state=16, size=72, scan_type='sweep', num_direction=2).cuda()
        self.mamba_blocks = nn.ModuleList(
            [
                SS2D_cond_v4_wo_ssd(
                    d_model=in_channels,
                    d_cond=cross_attention_dim,
                    cond_size=32,
                    dropout=0.1,
                    d_state=16,
                    size=int(72 / (in_channels / 320)),
                    scan_type="sweep",
                    num_direction=2,
                )
                for d in range(num_layers)
            ]
        )
        time_mix_inner_dim = inner_dim
        self.temporal_transformer_blocks = nn.ModuleList(
            [
                TemporalBasicTransformerBlock(
                    inner_dim,
                    time_mix_inner_dim,
                    num_attention_heads,
                    attention_head_dim,
                    cross_attention_dim=cross_attention_dim,
                )
                for _ in range(num_layers)
            ]
        )

        time_embed_dim = in_channels * 4
        self.time_pos_embed = TimestepEmbedding(
            in_channels, time_embed_dim, out_dim=in_channels
        )
        self.time_proj = Timesteps(in_channels, True, 0)
        self.time_mixer = AlphaBlender(alpha=0.5, merge_strategy="learned_with_images")

        # 4. Define output layers
        self.out_channels = in_channels if out_channels is None else out_channels
        # TODO: should use out_channels for continuous projections
        self.proj_out = nn.Linear(inner_dim, in_channels)

        self.gradient_checkpointing = False

    def forward(
        self,
        hidden_states: torch.Tensor,
        encoder_hidden_states: Optional[torch.Tensor] = None,
        cross_attention_kwargs: Optional[Dict[str, Any]] = None,
        image_only_indicator: Optional[torch.Tensor] = None,
        return_dict: bool = True,
    ):
        """
        Args:
            hidden_states (`torch.FloatTensor` of shape `(batch size, channel, height, width)`):
                Input hidden_states.
            num_frames (`int`):
                The number of frames to be processed per batch. This is used to reshape the hidden states.
            encoder_hidden_states ( `torch.LongTensor` of shape `(batch size, encoder_hidden_states dim)`, *optional*):
                Conditional embeddings for cross attention layer. If not given, cross-attention defaults to
                self-attention.
            image_only_indicator (`torch.LongTensor` of shape `(batch size, num_frames)`, *optional*):
                A tensor indicating whether the input contains only images. 1 indicates that the input contains only
                images, 0 indicates that the input contains video frames.
            return_dict (`bool`, *optional*, defaults to `True`):
                Whether or not to return a [`~models.transformer_temporal.TransformerTemporalModelOutput`] instead of a plain
                tuple.

        Returns:
            [`~models.transformer_temporal.TransformerTemporalModelOutput`] or `tuple`:
                If `return_dict` is True, an [`~models.transformer_temporal.TransformerTemporalModelOutput`] is
                returned, otherwise a `tuple` where the first element is the sample tensor.
        """

        # 1. Input
        batch_frames, _, height, width = hidden_states.shape
        num_frames = image_only_indicator.shape[-1]
        batch_size = batch_frames // num_frames

        def spatial2time(time_context):
            # print(time_context.shape)

            time_context = time_context.reshape(
                batch_size, num_frames, time_context.shape[-2], time_context.shape[-1]
            )
            time_context = time_context.mean(dim=(1,), keepdim=True)

            # time_context = time_context.flatten(1,2)
            # time_context = time_context[:, None].repeat(
            #     1, height * width, 1, 1
            # )
            time_context = time_context.repeat(1, height * width, 1, 1)
            time_context = time_context.reshape(
                batch_size * height * width, -1, time_context.shape[-1]
            )
            # print(time_context.shape)
            return time_context

        # clip_context, ip_contexts = encoder_hidden_states
        # clip_context_new = spatial2time(clip_context)
        # ip_contexts_new = []
        # for ip_context in ip_contexts:
        #     ip_context_new = spatial2time(ip_context)
        #     ip_contexts_new.append(ip_context_new)

        if isinstance(encoder_hidden_states, tuple):
            clip_hidden_states, ip_hidden_states = encoder_hidden_states
            encoder_hidden_states_time = (
                spatial2time(clip_hidden_states),
                [spatial2time(ip_hidden_state) for ip_hidden_state in ip_hidden_states],
            )
        else:
            encoder_hidden_states_time = spatial2time(encoder_hidden_states)

        residual = hidden_states

        hidden_states = self.norm(hidden_states)
        inner_dim = hidden_states.shape[1]
        hidden_states = hidden_states.permute(0, 2, 3, 1).reshape(
            batch_frames, height * width, inner_dim
        )
        hidden_states = self.proj_in(hidden_states)

        num_frames_emb = torch.arange(num_frames, device=hidden_states.device)
        num_frames_emb = num_frames_emb
        num_frames_emb = num_frames_emb.repeat(batch_size, 1)
        num_frames_emb = num_frames_emb.reshape(-1)
        t_emb = self.time_proj(num_frames_emb)
        # import ipdb
        # ipdb.set_trace()

        # `Timesteps` does not contain any weights and will always return f32 tensors
        # but time_embedding might actually be running in fp16. so we need to cast here.
        # there might be better ways to encapsulate this.
        t_emb = t_emb.to(dtype=hidden_states.dtype)

        emb = self.time_pos_embed(t_emb)
        emb = emb[:, None, :]
        # print(self.time_mixer.alpha)
        # 2. Blocks
        for block, mamba_block, temporal_block in zip(
            self.transformer_blocks, self.mamba_blocks, self.temporal_transformer_blocks
        ):
            if self.training and self.gradient_checkpointing:
                hidden_states = torch.utils.checkpoint.checkpoint(
                    block,
                    hidden_states,
                    None,
                    encoder_hidden_states,
                    None,
                    None,
                    cross_attention_kwargs,
                    use_reentrant=False,
                )
            else:
                hidden_states = block(
                    hidden_states,
                    encoder_hidden_states=encoder_hidden_states,
                    cross_attention_kwargs=cross_attention_kwargs,
                )
            if self.training and self.gradient_checkpointing:
                hidden_states = torch.utils.checkpoint.checkpoint(
                    mamba_block,
                    hidden_states,
                    torch.cat(
                        [
                            encoder_hidden_states[0],
                            encoder_hidden_states[1][0].squeeze(1),
                        ],
                        dim=1,
                    ),
                )
            else:
                hidden_states = mamba_block(
                    hidden_states,
                    torch.cat(
                        [
                            encoder_hidden_states[0],
                            encoder_hidden_states[1][0].squeeze(1),
                        ],
                        dim=1,
                    ),
                )
            hidden_states_mix = hidden_states
            hidden_states_mix = hidden_states_mix + emb
            if self.training and self.gradient_checkpointing:

                hidden_states_mix = torch.utils.checkpoint.checkpoint(
                    temporal_block,
                    hidden_states_mix,
                    num_frames,
                    encoder_hidden_states_time,
                    use_reentrant=False,
                )

            else:
                hidden_states_mix = temporal_block(
                    hidden_states_mix,
                    num_frames=num_frames,
                    encoder_hidden_states=encoder_hidden_states_time,
                )
            hidden_states = self.time_mixer(
                x_spatial=hidden_states,
                x_temporal=hidden_states_mix,
                image_only_indicator=image_only_indicator,
            )

        # 3. Output
        hidden_states = self.proj_out(hidden_states)
        hidden_states = (
            hidden_states.reshape(batch_frames, height, width, inner_dim)
            .permute(0, 3, 1, 2)
            .contiguous()
        )

        output = hidden_states + residual

        if not return_dict:
            return (output,)

        return TransformerTemporalModelOutput(sample=output)


# use the unet feature conditioned by clip feature after spatial attn, 更改了mamba的结构
class TransformerSpatioTemporalModel_mambaID_v4_two_ip(nn.Module):
    """
    A Transformer model for video-like data.

    Parameters:
        num_attention_heads (`int`, *optional*, defaults to 16): The number of heads to use for multi-head attention.
        attention_head_dim (`int`, *optional*, defaults to 88): The number of channels in each head.
        in_channels (`int`, *optional*):
            The number of channels in the input and output (specify if the input is **continuous**).
        out_channels (`int`, *optional*):
            The number of channels in the output (specify if the input is **continuous**).
        num_layers (`int`, *optional*, defaults to 1): The number of layers of Transformer blocks to use.
        cross_attention_dim (`int`, *optional*): The number of `encoder_hidden_states` dimensions to use.
    """

    def __init__(
        self,
        num_attention_heads: int = 16,
        attention_head_dim: int = 88,
        in_channels: int = 320,
        out_channels: Optional[int] = None,
        num_layers: int = 1,
        cross_attention_dim: Optional[int] = None,
    ):
        super().__init__()
        self.num_attention_heads = num_attention_heads
        self.attention_head_dim = attention_head_dim

        inner_dim = num_attention_heads * attention_head_dim
        self.inner_dim = inner_dim

        # 2. Define input layers
        self.in_channels = in_channels
        self.norm = torch.nn.GroupNorm(
            num_groups=32, num_channels=in_channels, eps=1e-6
        )
        self.proj_in = nn.Linear(in_channels, inner_dim)

        # 3. Define transformers blocks
        self.transformer_blocks = nn.ModuleList(
            [
                BasicTransformerBlock(
                    inner_dim,
                    num_attention_heads,
                    attention_head_dim,
                    cross_attention_dim=cross_attention_dim,
                )
                for d in range(num_layers)
            ]
        )

        # 3. Define transformers blocks
        # self_attention_cond = SS2D_cond(d_model=320,d_cond=1024, dropout=0.1, d_state=16, size=36, scan_type='scan', num_direction=4)
        # self_attention_cond = SS2D_cond(d_model=320,d_cond=1024,cond_size=32, dropout=0.1, d_state=16, size=72, scan_type='sweep', num_direction=2).cuda()
        self.mamba_blocks = nn.ModuleList(
            [
                SS2D_cond_v4(
                    d_model=in_channels,
                    d_cond=cross_attention_dim,
                    cond_size=32,
                    dropout=0.1,
                    d_state=16,
                    size=int(72 / (in_channels / 320)),
                    scan_type="sweep",
                    num_direction=2,
                )
                for d in range(num_layers)
            ]
        )
        time_mix_inner_dim = inner_dim
        self.temporal_transformer_blocks = nn.ModuleList(
            [
                TemporalBasicTransformerBlock(
                    inner_dim,
                    time_mix_inner_dim,
                    num_attention_heads,
                    attention_head_dim,
                    cross_attention_dim=cross_attention_dim,
                )
                for _ in range(num_layers)
            ]
        )

        time_embed_dim = in_channels * 4
        self.time_pos_embed = TimestepEmbedding(
            in_channels, time_embed_dim, out_dim=in_channels
        )
        self.time_proj = Timesteps(in_channels, True, 0)
        self.time_mixer = AlphaBlender(alpha=0.5, merge_strategy="learned_with_images")

        # 4. Define output layers
        self.out_channels = in_channels if out_channels is None else out_channels
        # TODO: should use out_channels for continuous projections
        self.proj_out = nn.Linear(inner_dim, in_channels)

        self.gradient_checkpointing = False

    def forward(
        self,
        hidden_states: torch.Tensor,
        encoder_hidden_states: Optional[torch.Tensor] = None,
        cross_attention_kwargs: Optional[Dict[str, Any]] = None,
        image_only_indicator: Optional[torch.Tensor] = None,
        return_dict: bool = True,
    ):
        """
        Args:
            hidden_states (`torch.FloatTensor` of shape `(batch size, channel, height, width)`):
                Input hidden_states.
            num_frames (`int`):
                The number of frames to be processed per batch. This is used to reshape the hidden states.
            encoder_hidden_states ( `torch.LongTensor` of shape `(batch size, encoder_hidden_states dim)`, *optional*):
                Conditional embeddings for cross attention layer. If not given, cross-attention defaults to
                self-attention.
            image_only_indicator (`torch.LongTensor` of shape `(batch size, num_frames)`, *optional*):
                A tensor indicating whether the input contains only images. 1 indicates that the input contains only
                images, 0 indicates that the input contains video frames.
            return_dict (`bool`, *optional*, defaults to `True`):
                Whether or not to return a [`~models.transformer_temporal.TransformerTemporalModelOutput`] instead of a plain
                tuple.

        Returns:
            [`~models.transformer_temporal.TransformerTemporalModelOutput`] or `tuple`:
                If `return_dict` is True, an [`~models.transformer_temporal.TransformerTemporalModelOutput`] is
                returned, otherwise a `tuple` where the first element is the sample tensor.
        """

        # 1. Input
        batch_frames, _, height, width = hidden_states.shape
        num_frames = image_only_indicator.shape[-1]
        batch_size = batch_frames // num_frames

        def spatial2time(time_context):
            # print(time_context.shape)

            time_context = time_context.reshape(
                batch_size, num_frames, time_context.shape[-2], time_context.shape[-1]
            )
            time_context = time_context.mean(dim=(1,), keepdim=True)

            # time_context = time_context.flatten(1,2)
            # time_context = time_context[:, None].repeat(
            #     1, height * width, 1, 1
            # )
            time_context = time_context.repeat(1, height * width, 1, 1)
            time_context = time_context.reshape(
                batch_size * height * width, -1, time_context.shape[-1]
            )
            # print(time_context.shape)
            return time_context

        # clip_context, ip_contexts = encoder_hidden_states
        # clip_context_new = spatial2time(clip_context)
        # ip_contexts_new = []
        # for ip_context in ip_contexts:
        #     ip_context_new = spatial2time(ip_context)
        #     ip_contexts_new.append(ip_context_new)

        if isinstance(encoder_hidden_states, tuple):
            clip_hidden_states, ip_hidden_states = encoder_hidden_states
            encoder_hidden_states_time = (
                spatial2time(clip_hidden_states),
                [spatial2time(ip_hidden_state) for ip_hidden_state in ip_hidden_states],
            )
        else:
            encoder_hidden_states_time = spatial2time(encoder_hidden_states)

        residual = hidden_states

        hidden_states = self.norm(hidden_states)
        inner_dim = hidden_states.shape[1]
        hidden_states = hidden_states.permute(0, 2, 3, 1).reshape(
            batch_frames, height * width, inner_dim
        )
        hidden_states = self.proj_in(hidden_states)

        num_frames_emb = torch.arange(num_frames, device=hidden_states.device)
        num_frames_emb = num_frames_emb
        num_frames_emb = num_frames_emb.repeat(batch_size, 1)
        num_frames_emb = num_frames_emb.reshape(-1)
        t_emb = self.time_proj(num_frames_emb)
        # import ipdb
        # ipdb.set_trace()

        # `Timesteps` does not contain any weights and will always return f32 tensors
        # but time_embedding might actually be running in fp16. so we need to cast here.
        # there might be better ways to encapsulate this.
        t_emb = t_emb.to(dtype=hidden_states.dtype)

        emb = self.time_pos_embed(t_emb)
        emb = emb[:, None, :]
        # print(self.time_mixer.alpha)
        # 2. Blocks
        for block, mamba_block, temporal_block in zip(
            self.transformer_blocks, self.mamba_blocks, self.temporal_transformer_blocks
        ):
            if self.training and self.gradient_checkpointing:
                hidden_states = torch.utils.checkpoint.checkpoint(
                    block,
                    hidden_states,
                    None,
                    encoder_hidden_states,
                    None,
                    None,
                    cross_attention_kwargs,
                    use_reentrant=False,
                )
            else:
                hidden_states = block(
                    hidden_states,
                    encoder_hidden_states=encoder_hidden_states,
                    cross_attention_kwargs=cross_attention_kwargs,
                )
            if self.training and self.gradient_checkpointing:
                hidden_states = torch.utils.checkpoint.checkpoint(
                    mamba_block,
                    hidden_states,
                    torch.cat(
                        [
                            encoder_hidden_states[0],
                            torch.cat(encoder_hidden_states[1], -2).squeeze(1),
                        ],
                        dim=1,
                    ),
                )
            else:
                hidden_states = mamba_block(
                    hidden_states,
                    torch.cat(
                        [
                            encoder_hidden_states[0],
                            torch.cat(encoder_hidden_states[1], -2).squeeze(1),
                        ],
                        dim=1,
                    ),
                )
            hidden_states_mix = hidden_states
            hidden_states_mix = hidden_states_mix + emb
            if self.training and self.gradient_checkpointing:

                hidden_states_mix = torch.utils.checkpoint.checkpoint(
                    temporal_block,
                    hidden_states_mix,
                    num_frames,
                    encoder_hidden_states_time,
                    use_reentrant=False,
                )

            else:
                hidden_states_mix = temporal_block(
                    hidden_states_mix,
                    num_frames=num_frames,
                    encoder_hidden_states=encoder_hidden_states_time,
                )
            hidden_states = self.time_mixer(
                x_spatial=hidden_states,
                x_temporal=hidden_states_mix,
                image_only_indicator=image_only_indicator,
            )

        # 3. Output
        hidden_states = self.proj_out(hidden_states)
        hidden_states = (
            hidden_states.reshape(batch_frames, height, width, inner_dim)
            .permute(0, 3, 1, 2)
            .contiguous()
        )

        output = hidden_states + residual

        if not return_dict:
            return (output,)

        return TransformerTemporalModelOutput(sample=output)


# 使用新的mamba结构，使用exp 和audio的context，使用新的mamba结构
class TransformerSpatioTemporalModel_new_mambaID_v8_two_ip(nn.Module):
    """
    A Transformer model for video-like data.

    Parameters:
        num_attention_heads (`int`, *optional*, defaults to 16): The number of heads to use for multi-head attention.
        attention_head_dim (`int`, *optional*, defaults to 88): The number of channels in each head.
        in_channels (`int`, *optional*):
            The number of channels in the input and output (specify if the input is **continuous**).
        out_channels (`int`, *optional*):
            The number of channels in the output (specify if the input is **continuous**).
        num_layers (`int`, *optional*, defaults to 1): The number of layers of Transformer blocks to use.
        cross_attention_dim (`int`, *optional*): The number of `encoder_hidden_states` dimensions to use.
    """

    def __init__(
        self,
        num_attention_heads: int = 16,
        attention_head_dim: int = 88,
        in_channels: int = 320,
        out_channels: Optional[int] = None,
        num_layers: int = 1,
        cross_attention_dim: Optional[int] = None,
    ):
        super().__init__()
        self.num_attention_heads = num_attention_heads
        self.attention_head_dim = attention_head_dim

        inner_dim = num_attention_heads * attention_head_dim
        self.inner_dim = inner_dim

        # 2. Define input layers
        self.in_channels = in_channels
        self.norm = torch.nn.GroupNorm(
            num_groups=32, num_channels=in_channels, eps=1e-6
        )
        self.proj_in = nn.Linear(in_channels, inner_dim)

        # 3. Define transformers blocks
        self.transformer_blocks = nn.ModuleList(
            [
                BasicTransformerBlock(
                    inner_dim,
                    num_attention_heads,
                    attention_head_dim,
                    cross_attention_dim=cross_attention_dim,
                )
                for d in range(num_layers)
            ]
        )

        # 3. Define transformers blocks
        # self_attention_cond = SS2D_cond(d_model=320,d_cond=1024, dropout=0.1, d_state=16, size=36, scan_type='scan', num_direction=4)
        # self_attention_cond = SS2D_cond(d_model=320,d_cond=1024,cond_size=32, dropout=0.1, d_state=16, size=72, scan_type='sweep', num_direction=2).cuda()
        self.mamba_blocks = nn.ModuleList(
            [
                SS2D_cond_v8(
                    d_model=in_channels,
                    d_cond=cross_attention_dim,
                    cond_size=32,
                    dropout=0.1,
                    d_state=16,
                    size=int(72 / (in_channels / 320)),
                    scan_type="sweep",
                    num_direction=2,
                )
                for d in range(num_layers)
            ]
        )
        time_mix_inner_dim = inner_dim
        self.temporal_transformer_blocks = nn.ModuleList(
            [
                TemporalBasicTransformerBlock(
                    inner_dim,
                    time_mix_inner_dim,
                    num_attention_heads,
                    attention_head_dim,
                    cross_attention_dim=cross_attention_dim,
                )
                for _ in range(num_layers)
            ]
        )

        time_embed_dim = in_channels * 4
        self.time_pos_embed = TimestepEmbedding(
            in_channels, time_embed_dim, out_dim=in_channels
        )
        self.time_proj = Timesteps(in_channels, True, 0)
        self.time_mixer = AlphaBlender(alpha=0.5, merge_strategy="learned_with_images")

        # 4. Define output layers
        self.out_channels = in_channels if out_channels is None else out_channels
        # TODO: should use out_channels for continuous projections
        self.proj_out = nn.Linear(inner_dim, in_channels)

        self.gradient_checkpointing = False

    def forward(
        self,
        hidden_states: torch.Tensor,
        encoder_hidden_states: Optional[torch.Tensor] = None,
        cross_attention_kwargs: Optional[Dict[str, Any]] = None,
        image_only_indicator: Optional[torch.Tensor] = None,
        return_dict: bool = True,
    ):
        """
        Args:
            hidden_states (`torch.FloatTensor` of shape `(batch size, channel, height, width)`):
                Input hidden_states.
            num_frames (`int`):
                The number of frames to be processed per batch. This is used to reshape the hidden states.
            encoder_hidden_states ( `torch.LongTensor` of shape `(batch size, encoder_hidden_states dim)`, *optional*):
                Conditional embeddings for cross attention layer. If not given, cross-attention defaults to
                self-attention.
            image_only_indicator (`torch.LongTensor` of shape `(batch size, num_frames)`, *optional*):
                A tensor indicating whether the input contains only images. 1 indicates that the input contains only
                images, 0 indicates that the input contains video frames.
            return_dict (`bool`, *optional*, defaults to `True`):
                Whether or not to return a [`~models.transformer_temporal.TransformerTemporalModelOutput`] instead of a plain
                tuple.

        Returns:
            [`~models.transformer_temporal.TransformerTemporalModelOutput`] or `tuple`:
                If `return_dict` is True, an [`~models.transformer_temporal.TransformerTemporalModelOutput`] is
                returned, otherwise a `tuple` where the first element is the sample tensor.
        """

        # 1. Input
        batch_frames, _, height, width = hidden_states.shape
        num_frames = image_only_indicator.shape[-1]
        batch_size = batch_frames // num_frames

        def spatial2time(time_context):
            # print(time_context.shape)

            time_context = time_context.reshape(
                batch_size, num_frames, time_context.shape[-2], time_context.shape[-1]
            )
            time_context = time_context.mean(dim=(1,), keepdim=True)

            # time_context = time_context.flatten(1,2)
            # time_context = time_context[:, None].repeat(
            #     1, height * width, 1, 1
            # )
            time_context = time_context.repeat(1, height * width, 1, 1)
            time_context = time_context.reshape(
                batch_size * height * width, -1, time_context.shape[-1]
            )
            # print(time_context.shape)
            return time_context

        # clip_context, ip_contexts = encoder_hidden_states
        # clip_context_new = spatial2time(clip_context)
        # ip_contexts_new = []
        # for ip_context in ip_contexts:
        #     ip_context_new = spatial2time(ip_context)
        #     ip_contexts_new.append(ip_context_new)

        if isinstance(encoder_hidden_states, tuple):
            clip_hidden_states, ip_hidden_states = encoder_hidden_states
            encoder_hidden_states_time = (
                spatial2time(clip_hidden_states),
                [spatial2time(ip_hidden_state) for ip_hidden_state in ip_hidden_states],
            )
        else:
            encoder_hidden_states_time = spatial2time(encoder_hidden_states)

        residual = hidden_states

        hidden_states = self.norm(hidden_states)
        inner_dim = hidden_states.shape[1]
        hidden_states = hidden_states.permute(0, 2, 3, 1).reshape(
            batch_frames, height * width, inner_dim
        )
        hidden_states = self.proj_in(hidden_states)

        num_frames_emb = torch.arange(num_frames, device=hidden_states.device)
        num_frames_emb = num_frames_emb
        num_frames_emb = num_frames_emb.repeat(batch_size, 1)
        num_frames_emb = num_frames_emb.reshape(-1)
        t_emb = self.time_proj(num_frames_emb)
        # import ipdb
        # ipdb.set_trace()

        # `Timesteps` does not contain any weights and will always return f32 tensors
        # but time_embedding might actually be running in fp16. so we need to cast here.
        # there might be better ways to encapsulate this.
        t_emb = t_emb.to(dtype=hidden_states.dtype)

        emb = self.time_pos_embed(t_emb)
        emb = emb[:, None, :]
        # print(self.time_mixer.alpha)
        # 2. Blocks
        for block, mamba_block, temporal_block in zip(
            self.transformer_blocks, self.mamba_blocks, self.temporal_transformer_blocks
        ):
            if self.training and self.gradient_checkpointing:
                hidden_states = torch.utils.checkpoint.checkpoint(
                    block,
                    hidden_states,
                    None,
                    encoder_hidden_states,
                    None,
                    None,
                    cross_attention_kwargs,
                    use_reentrant=False,
                )
            else:
                hidden_states = block(
                    hidden_states,
                    encoder_hidden_states=encoder_hidden_states,
                    cross_attention_kwargs=cross_attention_kwargs,
                )
            if self.training and self.gradient_checkpointing:
                hidden_states = torch.utils.checkpoint.checkpoint(
                    mamba_block,
                    hidden_states,
                    encoder_hidden_states[0],
                    torch.cat(
                        [
                            encoder_hidden_states[1][0].squeeze(1),
                            encoder_hidden_states[1][1].squeeze(1),
                        ],
                        dim=1,
                    ),
                    cross_attention_kwargs["ip_adapter_masks"],
                )
            else:
                hidden_states = mamba_block(
                    hidden_states,
                    encoder_hidden_states[0],
                    torch.cat(
                        [
                            encoder_hidden_states[1][0].squeeze(1),
                            encoder_hidden_states[1][1].squeeze(1),
                        ],
                        dim=1,
                    ),
                    cross_attention_kwargs["ip_adapter_masks"],
                )
            hidden_states_mix = hidden_states
            hidden_states_mix = hidden_states_mix + emb
            if self.training and self.gradient_checkpointing:

                hidden_states_mix = torch.utils.checkpoint.checkpoint(
                    temporal_block,
                    hidden_states_mix,
                    num_frames,
                    encoder_hidden_states_time,
                    use_reentrant=False,
                )

            else:
                hidden_states_mix = temporal_block(
                    hidden_states_mix,
                    num_frames=num_frames,
                    encoder_hidden_states=encoder_hidden_states_time,
                )
            hidden_states = self.time_mixer(
                x_spatial=hidden_states,
                x_temporal=hidden_states_mix,
                image_only_indicator=image_only_indicator,
            )

        # 3. Output
        hidden_states = self.proj_out(hidden_states)
        hidden_states = (
            hidden_states.reshape(batch_frames, height, width, inner_dim)
            .permute(0, 3, 1, 2)
            .contiguous()
        )

        output = hidden_states + residual

        if not return_dict:
            return (output,)

        return TransformerTemporalModelOutput(sample=output)


# 使用新的mamba结构，使用exp 和audio的context，使用新的mamba结构
class TransformerSpatioTemporalModel_new_mambaID_v9_two_ip(nn.Module):
    """
    A Transformer model for video-like data.

    Parameters:
        num_attention_heads (`int`, *optional*, defaults to 16): The number of heads to use for multi-head attention.
        attention_head_dim (`int`, *optional*, defaults to 88): The number of channels in each head.
        in_channels (`int`, *optional*):
            The number of channels in the input and output (specify if the input is **continuous**).
        out_channels (`int`, *optional*):
            The number of channels in the output (specify if the input is **continuous**).
        num_layers (`int`, *optional*, defaults to 1): The number of layers of Transformer blocks to use.
        cross_attention_dim (`int`, *optional*): The number of `encoder_hidden_states` dimensions to use.
    """

    def __init__(
        self,
        num_attention_heads: int = 16,
        attention_head_dim: int = 88,
        in_channels: int = 320,
        out_channels: Optional[int] = None,
        num_layers: int = 1,
        cross_attention_dim: Optional[int] = None,
    ):
        super().__init__()
        self.num_attention_heads = num_attention_heads
        self.attention_head_dim = attention_head_dim

        inner_dim = num_attention_heads * attention_head_dim
        self.inner_dim = inner_dim

        # 2. Define input layers
        self.in_channels = in_channels
        self.norm = torch.nn.GroupNorm(
            num_groups=32, num_channels=in_channels, eps=1e-6
        )
        self.proj_in = nn.Linear(in_channels, inner_dim)

        # 3. Define transformers blocks
        self.transformer_blocks = nn.ModuleList(
            [
                BasicTransformerBlock(
                    inner_dim,
                    num_attention_heads,
                    attention_head_dim,
                    cross_attention_dim=cross_attention_dim,
                )
                for d in range(num_layers)
            ]
        )

        # 3. Define transformers blocks
        # self_attention_cond = SS2D_cond(d_model=320,d_cond=1024, dropout=0.1, d_state=16, size=36, scan_type='scan', num_direction=4)
        # self_attention_cond = SS2D_cond(d_model=320,d_cond=1024,cond_size=32, dropout=0.1, d_state=16, size=72, scan_type='sweep', num_direction=2).cuda()
        self.mamba_blocks = nn.ModuleList(
            [
                SS2D_cond_v9(
                    d_model=in_channels,
                    d_cond=cross_attention_dim,
                    cond_size=32,
                    dropout=0.1,
                    d_state=16,
                    size=int(72 / (in_channels / 320)),
                    scan_type="sweep",
                    num_direction=2,
                )
                for d in range(num_layers)
            ]
        )
        time_mix_inner_dim = inner_dim
        self.temporal_transformer_blocks = nn.ModuleList(
            [
                TemporalBasicTransformerBlock(
                    inner_dim,
                    time_mix_inner_dim,
                    num_attention_heads,
                    attention_head_dim,
                    cross_attention_dim=cross_attention_dim,
                )
                for _ in range(num_layers)
            ]
        )

        time_embed_dim = in_channels * 4
        self.time_pos_embed = TimestepEmbedding(
            in_channels, time_embed_dim, out_dim=in_channels
        )
        self.time_proj = Timesteps(in_channels, True, 0)
        self.time_mixer = AlphaBlender(alpha=0.5, merge_strategy="learned_with_images")

        # 4. Define output layers
        self.out_channels = in_channels if out_channels is None else out_channels
        # TODO: should use out_channels for continuous projections
        self.proj_out = nn.Linear(inner_dim, in_channels)

        self.gradient_checkpointing = False

    def forward(
        self,
        hidden_states: torch.Tensor,
        encoder_hidden_states: Optional[torch.Tensor] = None,
        cross_attention_kwargs: Optional[Dict[str, Any]] = None,
        image_only_indicator: Optional[torch.Tensor] = None,
        return_dict: bool = True,
    ):
        """
        Args:
            hidden_states (`torch.FloatTensor` of shape `(batch size, channel, height, width)`):
                Input hidden_states.
            num_frames (`int`):
                The number of frames to be processed per batch. This is used to reshape the hidden states.
            encoder_hidden_states ( `torch.LongTensor` of shape `(batch size, encoder_hidden_states dim)`, *optional*):
                Conditional embeddings for cross attention layer. If not given, cross-attention defaults to
                self-attention.
            image_only_indicator (`torch.LongTensor` of shape `(batch size, num_frames)`, *optional*):
                A tensor indicating whether the input contains only images. 1 indicates that the input contains only
                images, 0 indicates that the input contains video frames.
            return_dict (`bool`, *optional*, defaults to `True`):
                Whether or not to return a [`~models.transformer_temporal.TransformerTemporalModelOutput`] instead of a plain
                tuple.

        Returns:
            [`~models.transformer_temporal.TransformerTemporalModelOutput`] or `tuple`:
                If `return_dict` is True, an [`~models.transformer_temporal.TransformerTemporalModelOutput`] is
                returned, otherwise a `tuple` where the first element is the sample tensor.
        """

        # 1. Input
        batch_frames, _, height, width = hidden_states.shape
        num_frames = image_only_indicator.shape[-1]
        batch_size = batch_frames // num_frames

        def spatial2time(time_context):
            # print(time_context.shape)

            time_context = time_context.reshape(
                batch_size, num_frames, time_context.shape[-2], time_context.shape[-1]
            )
            time_context = time_context.mean(dim=(1,), keepdim=True)

            # time_context = time_context.flatten(1,2)
            # time_context = time_context[:, None].repeat(
            #     1, height * width, 1, 1
            # )
            time_context = time_context.repeat(1, height * width, 1, 1)
            time_context = time_context.reshape(
                batch_size * height * width, -1, time_context.shape[-1]
            )
            # print(time_context.shape)
            return time_context

        # clip_context, ip_contexts = encoder_hidden_states
        # clip_context_new = spatial2time(clip_context)
        # ip_contexts_new = []
        # for ip_context in ip_contexts:
        #     ip_context_new = spatial2time(ip_context)
        #     ip_contexts_new.append(ip_context_new)

        if isinstance(encoder_hidden_states, tuple):
            clip_hidden_states, ip_hidden_states = encoder_hidden_states
            encoder_hidden_states_time = (
                spatial2time(clip_hidden_states),
                [spatial2time(ip_hidden_state) for ip_hidden_state in ip_hidden_states],
            )
        else:
            encoder_hidden_states_time = spatial2time(encoder_hidden_states)

        residual = hidden_states

        hidden_states = self.norm(hidden_states)
        inner_dim = hidden_states.shape[1]
        hidden_states = hidden_states.permute(0, 2, 3, 1).reshape(
            batch_frames, height * width, inner_dim
        )
        hidden_states = self.proj_in(hidden_states)

        num_frames_emb = torch.arange(num_frames, device=hidden_states.device)
        num_frames_emb = num_frames_emb
        num_frames_emb = num_frames_emb.repeat(batch_size, 1)
        num_frames_emb = num_frames_emb.reshape(-1)
        t_emb = self.time_proj(num_frames_emb)
        # import ipdb
        # ipdb.set_trace()

        # `Timesteps` does not contain any weights and will always return f32 tensors
        # but time_embedding might actually be running in fp16. so we need to cast here.
        # there might be better ways to encapsulate this.
        t_emb = t_emb.to(dtype=hidden_states.dtype)

        emb = self.time_pos_embed(t_emb)
        emb = emb[:, None, :]
        # print(self.time_mixer.alpha)
        # 2. Blocks
        for block, mamba_block, temporal_block in zip(
            self.transformer_blocks, self.mamba_blocks, self.temporal_transformer_blocks
        ):
            if self.training and self.gradient_checkpointing:
                hidden_states = torch.utils.checkpoint.checkpoint(
                    block,
                    hidden_states,
                    None,
                    encoder_hidden_states,
                    None,
                    None,
                    cross_attention_kwargs,
                    use_reentrant=False,
                )
            else:
                hidden_states = block(
                    hidden_states,
                    encoder_hidden_states=encoder_hidden_states,
                    cross_attention_kwargs=cross_attention_kwargs,
                )
            if self.training and self.gradient_checkpointing:
                hidden_states = torch.utils.checkpoint.checkpoint(
                    mamba_block,
                    hidden_states,
                    encoder_hidden_states[0],
                    torch.cat(
                        [
                            encoder_hidden_states[1][0].squeeze(1),
                            encoder_hidden_states[1][1].squeeze(1),
                        ],
                        dim=1,
                    ),
                    cross_attention_kwargs["ip_adapter_masks"],
                )
            else:
                hidden_states = mamba_block(
                    hidden_states,
                    encoder_hidden_states[0],
                    torch.cat(
                        [
                            encoder_hidden_states[1][0].squeeze(1),
                            encoder_hidden_states[1][1].squeeze(1),
                        ],
                        dim=1,
                    ),
                    cross_attention_kwargs["ip_adapter_masks"],
                )
            hidden_states_mix = hidden_states
            hidden_states_mix = hidden_states_mix + emb
            if self.training and self.gradient_checkpointing:

                hidden_states_mix = torch.utils.checkpoint.checkpoint(
                    temporal_block,
                    hidden_states_mix,
                    num_frames,
                    encoder_hidden_states_time,
                    use_reentrant=False,
                )

            else:
                hidden_states_mix = temporal_block(
                    hidden_states_mix,
                    num_frames=num_frames,
                    encoder_hidden_states=encoder_hidden_states_time,
                )
            hidden_states = self.time_mixer(
                x_spatial=hidden_states,
                x_temporal=hidden_states_mix,
                image_only_indicator=image_only_indicator,
            )

        # 3. Output
        hidden_states = self.proj_out(hidden_states)
        hidden_states = (
            hidden_states.reshape(batch_frames, height, width, inner_dim)
            .permute(0, 3, 1, 2)
            .contiguous()
        )

        output = hidden_states + residual

        if not return_dict:
            return (output,)

        return TransformerTemporalModelOutput(sample=output)


# 使用新的mamba结构，使用exp 和audio的context，使用新的mamba结构
class TransformerSpatioTemporalModel_new_mambaID_v10_two_ip(nn.Module):
    """
    A Transformer model for video-like data.

    Parameters:
        num_attention_heads (`int`, *optional*, defaults to 16): The number of heads to use for multi-head attention.
        attention_head_dim (`int`, *optional*, defaults to 88): The number of channels in each head.
        in_channels (`int`, *optional*):
            The number of channels in the input and output (specify if the input is **continuous**).
        out_channels (`int`, *optional*):
            The number of channels in the output (specify if the input is **continuous**).
        num_layers (`int`, *optional*, defaults to 1): The number of layers of Transformer blocks to use.
        cross_attention_dim (`int`, *optional*): The number of `encoder_hidden_states` dimensions to use.
    """

    def __init__(
        self,
        num_attention_heads: int = 16,
        attention_head_dim: int = 88,
        in_channels: int = 320,
        out_channels: Optional[int] = None,
        num_layers: int = 1,
        cross_attention_dim: Optional[int] = None,
    ):
        super().__init__()
        self.num_attention_heads = num_attention_heads
        self.attention_head_dim = attention_head_dim

        inner_dim = num_attention_heads * attention_head_dim
        self.inner_dim = inner_dim

        # 2. Define input layers
        self.in_channels = in_channels
        self.norm = torch.nn.GroupNorm(
            num_groups=32, num_channels=in_channels, eps=1e-6
        )
        self.proj_in = nn.Linear(in_channels, inner_dim)

        # 3. Define transformers blocks
        self.transformer_blocks = nn.ModuleList(
            [
                BasicTransformerBlock(
                    inner_dim,
                    num_attention_heads,
                    attention_head_dim,
                    cross_attention_dim=cross_attention_dim,
                )
                for d in range(num_layers)
            ]
        )

        # 3. Define transformers blocks
        # self_attention_cond = SS2D_cond(d_model=320,d_cond=1024, dropout=0.1, d_state=16, size=36, scan_type='scan', num_direction=4)
        # self_attention_cond = SS2D_cond(d_model=320,d_cond=1024,cond_size=32, dropout=0.1, d_state=16, size=72, scan_type='sweep', num_direction=2).cuda()
        self.mamba_blocks = nn.ModuleList(
            [
                SS2D_cond_v10(
                    d_model=in_channels,
                    d_cond=cross_attention_dim,
                    cond_size=32,
                    dropout=0.1,
                    d_state=16,
                    size=int(72 / (in_channels / 320)),
                    scan_type="sweep",
                    num_direction=2,
                )
                for d in range(num_layers)
            ]
        )
        time_mix_inner_dim = inner_dim
        self.temporal_transformer_blocks = nn.ModuleList(
            [
                TemporalBasicTransformerBlock(
                    inner_dim,
                    time_mix_inner_dim,
                    num_attention_heads,
                    attention_head_dim,
                    cross_attention_dim=cross_attention_dim,
                )
                for _ in range(num_layers)
            ]
        )

        time_embed_dim = in_channels * 4
        self.time_pos_embed = TimestepEmbedding(
            in_channels, time_embed_dim, out_dim=in_channels
        )
        self.time_proj = Timesteps(in_channels, True, 0)
        self.time_mixer = AlphaBlender(alpha=0.5, merge_strategy="learned_with_images")

        # 4. Define output layers
        self.out_channels = in_channels if out_channels is None else out_channels
        # TODO: should use out_channels for continuous projections
        self.proj_out = nn.Linear(inner_dim, in_channels)

        self.gradient_checkpointing = False

    def forward(
        self,
        hidden_states: torch.Tensor,
        encoder_hidden_states: Optional[torch.Tensor] = None,
        cross_attention_kwargs: Optional[Dict[str, Any]] = None,
        image_only_indicator: Optional[torch.Tensor] = None,
        return_dict: bool = True,
    ):
        """
        Args:
            hidden_states (`torch.FloatTensor` of shape `(batch size, channel, height, width)`):
                Input hidden_states.
            num_frames (`int`):
                The number of frames to be processed per batch. This is used to reshape the hidden states.
            encoder_hidden_states ( `torch.LongTensor` of shape `(batch size, encoder_hidden_states dim)`, *optional*):
                Conditional embeddings for cross attention layer. If not given, cross-attention defaults to
                self-attention.
            image_only_indicator (`torch.LongTensor` of shape `(batch size, num_frames)`, *optional*):
                A tensor indicating whether the input contains only images. 1 indicates that the input contains only
                images, 0 indicates that the input contains video frames.
            return_dict (`bool`, *optional*, defaults to `True`):
                Whether or not to return a [`~models.transformer_temporal.TransformerTemporalModelOutput`] instead of a plain
                tuple.

        Returns:
            [`~models.transformer_temporal.TransformerTemporalModelOutput`] or `tuple`:
                If `return_dict` is True, an [`~models.transformer_temporal.TransformerTemporalModelOutput`] is
                returned, otherwise a `tuple` where the first element is the sample tensor.
        """

        # 1. Input
        batch_frames, _, height, width = hidden_states.shape
        num_frames = image_only_indicator.shape[-1]
        batch_size = batch_frames // num_frames

        def spatial2time(time_context):
            # print(time_context.shape)

            time_context = time_context.reshape(
                batch_size, num_frames, time_context.shape[-2], time_context.shape[-1]
            )
            time_context = time_context.mean(dim=(1,), keepdim=True)

            # time_context = time_context.flatten(1,2)
            # time_context = time_context[:, None].repeat(
            #     1, height * width, 1, 1
            # )
            time_context = time_context.repeat(1, height * width, 1, 1)
            time_context = time_context.reshape(
                batch_size * height * width, -1, time_context.shape[-1]
            )
            # print(time_context.shape)
            return time_context

        # clip_context, ip_contexts = encoder_hidden_states
        # clip_context_new = spatial2time(clip_context)
        # ip_contexts_new = []
        # for ip_context in ip_contexts:
        #     ip_context_new = spatial2time(ip_context)
        #     ip_contexts_new.append(ip_context_new)

        if isinstance(encoder_hidden_states, tuple):
            clip_hidden_states, ip_hidden_states = encoder_hidden_states
            encoder_hidden_states_time = (
                spatial2time(clip_hidden_states),
                [spatial2time(ip_hidden_state) for ip_hidden_state in ip_hidden_states],
            )
        else:
            encoder_hidden_states_time = spatial2time(encoder_hidden_states)

        residual = hidden_states

        hidden_states = self.norm(hidden_states)
        inner_dim = hidden_states.shape[1]
        hidden_states = hidden_states.permute(0, 2, 3, 1).reshape(
            batch_frames, height * width, inner_dim
        )
        hidden_states = self.proj_in(hidden_states)

        num_frames_emb = torch.arange(num_frames, device=hidden_states.device)
        num_frames_emb = num_frames_emb
        num_frames_emb = num_frames_emb.repeat(batch_size, 1)
        num_frames_emb = num_frames_emb.reshape(-1)
        t_emb = self.time_proj(num_frames_emb)
        # import ipdb
        # ipdb.set_trace()

        # `Timesteps` does not contain any weights and will always return f32 tensors
        # but time_embedding might actually be running in fp16. so we need to cast here.
        # there might be better ways to encapsulate this.
        t_emb = t_emb.to(dtype=hidden_states.dtype)

        emb = self.time_pos_embed(t_emb)
        emb = emb[:, None, :]
        # print(self.time_mixer.alpha)
        # 2. Blocks
        for block, mamba_block, temporal_block in zip(
            self.transformer_blocks, self.mamba_blocks, self.temporal_transformer_blocks
        ):
            if self.training and self.gradient_checkpointing:
                hidden_states = torch.utils.checkpoint.checkpoint(
                    block,
                    hidden_states,
                    None,
                    encoder_hidden_states,
                    None,
                    None,
                    cross_attention_kwargs,
                    use_reentrant=False,
                )
            else:
                hidden_states = block(
                    hidden_states,
                    encoder_hidden_states=encoder_hidden_states,
                    cross_attention_kwargs=cross_attention_kwargs,
                )
            if self.training and self.gradient_checkpointing:
                hidden_states = torch.utils.checkpoint.checkpoint(
                    mamba_block,
                    hidden_states,
                    encoder_hidden_states[0],
                    torch.cat(
                        [
                            encoder_hidden_states[1][0].squeeze(1),
                            encoder_hidden_states[1][1].squeeze(1),
                        ],
                        dim=1,
                    ),
                    cross_attention_kwargs["ip_adapter_masks"],
                )
            else:
                hidden_states = mamba_block(
                    hidden_states,
                    encoder_hidden_states[0],
                    torch.cat(
                        [
                            encoder_hidden_states[1][0].squeeze(1),
                            encoder_hidden_states[1][1].squeeze(1),
                        ],
                        dim=1,
                    ),
                    cross_attention_kwargs["ip_adapter_masks"],
                )
            hidden_states_mix = hidden_states
            hidden_states_mix = hidden_states_mix + emb
            if self.training and self.gradient_checkpointing:

                hidden_states_mix = torch.utils.checkpoint.checkpoint(
                    temporal_block,
                    hidden_states_mix,
                    num_frames,
                    encoder_hidden_states_time,
                    use_reentrant=False,
                )

            else:
                hidden_states_mix = temporal_block(
                    hidden_states_mix,
                    num_frames=num_frames,
                    encoder_hidden_states=encoder_hidden_states_time,
                )
            hidden_states = self.time_mixer(
                x_spatial=hidden_states,
                x_temporal=hidden_states_mix,
                image_only_indicator=image_only_indicator,
            )

        # 3. Output
        hidden_states = self.proj_out(hidden_states)
        hidden_states = (
            hidden_states.reshape(batch_frames, height, width, inner_dim)
            .permute(0, 3, 1, 2)
            .contiguous()
        )

        output = hidden_states + residual

        if not return_dict:
            return (output,)

        return TransformerTemporalModelOutput(sample=output)


# ablation
# 使用新的mamba结构，使用exp 和audio的context，使用新的mamba结构
class TransformerSpatioTemporalModel_new_mambaID_v10_two_ip_wo_id(nn.Module):
    """
    A Transformer model for video-like data.

    Parameters:
        num_attention_heads (`int`, *optional*, defaults to 16): The number of heads to use for multi-head attention.
        attention_head_dim (`int`, *optional*, defaults to 88): The number of channels in each head.
        in_channels (`int`, *optional*):
            The number of channels in the input and output (specify if the input is **continuous**).
        out_channels (`int`, *optional*):
            The number of channels in the output (specify if the input is **continuous**).
        num_layers (`int`, *optional*, defaults to 1): The number of layers of Transformer blocks to use.
        cross_attention_dim (`int`, *optional*): The number of `encoder_hidden_states` dimensions to use.
    """

    def __init__(
        self,
        num_attention_heads: int = 16,
        attention_head_dim: int = 88,
        in_channels: int = 320,
        out_channels: Optional[int] = None,
        num_layers: int = 1,
        cross_attention_dim: Optional[int] = None,
    ):
        super().__init__()
        self.num_attention_heads = num_attention_heads
        self.attention_head_dim = attention_head_dim

        inner_dim = num_attention_heads * attention_head_dim
        self.inner_dim = inner_dim

        # 2. Define input layers
        self.in_channels = in_channels
        self.norm = torch.nn.GroupNorm(
            num_groups=32, num_channels=in_channels, eps=1e-6
        )
        self.proj_in = nn.Linear(in_channels, inner_dim)

        # 3. Define transformers blocks
        self.transformer_blocks = nn.ModuleList(
            [
                BasicTransformerBlock(
                    inner_dim,
                    num_attention_heads,
                    attention_head_dim,
                    cross_attention_dim=cross_attention_dim,
                )
                for d in range(num_layers)
            ]
        )

        # 3. Define transformers blocks
        # self_attention_cond = SS2D_cond(d_model=320,d_cond=1024, dropout=0.1, d_state=16, size=36, scan_type='scan', num_direction=4)
        # self_attention_cond = SS2D_cond(d_model=320,d_cond=1024,cond_size=32, dropout=0.1, d_state=16, size=72, scan_type='sweep', num_direction=2).cuda()
        self.mamba_blocks = nn.ModuleList(
            [
                SS2D_cond_v10_wo_id(
                    d_model=in_channels,
                    d_cond=cross_attention_dim,
                    cond_size=32,
                    dropout=0.1,
                    d_state=16,
                    size=int(72 / (in_channels / 320)),
                    scan_type="sweep",
                    num_direction=2,
                )
                for d in range(num_layers)
            ]
        )
        time_mix_inner_dim = inner_dim
        self.temporal_transformer_blocks = nn.ModuleList(
            [
                TemporalBasicTransformerBlock(
                    inner_dim,
                    time_mix_inner_dim,
                    num_attention_heads,
                    attention_head_dim,
                    cross_attention_dim=cross_attention_dim,
                )
                for _ in range(num_layers)
            ]
        )

        time_embed_dim = in_channels * 4
        self.time_pos_embed = TimestepEmbedding(
            in_channels, time_embed_dim, out_dim=in_channels
        )
        self.time_proj = Timesteps(in_channels, True, 0)
        self.time_mixer = AlphaBlender(alpha=0.5, merge_strategy="learned_with_images")

        # 4. Define output layers
        self.out_channels = in_channels if out_channels is None else out_channels
        # TODO: should use out_channels for continuous projections
        self.proj_out = nn.Linear(inner_dim, in_channels)

        self.gradient_checkpointing = False

    def forward(
        self,
        hidden_states: torch.Tensor,
        encoder_hidden_states: Optional[torch.Tensor] = None,
        cross_attention_kwargs: Optional[Dict[str, Any]] = None,
        image_only_indicator: Optional[torch.Tensor] = None,
        return_dict: bool = True,
    ):
        """
        Args:
            hidden_states (`torch.FloatTensor` of shape `(batch size, channel, height, width)`):
                Input hidden_states.
            num_frames (`int`):
                The number of frames to be processed per batch. This is used to reshape the hidden states.
            encoder_hidden_states ( `torch.LongTensor` of shape `(batch size, encoder_hidden_states dim)`, *optional*):
                Conditional embeddings for cross attention layer. If not given, cross-attention defaults to
                self-attention.
            image_only_indicator (`torch.LongTensor` of shape `(batch size, num_frames)`, *optional*):
                A tensor indicating whether the input contains only images. 1 indicates that the input contains only
                images, 0 indicates that the input contains video frames.
            return_dict (`bool`, *optional*, defaults to `True`):
                Whether or not to return a [`~models.transformer_temporal.TransformerTemporalModelOutput`] instead of a plain
                tuple.

        Returns:
            [`~models.transformer_temporal.TransformerTemporalModelOutput`] or `tuple`:
                If `return_dict` is True, an [`~models.transformer_temporal.TransformerTemporalModelOutput`] is
                returned, otherwise a `tuple` where the first element is the sample tensor.
        """

        # 1. Input
        batch_frames, _, height, width = hidden_states.shape
        num_frames = image_only_indicator.shape[-1]
        batch_size = batch_frames // num_frames

        def spatial2time(time_context):
            # print(time_context.shape)

            time_context = time_context.reshape(
                batch_size, num_frames, time_context.shape[-2], time_context.shape[-1]
            )
            time_context = time_context.mean(dim=(1,), keepdim=True)

            # time_context = time_context.flatten(1,2)
            # time_context = time_context[:, None].repeat(
            #     1, height * width, 1, 1
            # )
            time_context = time_context.repeat(1, height * width, 1, 1)
            time_context = time_context.reshape(
                batch_size * height * width, -1, time_context.shape[-1]
            )
            # print(time_context.shape)
            return time_context

        # clip_context, ip_contexts = encoder_hidden_states
        # clip_context_new = spatial2time(clip_context)
        # ip_contexts_new = []
        # for ip_context in ip_contexts:
        #     ip_context_new = spatial2time(ip_context)
        #     ip_contexts_new.append(ip_context_new)

        if isinstance(encoder_hidden_states, tuple):
            clip_hidden_states, ip_hidden_states = encoder_hidden_states
            encoder_hidden_states_time = (
                spatial2time(clip_hidden_states),
                [spatial2time(ip_hidden_state) for ip_hidden_state in ip_hidden_states],
            )
        else:
            encoder_hidden_states_time = spatial2time(encoder_hidden_states)

        residual = hidden_states

        hidden_states = self.norm(hidden_states)
        inner_dim = hidden_states.shape[1]
        hidden_states = hidden_states.permute(0, 2, 3, 1).reshape(
            batch_frames, height * width, inner_dim
        )
        hidden_states = self.proj_in(hidden_states)

        num_frames_emb = torch.arange(num_frames, device=hidden_states.device)
        num_frames_emb = num_frames_emb
        num_frames_emb = num_frames_emb.repeat(batch_size, 1)
        num_frames_emb = num_frames_emb.reshape(-1)
        t_emb = self.time_proj(num_frames_emb)
        # import ipdb
        # ipdb.set_trace()

        # `Timesteps` does not contain any weights and will always return f32 tensors
        # but time_embedding might actually be running in fp16. so we need to cast here.
        # there might be better ways to encapsulate this.
        t_emb = t_emb.to(dtype=hidden_states.dtype)

        emb = self.time_pos_embed(t_emb)
        emb = emb[:, None, :]
        # print(self.time_mixer.alpha)
        # 2. Blocks
        for block, mamba_block, temporal_block in zip(
            self.transformer_blocks, self.mamba_blocks, self.temporal_transformer_blocks
        ):
            if self.training and self.gradient_checkpointing:
                hidden_states = torch.utils.checkpoint.checkpoint(
                    block,
                    hidden_states,
                    None,
                    encoder_hidden_states,
                    None,
                    None,
                    cross_attention_kwargs,
                    use_reentrant=False,
                )
            else:
                hidden_states = block(
                    hidden_states,
                    encoder_hidden_states=encoder_hidden_states,
                    cross_attention_kwargs=cross_attention_kwargs,
                )
            if self.training and self.gradient_checkpointing:
                hidden_states = torch.utils.checkpoint.checkpoint(
                    mamba_block,
                    hidden_states,
                    encoder_hidden_states[0],
                    torch.cat(
                        [
                            encoder_hidden_states[1][0].squeeze(1),
                            encoder_hidden_states[1][1].squeeze(1),
                        ],
                        dim=1,
                    ),
                    cross_attention_kwargs["ip_adapter_masks"],
                )
            else:
                hidden_states = mamba_block(
                    hidden_states,
                    encoder_hidden_states[0],
                    torch.cat(
                        [
                            encoder_hidden_states[1][0].squeeze(1),
                            encoder_hidden_states[1][1].squeeze(1),
                        ],
                        dim=1,
                    ),
                    cross_attention_kwargs["ip_adapter_masks"],
                )
            hidden_states_mix = hidden_states
            hidden_states_mix = hidden_states_mix + emb
            if self.training and self.gradient_checkpointing:

                hidden_states_mix = torch.utils.checkpoint.checkpoint(
                    temporal_block,
                    hidden_states_mix,
                    num_frames,
                    encoder_hidden_states_time,
                    use_reentrant=False,
                )

            else:
                hidden_states_mix = temporal_block(
                    hidden_states_mix,
                    num_frames=num_frames,
                    encoder_hidden_states=encoder_hidden_states_time,
                )
            hidden_states = self.time_mixer(
                x_spatial=hidden_states,
                x_temporal=hidden_states_mix,
                image_only_indicator=image_only_indicator,
            )

        # 3. Output
        hidden_states = self.proj_out(hidden_states)
        hidden_states = (
            hidden_states.reshape(batch_frames, height, width, inner_dim)
            .permute(0, 3, 1, 2)
            .contiguous()
        )

        output = hidden_states + residual

        if not return_dict:
            return (output,)

        return TransformerTemporalModelOutput(sample=output)
