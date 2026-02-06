# Extracted from: C:\DEV\PyAgent\.external\Stream-Omni\stream_omni\model\language_model\stream_omni_llama.py
#    Copyright 2023 Haotian Liu
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.


import random
from copy import copy, deepcopy
from typing import List, Optional, Tuple, Union

import torch
import torch.nn as nn
import transformers
from torch import nn
from torch.nn import BCEWithLogitsLoss, CrossEntropyLoss, MSELoss
from transformers import AutoConfig, AutoModelForCausalLM, LlamaConfig
from transformers.activations import ACT2FN
from transformers.cache_utils import Cache, DynamicCache, StaticCache
from transformers.modeling_attn_mask_utils import AttentionMaskConverter
from transformers.modeling_flash_attention_utils import _flash_attention_forward
from transformers.modeling_outputs import (
    BaseModelOutputWithPast,
    CausalLMOutputWithPast,
    QuestionAnsweringModelOutput,
    SequenceClassifierOutputWithPast,
    TokenClassifierOutput,
)
from transformers.modeling_rope_utils import ROPE_INIT_FUNCTIONS
from transformers.modeling_utils import PreTrainedModel
from transformers.models.llama.configuration_llama import LlamaConfig
from transformers.pytorch_utils import ALL_LAYERNORM_LAYERS
from transformers.utils import (
    add_start_docstrings,
    add_start_docstrings_to_model_forward,
    is_flash_attn_greater_or_equal_2_10,
    logging,
    replace_return_docstrings,
)

logger = logging.get_logger(__name__)


import math
import re

from stream_omni.model.stream_omni_arch import (
    StreamOmniMetaForCausalLM,
    StreamOmniMetaModel,
)
from torch.linalg import det
from torch.nn.utils.rnn import pad_sequence
from transformers.generation.utils import GenerateOutput
from transformers.modeling_outputs import (
    BaseModelOutputWithPast,
    CausalLMOutputWithPast,
    QuestionAnsweringModelOutput,
    SequenceClassifierOutputWithPast,
    TokenClassifierOutput,
)
from transformers.utils import (
    add_start_docstrings_to_model_forward,
)

from .modeling_llama import (
    LLAMA_INPUTS_DOCSTRING,
    LlamaAttention,
    LlamaDecoderLayer,
    LlamaFlashAttention2,
    LlamaForCausalLM,
    LlamaMLP,
    LlamaModel,
    LlamaRMSNorm,
    LlamaRotaryEmbedding,
    LlamaSdpaAttention,
)


def remove_special_chars(text):
    punctuation_and_special_chars = r"[^\w\s。，\',\.、“”\"！？!?]"
    cleaned_text = re.sub(punctuation_and_special_chars, "", text)
    cleaned_text = (
        cleaned_text.replace("\n", " ").replace("\t", " ").replace("\r", " ").strip()
    )
    return cleaned_text


class StreamOmniConfig(LlamaConfig):
    model_type = "stream_omni_llama"
    temperature: float = 0.0  # reset to 0.0, previously 0.9 for Vicuna
    max_new_tokens: int = 1024
    do_sample: bool = False
    top_p: Optional[float] = None
    # rope_scaling: Optional[dict] = {}


def rotate_half(x):
    """Rotates half the hidden dims of the input."""
    x1 = x[..., : x.shape[-1] // 2]
    x2 = x[..., x.shape[-1] // 2 :]
    return torch.cat((-x2, x1), dim=-1)


def apply_rotary_pos_emb(h, cos, sin, position_ids=None, unsqueeze_dim=1):
    """Applies Rotary Position Embedding to the query and key tensors.

    Args:
        q (`torch.Tensor`): The query tensor.
        k (`torch.Tensor`): The key tensor.
        cos (`torch.Tensor`): The cosine part of the rotary embedding.
        sin (`torch.Tensor`): The sine part of the rotary embedding.
        position_ids (`torch.Tensor`, *optional*):
            Deprecated and unused.
        unsqueeze_dim (`int`, *optional*, defaults to 1):
            The 'unsqueeze_dim' argument specifies the dimension along which to unsqueeze cos[position_ids] and
            sin[position_ids] so that they can be properly broadcasted to the dimensions of q and k. For example, note
            that cos[position_ids] and sin[position_ids] have the shape [batch_size, seq_len, head_dim]. Then, if q and
            k have the shape [batch_size, heads, seq_len, head_dim], then setting unsqueeze_dim=1 makes
            cos[position_ids] and sin[position_ids] broadcastable to the shapes of q and k. Similarly, if q and k have
            the shape [batch_size, seq_len, heads, head_dim], then set unsqueeze_dim=2.
    Returns:
        `tuple(torch.Tensor)` comprising of the query and key tensors rotated using the Rotary Position Embedding.
    """
    cos = cos.unsqueeze(unsqueeze_dim)
    sin = sin.unsqueeze(unsqueeze_dim)
    h_embed = (h * cos) + (rotate_half(h) * sin)
    return h_embed


class MaskedLlamaAttention(nn.Module):
    """Multi-headed attention from 'Attention Is All You Need' paper"""

    def __init__(self, config: LlamaConfig, layer_idx: Optional[int] = None):
        super().__init__()
        self.config = config
        self.layer_idx = layer_idx
        if layer_idx is None:
            logger.warning_once(
                f"Instantiating {self.__class__.__name__} without passing a `layer_idx` is not recommended and will "
                "lead to errors during the forward call if caching is used. Please make sure to provide a `layer_idx` "
                "when creating this class."
            )

        self.attention_dropout = config.attention_dropout
        self.hidden_size = config.hidden_size
        self.num_heads = config.num_attention_heads
        self.head_dim = self.hidden_size // self.num_heads
        self.num_key_value_heads = self.num_heads
        self.num_key_value_groups = 1
        self.max_position_embeddings = config.max_position_embeddings
        # self.rope_theta = config.rope_theta
        self.is_causal = True

        if (self.head_dim * self.num_heads) != self.hidden_size:
            raise ValueError(
                f"hidden_size must be divisible by num_heads (got `hidden_size`: {self.hidden_size}"
                f" and `num_heads`: {self.num_heads})."
            )

        self.q_proj = nn.Linear(
            self.hidden_size, self.num_heads * self.head_dim, bias=config.attention_bias
        )
        self.k_proj = nn.Linear(
            self.hidden_size,
            self.num_key_value_heads * self.head_dim,
            bias=config.attention_bias,
        )
        self.v_proj = nn.Linear(
            self.hidden_size,
            self.num_key_value_heads * self.head_dim,
            bias=config.attention_bias,
        )
        self.o_proj = nn.Linear(
            self.hidden_size, self.hidden_size, bias=config.attention_bias
        )

        # TODO (joao): remove in v4.45 (RoPE is computed in the model, not in the decoder layers)
        self.rotary_emb = LlamaRotaryEmbedding(config=self.config)

    def forward(
        self,
        hidden_states: torch.Tensor,
        key_value_states: torch.Tensor,
        attention_mask: Optional[torch.Tensor] = None,
        simul_mask: Optional[torch.Tensor] = None,
        position_ids: Optional[torch.LongTensor] = None,
        text_position_ids: Optional[torch.LongTensor] = None,
        past_key_value: Optional[Cache] = None,
        output_attentions: bool = False,
        use_cache: bool = False,
        cache_position: Optional[torch.LongTensor] = None,
        position_embeddings: Optional[
            Tuple[torch.Tensor, torch.Tensor]
        ] = None,  # will become mandatory in v4.45
        text_position_embeddings: Optional[
            Tuple[torch.Tensor, torch.Tensor]
        ] = None,  # will become mandatory in v4.45
        **kwargs,
    ) -> Tuple[torch.Tensor, Optional[torch.Tensor], Optional[Tuple[torch.Tensor]]]:
        bsz, q_len, _ = hidden_states.size()
        bsz, kv_len, _ = key_value_states.size()

        query_states = self.q_proj(hidden_states)
        key_states = self.k_proj(key_value_states)
        value_states = self.v_proj(key_value_states)

        query_states = query_states.view(
            bsz, q_len, self.num_heads, self.head_dim
        ).transpose(1, 2)
        key_states = key_states.view(
            bsz, kv_len, self.num_key_value_heads, self.head_dim
        ).transpose(1, 2)
        value_states = value_states.view(
            bsz, kv_len, self.num_key_value_heads, self.head_dim
        ).transpose(1, 2)

        if position_embeddings is None:
            cos, sin = self.rotary_emb(value_states, position_ids)

        else:
            cos, sin = position_embeddings

        query_states = apply_rotary_pos_emb(query_states, cos, sin)

        if text_position_embeddings is None:
            t_cos, t_sin = self.rotary_emb(value_states, text_position_ids)
        else:
            t_cos, t_sin = text_position_embeddings
        key_states = apply_rotary_pos_emb(key_states, t_cos, t_sin)

        attn_weights = torch.matmul(
            query_states, key_states.transpose(2, 3)
        ) / math.sqrt(self.head_dim)

        if attention_mask is not None:  # no matter the length, we just slice it
            causal_mask = attention_mask[:, :, :, : key_states.shape[-2]]
            attn_weights = attn_weights + causal_mask

        if simul_mask is not None:  # no matter the length, we just slice it
            simul_mask, window_size = simul_mask
            window_size = window_size.unsqueeze(1).unsqueeze(3)
            tmp = (
                torch.arange(0, kv_len, device=simul_mask.device)
                .unsqueeze(0)
                .unsqueeze(1)
                .unsqueeze(2)
                .repeat(bsz, self.num_key_value_heads, q_len, 1)
            )
            mask_idx = (
                simul_mask.unsqueeze(1)
                .unsqueeze(3)
                .repeat(1, self.num_key_value_heads, 1, 1)
            )
            mask = ((mask_idx - window_size).clamp(min=0) <= tmp) & (tmp < mask_idx)
            attn_weights = attn_weights.masked_fill(~mask, -1e5)

        # upcast attention to fp32
        attn_weights = nn.functional.softmax(
            attn_weights, dim=-1, dtype=torch.float32
        ).to(query_states.dtype)
        attn_weights = nn.functional.dropout(
            attn_weights, p=self.attention_dropout, training=self.training
        )
        attn_output = torch.matmul(attn_weights, value_states)

        if attn_output.size() != (bsz, self.num_heads, q_len, self.head_dim):
            raise ValueError(
                f"`attn_output` should be of size {(bsz, self.num_heads, q_len, self.head_dim)}, but is"
                f" {attn_output.size()}"
            )

        attn_output = attn_output.transpose(1, 2).contiguous()

        attn_output = attn_output.reshape(bsz, q_len, -1)

        if self.config.pretraining_tp > 1:
            attn_output = attn_output.split(
                self.hidden_size // self.config.pretraining_tp, dim=2
            )
            o_proj_slices = self.o_proj.weight.split(
                self.hidden_size // self.config.pretraining_tp, dim=1
            )
            attn_output = sum(
                [
                    F.linear(attn_output[i], o_proj_slices[i])
                    for i in range(self.config.pretraining_tp)
                ]
            )
        else:
            attn_output = self.o_proj(attn_output)

        if not output_attentions:
            attn_weights = None

        return attn_output, attn_weights, past_key_value


LLAMA_ATTENTION_CLASSES = {
    "eager": LlamaAttention,
    "flash_attention_2": LlamaFlashAttention2,
    "sdpa": LlamaSdpaAttention,
}


class TopAudioLlamaDecoderLayer(nn.Module):
    def __init__(self, config: LlamaConfig, layer_idx: int):
        super().__init__()
        self.hidden_size = config.hidden_size

        self.self_attn = LLAMA_ATTENTION_CLASSES[config._attn_implementation](
            config=config, layer_idx=layer_idx
        )

        self.mlp = LlamaMLP(config)
        self.input_layernorm = LlamaRMSNorm(config.hidden_size, eps=config.rms_norm_eps)
        self.post_attention_layernorm = LlamaRMSNorm(
            config.hidden_size, eps=config.rms_norm_eps
        )

        self.audio_text_attn = MaskedLlamaAttention(config)

    def forward(
        self,
        hidden_states: torch.Tensor,
        attention_mask: Optional[torch.Tensor] = None,
        position_ids: Optional[torch.LongTensor] = None,
        text_position_ids: Optional[torch.LongTensor] = None,
        past_key_value: Optional[Cache] = None,
        output_attentions: Optional[bool] = False,
        use_cache: Optional[bool] = False,
        cache_position: Optional[torch.LongTensor] = None,
        position_embeddings: Optional[
            Tuple[torch.Tensor, torch.Tensor]
        ] = None,  # will become mandatory in v4.45
        text_position_embeddings: Optional[
            Tuple[torch.Tensor, torch.Tensor]
        ] = None,  # will become mandatory in v4.45
        text_rep=None,
        simul_mask=None,
        fusion_mask=None,
        **kwargs,
    ) -> Tuple[
        torch.FloatTensor, Optional[Tuple[torch.FloatTensor, torch.FloatTensor]]
    ]:
        """
        Args:
            hidden_states (`torch.FloatTensor`): input to the layer of shape `(batch, seq_len, embed_dim)`
            attention_mask (`torch.FloatTensor`, *optional*):
                attention mask of size `(batch_size, sequence_length)` if flash attention is used or `(batch_size, 1,
                query_sequence_length, key_sequence_length)` if default attention is used.
            output_attentions (`bool`, *optional*):
                Whether or not to return the attentions tensors of all attention layers. See `attentions` under
                returned tensors for more detail.
            use_cache (`bool`, *optional*):
                If set to `True`, `past_key_values` key value states are returned and can be used to speed up decoding
                (see `past_key_values`).
            past_key_value (`Tuple(torch.FloatTensor)`, *optional*): cached past key and value projection states
            cache_position (`torch.LongTensor` of shape `(sequence_length)`, *optional*):
                Indices depicting the position of the input sequence tokens in the sequence
            position_embeddings (`Tuple[torch.FloatTensor, torch.FloatTensor]`, *optional*):
                Tuple containing the cosine and sine positional embeddings of shape `(batch_size, seq_len, head_dim)`,
                with `head_dim` being the embedding dimension of each attention head.
            kwargs (`dict`, *optional*):
                Arbitrary kwargs to be ignored, used for FSDP and other methods that injects code
                into the model
        """
        residual = hidden_states

        hidden_states = self.input_layernorm(hidden_states)

        # Self Attention
        hidden_states, self_attn_weights, present_key_value = self.self_attn(
            hidden_states=hidden_states,
            attention_mask=attention_mask,
            position_ids=position_ids,
            past_key_value=past_key_value,
            output_attentions=output_attentions,
            use_cache=use_cache,
            cache_position=cache_position,
            position_embeddings=position_embeddings,
            **kwargs,
        )
        hidden_states = residual + hidden_states

        if text_rep is not None:
            if fusion_mask is not None:
                hidden_states = (
                    hidden_states
                    + self.audio_text_attn(
                        hidden_states,
                        text_rep,
                        simul_mask=simul_mask,
                        position_embeddings=position_embeddings,
                        text_position_embeddings=text_position_embeddings,
                    )[0]
                    * fusion_mask
                )
            else:
                position_embeddings = (
                    position_embeddings[0][:, -1:],
                    position_embeddings[1][:, -1:],
                )
                hidden_states[:, -1:] = (
                    hidden_states[:, -1:]
                    + self.audio_text_attn(
                        hidden_states[:, -1:],
                        text_rep,
                        position_embeddings=position_embeddings,
                        text_position_embeddings=text_position_embeddings,
                    )[0]
                )

        # Fully Connected
        residual = hidden_states
        hidden_states = self.post_attention_layernorm(hidden_states)
        hidden_states = self.mlp(hidden_states)
        hidden_states = residual + hidden_states

        outputs = (hidden_states,)

        if output_attentions:
            outputs += (self_attn_weights,)

        if use_cache:
            outputs += (present_key_value,)

        return outputs


class StreamOmniLlamaModel(StreamOmniMetaModel, LlamaModel):
    config_class = StreamOmniConfig

    def __init__(self, config: LlamaConfig):
        super(StreamOmniLlamaModel, self).__init__(config)
        self.audio_norm = LlamaRMSNorm(config.hidden_size, eps=config.rms_norm_eps)

        self.top_audio_norm = LlamaRMSNorm(config.hidden_size, eps=config.rms_norm_eps)
        self.embed_tokens = nn.Embedding(
            getattr(config, "text_vocab_size", config.vocab_size),
            config.hidden_size,
            self.padding_idx,
        )

        num_top_audio_layers = getattr(config, "num_top_audio_layers", 5)
        self.top_audio_layers = nn.ModuleList(
            [
                TopAudioLlamaDecoderLayer(config, layer_idx)
                for layer_idx in range(num_top_audio_layers)
            ]
        )

    @add_start_docstrings_to_model_forward(LLAMA_INPUTS_DOCSTRING)
    def forward(
        self,
        input_ids: torch.LongTensor = None,
        attention_mask: Optional[torch.Tensor] = None,
        position_ids: Optional[torch.LongTensor] = None,
        text_position_ids: Optional[torch.LongTensor] = None,
        past_key_values: Optional[Union[Cache, List[torch.FloatTensor]]] = None,
        inputs_embeds: Optional[torch.FloatTensor] = None,
        use_cache: Optional[bool] = None,
        output_attentions: Optional[bool] = None,
        output_hidden_states: Optional[bool] = None,
        return_dict: Optional[bool] = None,
        cache_position: Optional[torch.LongTensor] = None,
        layers_type="bottom_audio_layers,audio_to_text,llm_layers",
        audio_to_text_proj=None,
        lm_head=None,
        text_to_audio_proj=None,
        text_rep=None,
        simul_mask=None,
        fusion_mask=None,
    ) -> Union[Tuple, BaseModelOutputWithPast]:
        output_attentions = (
            output_attentions
            if output_attentions is not None
            else self.config.output_attentions
        )
        output_hidden_states = (
            output_hidden_states
            if output_hidden_states is not None
            else self.config.output_hidden_states
        )
        use_cache = use_cache if use_cache is not None else self.config.use_cache
        return_dict = (
            return_dict if return_dict is not None else self.config.use_return_dict
        )

        if (input_ids is None) ^ (inputs_embeds is not None):
            raise ValueError(
                "You cannot specify both input_ids and inputs_embeds at the same time, and must specify either one"
            )

        if self.gradient_checkpointing and self.training and use_cache:
            logger.warning_once(
                "`use_cache=True` is incompatible with gradient checkpointing. Setting `use_cache=False`."
            )
            use_cache = False

        if inputs_embeds is None:
            inputs_embeds = self.embed_tokens(input_ids)

        return_legacy_cache = False
        if use_cache and not isinstance(
            past_key_values, Cache
        ):  # kept for BC (non `Cache` `past_key_values` inputs)
            return_legacy_cache = True
            past_key_values = DynamicCache.from_legacy_cache(past_key_values)
            logger.warning_once(
                "We detected that you are passing `past_key_values` as a tuple and this is deprecated and will be removed in v4.43. "
                "Please use an appropriate `Cache` class (https://huggingface.co/docs/transformers/v4.41.3/en/internal/generation_utils#transformers.Cache)"
            )

        if cache_position is None:
            past_seen_tokens = (
                past_key_values.get_seq_length() if past_key_values is not None else 0
            )
            cache_position = torch.arange(
                past_seen_tokens,
                past_seen_tokens + inputs_embeds.shape[1],
                device=inputs_embeds.device,
            )
        if position_ids is None:
            position_ids = cache_position.unsqueeze(0)

        causal_mask = self._update_causal_mask(
            attention_mask,
            inputs_embeds,
            cache_position,
            past_key_values,
            output_attentions,
        )
        hidden_states = inputs_embeds
        # create position embeddings to be shared across the decoder layers
        position_embeddings = self.rotary_emb(hidden_states, position_ids)

        # decoder layers
        all_hidden_states = () if output_hidden_states else None
        all_self_attns = () if output_attentions else None
        next_decoder_cache = None

        forward_layers = []

        bottom_audio_layers_outputs = None

        if "bottom_audio_layers" in layers_type.split(","):
            final_norm = self.audio_norm
            for decoder_layer in self.bottom_audio_layers:
                if output_hidden_states:
                    all_hidden_states += (hidden_states,)

                if self.gradient_checkpointing and self.training:
                    layer_outputs = self._gradient_checkpointing_func(
                        decoder_layer.__call__,
                        hidden_states,
                        causal_mask,
                        position_ids,
                        past_key_values,
                        output_attentions,
                        use_cache,
                        cache_position,
                        position_embeddings,
                    )
                else:
                    layer_outputs = decoder_layer(
                        hidden_states,
                        attention_mask=causal_mask,
                        position_ids=position_ids,
                        past_key_value=past_key_values,
                        output_attentions=output_attentions,
                        use_cache=use_cache,
                        cache_position=cache_position,
                        position_embeddings=position_embeddings,
                    )

                hidden_states = layer_outputs[0]

                if use_cache:
                    next_decoder_cache = layer_outputs[2 if output_attentions else 1]

                if output_attentions:
                    all_self_attns += (layer_outputs[1],)
            hidden_states = final_norm(hidden_states)

        if "audio_to_text" in layers_type.split(","):
            # assert "bottom_audio_layers" in layers_type.split(",")
            if output_hidden_states:
                all_hidden_states += (hidden_states,)
            hidden_states = audio_to_text_proj(hidden_states)
            hidden_states = torch.matmul(
                hidden_states.softmax(dim=-1), self.embed_tokens.weight
            )

        if "llm_layers" in layers_type.split(","):
            final_norm = self.norm
            for decoder_layer in self.layers:
                if output_hidden_states:
                    all_hidden_states += (hidden_states,)

                if self.gradient_checkpointing and self.training:
                    layer_outputs = self._gradient_checkpointing_func(
                        decoder_layer.__call__,
                        hidden_states,
                        causal_mask,
                        position_ids,
                        past_key_values,
                        output_attentions,
                        use_cache,
                        cache_position,
                        position_embeddings,
                    )
                else:
                    layer_outputs = decoder_layer(
                        hidden_states,
                        attention_mask=causal_mask,
                        position_ids=position_ids,
                        past_key_value=past_key_values,
                        output_attentions=output_attentions,
                        use_cache=use_cache,
                        cache_position=cache_position,
                        position_embeddings=position_embeddings,
                    )

                hidden_states = layer_outputs[0]

                if use_cache:
                    next_decoder_cache = layer_outputs[2 if output_attentions else 1]
                if output_attentions:
                    all_self_attns += (layer_outputs[1],)

            hidden_states = final_norm(hidden_states)

        if "text_to_audio" in layers_type.split(","):
            if output_hidden_states:
                all_hidden_states += (hidden_states,)

            hidden_states = lm_head(hidden_states)
            hidden_states = torch.matmul(
                hidden_states.softmax(dim=-1),
                self.text_to_audio_proj.weight.type_as(hidden_states),
            )

        if "top_audio_layers" in layers_type.split(","):
            final_norm = self.top_audio_norm
            text_position_embeddings = self.rotary_emb(hidden_states, text_position_ids)

            for decoder_layer in self.top_audio_layers:
                if output_hidden_states:
                    all_hidden_states += (hidden_states,)
                if self.gradient_checkpointing and self.training:
                    layer_outputs = self._gradient_checkpointing_func(
                        decoder_layer.__call__,
                        hidden_states,
                        causal_mask,
                        position_ids,
                        text_position_ids,
                        past_key_values,
                        output_attentions,
                        use_cache,
                        cache_position,
                        position_embeddings,
                        text_position_embeddings,
                        text_rep,
                        simul_mask,
                        fusion_mask,
                    )
                else:
                    layer_outputs = decoder_layer(
                        hidden_states,
                        attention_mask=causal_mask,
                        position_ids=position_ids,
                        text_position_ids=text_position_ids,
                        past_key_value=past_key_values,
                        output_attentions=output_attentions,
                        use_cache=use_cache,
                        cache_position=cache_position,
                        position_embeddings=position_embeddings,
                        text_rep=text_rep,
                        simul_mask=simul_mask,
                        fusion_mask=fusion_mask,
                        text_position_embeddings=text_position_embeddings,
                    )

                hidden_states = layer_outputs[0]

                if use_cache:
                    next_decoder_cache = layer_outputs[2 if output_attentions else 1]

                if output_attentions:
                    all_self_attns += (layer_outputs[1],)

            hidden_states = final_norm(hidden_states)

        # add hidden states from the last decoder layer
        if output_hidden_states:
            all_hidden_states += (hidden_states,)

        next_cache = next_decoder_cache if use_cache else None
        if return_legacy_cache:
            next_cache = next_cache.to_legacy_cache()

        if not return_dict:
            return tuple(
                v
                for v in [hidden_states, next_cache, all_hidden_states, all_self_attns]
                if v is not None
            )
        return BaseModelOutputWithPast(
            last_hidden_state=hidden_states,
            past_key_values=next_cache,
            hidden_states=all_hidden_states,
            attentions=all_self_attns,
        )


class StreamOmniLlamaForCausalLM(LlamaForCausalLM, StreamOmniMetaForCausalLM):
    config_class = StreamOmniConfig

    def __init__(self, config):
        LlamaForCausalLM.__init__(self, config)

        # configure default generation settings
        config.model_type = "stream_omni_llama"
        # config.rope_scaling = None

        self.model = StreamOmniLlamaModel(config)
        self.lm_head = nn.Linear(
            config.hidden_size,
            getattr(config, "text_vocab_size", config.vocab_size),
            bias=False,
        )

        # Initialize weights and apply final processing
        self.post_init()
        self.audio_to_text_proj = nn.Linear(
            config.hidden_size,
            getattr(config, "text_vocab_size", config.vocab_size),
            bias=False,
        )
        self.audio_lm_head = nn.Linear(
            config.hidden_size, config.vocab_size, bias=False
        )
        self.text_to_audio_proj = nn.Embedding(
            config.vocab_size, config.hidden_size, config.pad_token_id
        )
        self.padding_idx = config.pad_token_id
        self.pre_llm_token = 128002
        self.pre_llm_id = None
        self.llm_ids = []
        self.prev_llm_ids = []
        self.outputs = None
        self.asr_ids = None
        self.tok = transformers.AutoTokenizer.from_pretrained(config._name_or_path)

    def reset(self, text=""):
        self.pre_llm_token = 128002
        self.pre_llm_id = None
        self.llm_ids = []
        self.prev_llm_ids = []
        self.asr_ids = None
        self.outputs = None
        self.res = self.tok(f"{text}<|eot_id|>", return_tensors="pt").input_ids
        self.res_id = 0

    def get_model(self):
        return self.model

    def forward(
        self,
        input_ids: torch.LongTensor = None,
        attention_mask: Optional[torch.Tensor] = None,
        position_ids: Optional[torch.LongTensor] = None,
        past_key_values: Optional[List[torch.FloatTensor]] = None,
        audio_past_key_values: Optional[List[torch.FloatTensor]] = None,
        top_audio_past_key_values: Optional[List[torch.FloatTensor]] = None,
        inputs_embeds: Optional[torch.FloatTensor] = None,
        inputs_embeds_proj: Optional[torch.FloatTensor] = None,
        fake_inputs_embeds: Optional[torch.FloatTensor] = None,
        labels: Optional[torch.LongTensor] = None,
        use_cache: Optional[bool] = None,
        output_attentions: Optional[bool] = None,
        output_hidden_states: Optional[bool] = None,
        images: Optional[torch.FloatTensor] = None,
        image_sizes: Optional[List[List[int]]] = None,
        return_dict: Optional[bool] = None,
        modalities: Optional[List[str]] = ["image"],
        dpo_forward: Optional[bool] = None,
        cache_position=None,
        audio_input_ids=None,
        audio_labels=None,
        text_input_ids=None,
        text_labels=None,
        audio_input_length=None,
        text_input_length=None,
        audio_attention_mask=None,
        text_attention_mask=None,
        bottom_audio_labels=None,
        inference_type=None,
        prefill_audio_rep=None,
    ) -> Union[Tuple, CausalLMOutputWithPast]:

        if inference_type == "speech_to_speech":
            if inputs_embeds is None:
                (
                    input_ids,
                    position_ids,
                    attention_mask,
                    past_key_values,
                    inputs_embeds,
                    labels,
                    fake_inputs_embeds,
                    bottom_audio_labels,
                    inputs_embeds_proj,
                ) = self.prepare_inputs_labels_for_multimodal_audio(
                    input_ids,
                    position_ids,
                    attention_mask,
                    past_key_values,
                    labels,
                    images,
                    modalities,
                    image_sizes,
                )

            return self.infer_speech_to_speech(
                input_ids=input_ids,
                attention_mask=attention_mask,
                position_ids=position_ids,
                past_key_values=past_key_values,
                audio_past_key_values=audio_past_key_values,
                top_audio_past_key_values=top_audio_past_key_values,
                inputs_embeds=inputs_embeds_proj,
                labels=labels,
                use_cache=use_cache,
                output_attentions=output_attentions,
                output_hidden_states=output_hidden_states,
                return_dict=return_dict,
                audio_input_ids=audio_input_ids,
                text_input_ids=text_input_ids,
                audio_input_length=audio_input_length,
                text_input_length=text_input_length,
                audio_attention_mask=audio_attention_mask,
                fake_inputs_embeds=fake_inputs_embeds,
                bottom_audio_labels=bottom_audio_labels,
                bottom_audio_rep=inputs_embeds,
                prefill_audio_rep=prefill_audio_rep,
            )

        if inference_type == "speech_to_text":
            if inputs_embeds is None:
                (
                    input_ids,
                    position_ids,
                    attention_mask,
                    past_key_values,
                    inputs_embeds,
                    labels,
                    fake_inputs_embeds,
                    bottom_audio_labels,
                    inputs_embeds_proj,
                ) = self.prepare_inputs_labels_for_multimodal_audio(
                    input_ids,
                    position_ids,
                    attention_mask,
                    past_key_values,
                    labels,
                    images,
                    modalities,
                    image_sizes,
                )

            return self.infer_speech_to_text(
                input_ids=input_ids,
                attention_mask=attention_mask,
                position_ids=position_ids,
                past_key_values=past_key_values,
                audio_past_key_values=audio_past_key_values,
                top_audio_past_key_values=top_audio_past_key_values,
                inputs_embeds=inputs_embeds_proj,
                labels=labels,
                use_cache=use_cache,
                output_attentions=output_attentions,
                output_hidden_states=output_hidden_states,
                return_dict=return_dict,
                audio_input_ids=audio_input_ids,
                text_input_ids=text_input_ids,
                audio_input_length=audio_input_length,
                text_input_length=text_input_length,
                audio_attention_mask=audio_attention_mask,
                fake_inputs_embeds=fake_inputs_embeds,
                bottom_audio_labels=bottom_audio_labels,
            )

        if inference_type == "text_to_speech":
            if inputs_embeds is None:
                (
                    input_ids,
                    position_ids,
                    attention_mask,
                    past_key_values,
                    inputs_embeds,
                    labels,
                ) = self.prepare_inputs_labels_for_multimodal(
                    input_ids,
                    position_ids,
                    attention_mask,
                    past_key_values,
                    labels,
                    images,
                    modalities,
                    image_sizes,
                )

            return self.infer_text_to_speech(
                input_ids=input_ids,
                attention_mask=attention_mask,
                position_ids=position_ids,
                past_key_values=past_key_values,
                audio_past_key_values=audio_past_key_values,
                top_audio_past_key_values=top_audio_past_key_values,
                inputs_embeds=inputs_embeds,
                labels=labels,
                use_cache=use_cache,
                output_attentions=output_attentions,
                output_hidden_states=output_hidden_states,
                return_dict=return_dict,
                audio_input_ids=audio_input_ids,
                text_input_ids=text_input_ids,
                audio_input_length=audio_input_length,
                text_input_length=text_input_length,
                audio_attention_mask=audio_attention_mask,
                prefill_audio_rep=prefill_audio_rep,
            )

        if inference_type == "text_to_text":
            if inputs_embeds is None:
                (
                    input_ids,
                    position_ids,
                    attention_mask,
                    past_key_values,
                    inputs_embeds,
                    labels,
                ) = self.prepare_inputs_labels_for_multimodal(
                    input_ids,
                    position_ids,
                    attention_mask,
                    past_key_values,
                    labels,
                    images,
                    modalities,
                    image_sizes,
                )

            return self.infer_text_to_text(
                input_ids=input_ids,
                attention_mask=attention_mask,
                position_ids=position_ids,
                past_key_values=past_key_values,
                audio_past_key_values=audio_past_key_values,
                top_audio_past_key_values=top_audio_past_key_values,
                inputs_embeds=inputs_embeds,
                labels=labels,
                use_cache=use_cache,
                output_attentions=output_attentions,
                output_hidden_states=output_hidden_states,
                return_dict=return_dict,
                audio_input_ids=audio_input_ids,
                text_input_ids=text_input_ids,
                audio_input_length=audio_input_length,
                text_input_length=text_input_length,
                audio_attention_mask=audio_attention_mask,
            )

    @add_start_docstrings_to_model_forward(LLAMA_INPUTS_DOCSTRING)
    @replace_return_docstrings(
        output_type=CausalLMOutputWithPast, config_class="LlamaConfig"
    )
    def infer_speech_to_speech(
        self,
        input_ids: torch.LongTensor = None,
        attention_mask: Optional[torch.Tensor] = None,
        position_ids: Optional[torch.LongTensor] = None,
        past_key_values: Optional[Union[Cache, List[torch.FloatTensor]]] = None,
        audio_past_key_values: Optional[Union[Cache, List[torch.FloatTensor]]] = None,
        top_audio_past_key_values: Optional[
            Union[Cache, List[torch.FloatTensor]]
        ] = None,
        inputs_embeds: Optional[torch.FloatTensor] = None,
        labels: Optional[torch.LongTensor] = None,
        use_cache: Optional[bool] = None,
        output_attentions: Optional[bool] = None,
        output_hidden_states: Optional[bool] = None,
        return_dict: Optional[bool] = None,
        cache_position: Optional[torch.LongTensor] = None,
        audio_input_ids=None,
        text_input_ids=None,
        audio_input_length=None,
        text_input_length=None,
        audio_attention_mask=None,
        layers_type="llm_layers",
        fake_inputs_embeds=None,
        bottom_audio_labels=None,
        bottom_audio_rep=None,
        prefill_audio_rep=None,
    ) -> Union[Tuple, CausalLMOutputWithPast]:
        r"""
        Args:
            labels (`torch.LongTensor` of shape `(batch_size, sequence_length)`, *optional*):
                Labels for computing the masked language modeling loss. Indices should either be in `[0, ...,
                config.vocab_size]` or -100 (see `input_ids` docstring). Tokens with indices set to `-100` are ignored
                (masked), the loss is only computed for the tokens with labels in `[0, ..., config.vocab_size]`.

        Returns:

        Example:

        ```python
        >>> from transformers import AutoTokenizer, LlamaForCausalLM

        >>> model = LlamaForCausalLM.from_pretrained("meta-llama/Llama-2-7b-hf")
        >>> tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-hf")

        >>> prompt = "Hey, are you conscious? Can you talk to me?"
        >>> inputs = tokenizer(prompt, return_tensors="pt")

        >>> # Generate
        >>> generate_ids = model.generate(inputs.input_ids, max_length=30)
        >>> tokenizer.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
        "Hey, are you conscious? Can you talk to me?\nI'm not conscious, but I can talk to you."
        ```"""

        output_attentions = (
            output_attentions
            if output_attentions is not None
            else self.config.output_attentions
        )
        output_hidden_states = (
            output_hidden_states
            if output_hidden_states is not None
            else self.config.output_hidden_states
        )
        return_dict = (
            return_dict if return_dict is not None else self.config.use_return_dict
        )

        llm_inputs_embeds = None
        if input_ids is not None:
            inputs_embeds, inputs_embeds_proj, bottom_audio_labels = self.encode_audio(
                input_ids.clamp(min=0), past_key_values=audio_past_key_values
            )
            input_ids = None
            bottom_audio_rep = inputs_embeds

            if (
                bottom_audio_labels.item() != 128002
                and bottom_audio_labels.item() != self.pre_llm_token
            ):
                llm_inputs_embeds = inputs_embeds_proj
                self.pre_llm_token = bottom_audio_labels.item()
                self.blank_num = 0
                # print(bottom_audio_labels,self.tok.decode(bottom_audio_labels.clamp(min=0)[0], skip_special_tokens=True).strip())
            else:
                llm_inputs_embeds = None
                self.blank_num += 1
        else:
            llm_inputs_embeds = inputs_embeds
            self.blank_num = 0
            # print(self.tok.decode(bottom_audio_labels[0].clamp(min=0), skip_special_tokens=True).strip())
            self.asr_ids = bottom_audio_labels.clamp(min=0)

        top_audio_in = bottom_audio_rep
        if llm_inputs_embeds is not None:
            # lagging 3 text tokens before generating speech
            gen_len = max(3, len(self.prev_llm_ids) + 1)
            while len(self.prev_llm_ids) < gen_len:
                if len(self.prev_llm_ids) > 0 and self.pre_llm_id.item() == 128009:
                    break
                if self.pre_llm_id is not None:
                    llm_inputs_embeds = self.model.embed_tokens(self.pre_llm_id)
                outputs = self.model(
                    input_ids=None,
                    attention_mask=attention_mask,
                    position_ids=None,
                    past_key_values=past_key_values,
                    inputs_embeds=llm_inputs_embeds,
                    use_cache=use_cache,
                    output_attentions=output_attentions,
                    output_hidden_states=True,
                    return_dict=return_dict,
                    cache_position=None,
                    layers_type="llm_layers",
                )
                self.outputs = deepcopy(outputs)
                llm_rep = self.lm_head(outputs[0])
                llm_id = llm_rep.argmax(dim=-1)
                self.pre_llm_id = llm_id[:, -1:]
                self.llm_ids.append(self.pre_llm_id)
                if remove_special_chars(self.tok.decode(self.pre_llm_id[0])) != "":
                    self.prev_llm_ids.append(self.pre_llm_id)

                # if use hidden states of LLM
                # text_llm_rep=torch.matmul((llm_rep[:, -1:]/0.01).softmax(dim=-1).type_as(llm_rep),self.text_to_audio_proj.weight.type_as(llm_rep))
                # self.prev_llm_ids.append(text_llm_rep.cpu())

        window_size = 5
        text_rep = self.text_to_audio_proj(
            torch.cat(self.prev_llm_ids[-1 * window_size :], dim=-1)
        )

        # if use hidden states of LLM
        # text_rep=torch.cat(self.prev_llm_ids[-5:],dim=-2).to(top_audio_in.device)

        text_position_ids = (
            torch.arange(
                max(0, len(self.prev_llm_ids) - window_size),
                len(self.prev_llm_ids),
                device=text_rep.device,
            )
            .unsqueeze(0)
            .type_as(self.pre_llm_id)
        )

        is_image = None
        if fake_inputs_embeds is not None:
            try:
                is_image = fake_inputs_embeds.sum(dim=-1) == 0
                hidden_states_wo_image = [
                    top_audio_in[i][~is_image[i]] for i in range(top_audio_in.size(0))
                ]
                hidden_states_wo_image = torch.stack(hidden_states_wo_image)

            except:
                is_image = None
                hidden_states_wo_image = top_audio_in
                pass

        else:
            hidden_states_wo_image = top_audio_in

        if is_image is not None and attention_mask is not None:
            top_audio_attention_mask = [
                attention_mask[i][~is_image[i]] for i in range(attention_mask.size(0))
            ]
            top_audio_attention_mask = torch.stack(top_audio_attention_mask)
        else:
            top_audio_attention_mask = attention_mask

        top_audio_outputs = self.decode_audio(
            hidden_states_wo_image,
            text_rep=text_rep,
            text_position_ids=text_position_ids,
            attention_mask=top_audio_attention_mask,
            past_key_values=top_audio_past_key_values,
        )

        hidden_states = top_audio_outputs[0]
        if self.config.pretraining_tp > 1:
            lm_head_slices = self.audio_lm_head.weight.split(
                self.vocab_size // self.config.pretraining_tp, dim=0
            )
            logits = [
                F.linear(hidden_states, lm_head_slices[i])
                for i in range(self.config.pretraining_tp)
            ]
            logits = torch.cat(logits, dim=-1)
        else:
            logits = self.audio_lm_head(hidden_states)
        logits = logits.float()

        return CausalLMOutputWithPast(
            loss=None,
            logits=logits,
            past_key_values=self.outputs.past_key_values,
            hidden_states=None,
            attentions=None,
        )

    @add_start_docstrings_to_model_forward(LLAMA_INPUTS_DOCSTRING)
    @replace_return_docstrings(
        output_type=CausalLMOutputWithPast, config_class="LlamaConfig"
    )
    def infer_text_to_speech(
        self,
        input_ids: torch.LongTensor = None,
        attention_mask: Optional[torch.Tensor] = None,
        position_ids: Optional[torch.LongTensor] = None,
        past_key_values: Optional[Union[Cache, List[torch.FloatTensor]]] = None,
        audio_past_key_values: Optional[Union[Cache, List[torch.FloatTensor]]] = None,
        top_audio_past_key_values: Optional[
            Union[Cache, List[torch.FloatTensor]]
        ] = None,
        inputs_embeds: Optional[torch.FloatTensor] = None,
        labels: Optional[torch.LongTensor] = None,
        use_cache: Optional[bool] = None,
        output_attentions: Optional[bool] = None,
        output_hidden_states: Optional[bool] = None,
        return_dict: Optional[bool] = None,
        cache_position: Optional[torch.LongTensor] = None,
        audio_input_ids=None,
        text_input_ids=None,
        audio_input_length=None,
        text_input_length=None,
        audio_attention_mask=None,
        layers_type="llm_layers",
        fake_inputs_embeds=None,
        bottom_audio_labels=None,
        prefill_audio_rep=None,
    ) -> Union[Tuple, CausalLMOutputWithPast]:
        r"""
        Args:
            labels (`torch.LongTensor` of shape `(batch_size, sequence_length)`, *optional*):
                Labels for computing the masked language modeling loss. Indices should either be in `[0, ...,
                config.vocab_size]` or -100 (see `input_ids` docstring). Tokens with indices set to `-100` are ignored
                (masked), the loss is only computed for the tokens with labels in `[0, ..., config.vocab_size]`.

        Returns:

        Example:

        ```python
        >>> from transformers import AutoTokenizer, LlamaForCausalLM

        >>> model = LlamaForCausalLM.from_pretrained("meta-llama/Llama-2-7b-hf")
        >>> tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-hf")

        >>> prompt = "Hey, are you conscious? Can you talk to me?"
        >>> inputs = tokenizer(prompt, return_tensors="pt")

        >>> # Generate
        >>> generate_ids = model.generate(inputs.input_ids, max_length=30)
        >>> tokenizer.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
        "Hey, are you conscious? Can you talk to me?\nI'm not conscious, but I can talk to you."
        ```"""

        output_attentions = (
            output_attentions
            if output_attentions is not None
            else self.config.output_attentions
        )
        output_hidden_states = (
            output_hidden_states
            if output_hidden_states is not None
            else self.config.output_hidden_states
        )
        return_dict = (
            return_dict if return_dict is not None else self.config.use_return_dict
        )

        gen_new_token = False
        llm_inputs_embeds = None
        if input_ids is not None:

            _inputs_embeds, inputs_embeds_proj, bottom_audio_labels = self.encode_audio(
                input_ids.clamp(min=0), past_key_values=audio_past_key_values
            )
            input_ids = None

            if (
                bottom_audio_labels.item() != 128002
                and bottom_audio_labels.item() != self.pre_llm_token
            ):
                llm_inputs_embeds = inputs_embeds
                self.pre_llm_token = bottom_audio_labels.item()
                self.blank_num = 0

                print(
                    bottom_audio_labels,
                    self.tok.decode(
                        bottom_audio_labels.clamp(min=0)[0], skip_special_tokens=True
                    ).strip(),
                )
                gen_new_token = True
            else:
                llm_inputs_embeds = None
                self.blank_num += 1
                gen_new_token = False

            top_audio_in = _inputs_embeds
        else:
            llm_inputs_embeds = inputs_embeds
            top_audio_in = prefill_audio_rep
            self.blank_num = 0
            gen_new_token = True

        if gen_new_token:
            gen_len = max(3, len(self.prev_llm_ids) + 1)
            if len(self.prev_llm_ids) > 0 and (
                self.prev_llm_ids[-1].item() == 128009
                or self.prev_llm_ids[-1].item() == 128002
            ):
                gen_len = len(self.prev_llm_ids)

            while len(self.prev_llm_ids) < gen_len:
                if (
                    len(self.prev_llm_ids) > 0
                    and self.prev_llm_ids[-1].item() == 128009
                ):
                    break
                if self.pre_llm_id is not None:
                    llm_inputs_embeds = self.model.embed_tokens(self.pre_llm_id)
                outputs = self.model(
                    input_ids=None,
                    attention_mask=attention_mask,
                    position_ids=None,
                    past_key_values=past_key_values,
                    inputs_embeds=llm_inputs_embeds,
                    use_cache=use_cache,
                    output_attentions=output_attentions,
                    output_hidden_states=True,
                    return_dict=return_dict,
                    cache_position=None,
                    layers_type="llm_layers",
                )
                self.outputs = deepcopy(outputs)
                llm_rep = self.lm_head(outputs[0])
                llm_id = llm_rep.argmax(dim=-1)
                self.pre_llm_id = llm_id[:, -1:]
                self.llm_ids.append(self.pre_llm_id)
                if remove_special_chars(self.tok.decode(self.pre_llm_id[0])) != "":
                    self.prev_llm_ids.append(self.pre_llm_id)

                # if use hidden states of LLM
                # text_llm_rep=torch.matmul((llm_rep[:, -1:]/0.01).softmax(dim=-1).type_as(llm_rep),self.text_to_audio_proj.weight.type_as(llm_rep))
                # self.prev_llm_ids.append(text_llm_rep.cpu())

        window_size = 5
        text_rep = self.text_to_audio_proj(
            torch.cat(self.prev_llm_ids[-1 * window_size :], dim=-1)
        )

        # if use hidden states of LLM
        # text_rep=torch.cat(self.prev_llm_ids[-5:],dim=-2).to(top_audio_in.device)

        text_position_ids = (
            torch.arange(
                max(0, len(self.prev_llm_ids) - window_size),
                len(self.prev_llm_ids),
                device=text_rep.device,
            )
            .unsqueeze(0)
            .type_as(self.pre_llm_id)
        )

        is_image = None
        if fake_inputs_embeds is not None:
            try:
                is_image = fake_inputs_embeds.sum(dim=-1) == 0
                hidden_states_wo_image = [
                    top_audio_in[i][~is_image[i]] for i in range(top_audio_in.size(0))
                ]
                hidden_states_wo_image = torch.stack(hidden_states_wo_image)

            except:
                is_image = None
                hidden_states_wo_image = top_audio_in
                pass

        else:
            hidden_states_wo_image = top_audio_in

        if is_image is not None and attention_mask is not None:
            top_audio_attention_mask = [
                attention_mask[i][~is_image[i]] for i in range(attention_mask.size(0))
            ]
            top_audio_attention_mask = torch.stack(top_audio_attention_mask)
        else:
            top_audio_attention_mask = attention_mask

        top_audio_outputs = self.decode_audio(
            hidden_states_wo_image,
            text_rep=text_rep,
            text_position_ids=text_position_ids,
            attention_mask=top_audio_attention_mask,
            past_key_values=top_audio_past_key_values,
        )

        hidden_states = top_audio_outputs[0]
        if self.config.pretraining_tp > 1:
            lm_head_slices = self.audio_lm_head.weight.split(
                self.vocab_size // self.config.pretraining_tp, dim=0
            )
            logits = [
                F.linear(hidden_states, lm_head_slices[i])
                for i in range(self.config.pretraining_tp)
            ]
            logits = torch.cat(logits, dim=-1)
        else:
            logits = self.audio_lm_head(hidden_states)
        logits = logits.float()

        return CausalLMOutputWithPast(
            loss=None,
            logits=logits,
            past_key_values=self.outputs.past_key_values,
            hidden_states=None,
            attentions=None,
        )

    @add_start_docstrings_to_model_forward(LLAMA_INPUTS_DOCSTRING)
    @replace_return_docstrings(
        output_type=CausalLMOutputWithPast, config_class="LlamaConfig"
    )
    def infer_text_to_text(
        self,
        input_ids: torch.LongTensor = None,
        attention_mask: Optional[torch.Tensor] = None,
        position_ids: Optional[torch.LongTensor] = None,
        past_key_values: Optional[Union[Cache, List[torch.FloatTensor]]] = None,
        audio_past_key_values: Optional[Union[Cache, List[torch.FloatTensor]]] = None,
        top_audio_past_key_values: Optional[
            Union[Cache, List[torch.FloatTensor]]
        ] = None,
        inputs_embeds: Optional[torch.FloatTensor] = None,
        labels: Optional[torch.LongTensor] = None,
        use_cache: Optional[bool] = None,
        output_attentions: Optional[bool] = None,
        output_hidden_states: Optional[bool] = None,
        return_dict: Optional[bool] = None,
        cache_position: Optional[torch.LongTensor] = None,
        audio_input_ids=None,
        text_input_ids=None,
        audio_input_length=None,
        text_input_length=None,
        audio_attention_mask=None,
        layers_type="llm_layers,text_to_audio,top_audio_layers",
        fake_inputs_embeds=None,
        bottom_audio_labels=None,
    ) -> Union[Tuple, CausalLMOutputWithPast]:
        r"""
        Args:
            labels (`torch.LongTensor` of shape `(batch_size, sequence_length)`, *optional*):
                Labels for computing the masked language modeling loss. Indices should either be in `[0, ...,
                config.vocab_size]` or -100 (see `input_ids` docstring). Tokens with indices set to `-100` are ignored
                (masked), the loss is only computed for the tokens with labels in `[0, ..., config.vocab_size]`.

        Returns:

        Example:

        ```python
        >>> from transformers import AutoTokenizer, LlamaForCausalLM

        >>> model = LlamaForCausalLM.from_pretrained("meta-llama/Llama-2-7b-hf")
        >>> tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-hf")

        >>> prompt = "Hey, are you conscious? Can you talk to me?"
        >>> inputs = tokenizer(prompt, return_tensors="pt")

        >>> # Generate
        >>> generate_ids = model.generate(inputs.input_ids, max_length=30)
        >>> tokenizer.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
        "Hey, are you conscious? Can you talk to me?\nI'm not conscious, but I can talk to you."
        ```"""

        output_attentions = (
            output_attentions
            if output_attentions is not None
            else self.config.output_attentions
        )
        output_hidden_states = (
            output_hidden_states
            if output_hidden_states is not None
            else self.config.output_hidden_states
        )
        return_dict = (
            return_dict if return_dict is not None else self.config.use_return_dict
        )

        outputs = self.model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            position_ids=position_ids,
            past_key_values=past_key_values,
            inputs_embeds=inputs_embeds,
            use_cache=use_cache,
            output_attentions=output_attentions,
            output_hidden_states=True,
            return_dict=return_dict,
            cache_position=cache_position,
            # audio_to_text_proj=self.audio_to_text_proj,
            layers_type="llm_layers",
            # text_to_audio_proj=self.text_to_audio_proj,
        )

        hidden_states = outputs[0]
        if self.config.pretraining_tp > 1:
            lm_head_slices = self.lm_head.weight.split(
                self.vocab_size // self.config.pretraining_tp, dim=0
            )
            logits = [
                F.linear(hidden_states, lm_head_slices[i])
                for i in range(self.config.pretraining_tp)
            ]
            logits = torch.cat(logits, dim=-1)
        else:
            logits = self.lm_head(hidden_states)
        logits = logits.float()

        loss = None

        return CausalLMOutputWithPast(
            loss=loss,
            logits=logits,
            past_key_values=outputs.past_key_values,
            hidden_states=outputs.hidden_states,
            attentions=outputs.attentions,
        )

    @add_start_docstrings_to_model_forward(LLAMA_INPUTS_DOCSTRING)
    @replace_return_docstrings(
        output_type=CausalLMOutputWithPast, config_class="LlamaConfig"
    )
    def infer_speech_to_text(
        self,
        input_ids: torch.LongTensor = None,
        attention_mask: Optional[torch.Tensor] = None,
        position_ids: Optional[torch.LongTensor] = None,
        past_key_values: Optional[Union[Cache, List[torch.FloatTensor]]] = None,
        audio_past_key_values: Optional[Union[Cache, List[torch.FloatTensor]]] = None,
        top_audio_past_key_values: Optional[
            Union[Cache, List[torch.FloatTensor]]
        ] = None,
        inputs_embeds: Optional[torch.FloatTensor] = None,
        labels: Optional[torch.LongTensor] = None,
        use_cache: Optional[bool] = None,
        output_attentions: Optional[bool] = None,
        output_hidden_states: Optional[bool] = None,
        return_dict: Optional[bool] = None,
        cache_position: Optional[torch.LongTensor] = None,
        audio_input_ids=None,
        text_input_ids=None,
        audio_input_length=None,
        text_input_length=None,
        audio_attention_mask=None,
        layers_type="llm_layers,text_to_audio,top_audio_layers",
        fake_inputs_embeds=None,
        bottom_audio_labels=None,
    ) -> Union[Tuple, CausalLMOutputWithPast]:
        r"""
        Args:
            labels (`torch.LongTensor` of shape `(batch_size, sequence_length)`, *optional*):
                Labels for computing the masked language modeling loss. Indices should either be in `[0, ...,
                config.vocab_size]` or -100 (see `input_ids` docstring). Tokens with indices set to `-100` are ignored
                (masked), the loss is only computed for the tokens with labels in `[0, ..., config.vocab_size]`.

        Returns:

        Example:

        ```python
        >>> from transformers import AutoTokenizer, LlamaForCausalLM

        >>> model = LlamaForCausalLM.from_pretrained("meta-llama/Llama-2-7b-hf")
        >>> tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-hf")

        >>> prompt = "Hey, are you conscious? Can you talk to me?"
        >>> inputs = tokenizer(prompt, return_tensors="pt")

        >>> # Generate
        >>> generate_ids = model.generate(inputs.input_ids, max_length=30)
        >>> tokenizer.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
        "Hey, are you conscious? Can you talk to me?\nI'm not conscious, but I can talk to you."
        ```"""

        output_attentions = (
            output_attentions
            if output_attentions is not None
            else self.config.output_attentions
        )
        output_hidden_states = (
            output_hidden_states
            if output_hidden_states is not None
            else self.config.output_hidden_states
        )
        return_dict = (
            return_dict if return_dict is not None else self.config.use_return_dict
        )
        if input_ids is None:
            print(
                self.tok.decode(
                    bottom_audio_labels[0].clamp(min=0), skip_special_tokens=True
                ).strip()
            )

        outputs = self.model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            position_ids=position_ids,
            past_key_values=past_key_values,
            inputs_embeds=inputs_embeds,
            use_cache=use_cache,
            output_attentions=output_attentions,
            output_hidden_states=True,
            return_dict=return_dict,
            cache_position=cache_position,
            layers_type="llm_layers",
        )

        hidden_states = outputs[0]
        if self.config.pretraining_tp > 1:
            lm_head_slices = self.lm_head.weight.split(
                self.vocab_size // self.config.pretraining_tp, dim=0
            )
            logits = [
                F.linear(hidden_states, lm_head_slices[i])
                for i in range(self.config.pretraining_tp)
            ]
            logits = torch.cat(logits, dim=-1)
        else:
            logits = self.lm_head(hidden_states)
        logits = logits.float()
        loss = None

        return CausalLMOutputWithPast(
            loss=loss,
            logits=logits,
            past_key_values=outputs.past_key_values,
            hidden_states=outputs.hidden_states,
            attentions=outputs.attentions,
        )

    @torch.no_grad()
    def generate(
        self,
        inputs: Optional[torch.Tensor] = None,
        images: Optional[torch.Tensor] = None,
        image_sizes: Optional[torch.Tensor] = None,
        modalities: Optional[List[str]] = ["image"],
        inference_type="speech_to_speech",
        prefill_audio_ids=None,
        **kwargs,
    ) -> Union[GenerateOutput, torch.LongTensor]:
        modalities = (
            kwargs.pop("modalities", None)
            if "modalities" in kwargs and modalities is None
            else modalities
        )
        position_ids = kwargs.pop("position_ids", None)
        attention_mask = kwargs.pop("attention_mask", None)
        if "inputs_embeds" in kwargs:
            raise NotImplementedError("`inputs_embeds` is not supported")
        audio_past_key_values = ()
        audio_past_key_values = DynamicCache.from_legacy_cache(audio_past_key_values)
        top_audio_past_key_values = ()
        top_audio_past_key_values = DynamicCache.from_legacy_cache(
            top_audio_past_key_values
        )
        kwargs["audio_past_key_values"] = audio_past_key_values
        kwargs["top_audio_past_key_values"] = top_audio_past_key_values

        # for text-to-speech interaction, add the prefill audio_ids
        if prefill_audio_ids is not None and len(audio_past_key_values) == 0:
            prefill_audio_rep, _, _ = self.encode_audio(
                prefill_audio_ids, past_key_values=audio_past_key_values
            )
            kwargs["prefill_audio_rep"] = prefill_audio_rep
        fake_inputs_embeds = None
        bottom_audio_labels = None
        if images is not None:
            if inference_type in ["speech_to_speech", "speech_to_text"]:
                (
                    inputs,
                    position_ids,
                    attention_mask,
                    _,
                    inputs_embeds,
                    _,
                    fake_inputs_embeds,
                    bottom_audio_labels,
                    inputs_embeds_proj,
                ) = self.prepare_inputs_labels_for_multimodal_audio(
                    inputs,
                    position_ids,
                    attention_mask,
                    audio_past_key_values,
                    None,
                    images,
                    modalities,
                    image_sizes=image_sizes,
                )
            else:
                inputs, position_ids, attention_mask, _, inputs_embeds, _ = (
                    self.prepare_inputs_labels_for_multimodal(
                        inputs,
                        position_ids,
                        attention_mask,
                        None,
                        None,
                        images,
                        modalities,
                        image_sizes=image_sizes,
                    )
                )
                fake_inputs_embeds = None
                inputs_embeds_proj = None
                bottom_audio_labels = None
        else:
            if inference_type in ["speech_to_speech", "speech_to_text"]:
                inputs_embeds, inputs_embeds_proj, bottom_audio_labels = (
                    self.encode_audio(
                        inputs.clamp(min=0), past_key_values=audio_past_key_values
                    )
                )
            else:
                inputs_embeds = self.get_model().embed_tokens(inputs.clamp(min=0))
                inputs_embeds_proj = None
            fake_inputs_embeds = inputs_embeds

        kwargs["fake_inputs_embeds"] = fake_inputs_embeds
        kwargs["inputs_embeds_proj"] = inputs_embeds_proj
        kwargs["bottom_audio_labels"] = bottom_audio_labels
        kwargs["inference_type"] = inference_type

        return super().generate(
            position_ids=position_ids,
            attention_mask=attention_mask,
            inputs_embeds=inputs_embeds,
            **kwargs,
        )

    def prepare_inputs_for_generation(
        self, input_ids, past_key_values=None, inputs_embeds=None, **kwargs
    ):
        images = kwargs.pop("images", None)
        image_sizes = kwargs.pop("image_sizes", None)
        audio_past_key_values = kwargs.pop("audio_past_key_values", None)
        top_audio_past_key_values = kwargs.pop("top_audio_past_key_values", None)
        fake_inputs_embeds = kwargs.pop("fake_inputs_embeds", None)
        inputs_embeds_proj = kwargs.pop("inputs_embeds_proj", None)
        bottom_audio_labels = kwargs.pop("bottom_audio_labels", None)
        inference_type = kwargs.pop("inference_type", None)
        prefill_audio_rep = kwargs.pop("prefill_audio_rep", None)

        inputs = super().prepare_inputs_for_generation(
            input_ids,
            past_key_values=past_key_values,
            inputs_embeds=inputs_embeds,
            fake_inputs_embeds=fake_inputs_embeds,
            **kwargs,
        )
        if images is not None:
            inputs["images"] = images
        if image_sizes is not None:
            inputs["image_sizes"] = image_sizes
        if audio_past_key_values is not None:
            inputs["audio_past_key_values"] = audio_past_key_values
        if top_audio_past_key_values is not None:
            inputs["top_audio_past_key_values"] = top_audio_past_key_values
        if fake_inputs_embeds is not None:
            inputs["fake_inputs_embeds"] = fake_inputs_embeds
        if bottom_audio_labels is not None:
            inputs["bottom_audio_labels"] = bottom_audio_labels
        if inference_type is not None:
            inputs["inference_type"] = inference_type
        if prefill_audio_rep is not None:
            inputs["prefill_audio_rep"] = prefill_audio_rep
        if inputs_embeds_proj is not None:
            inputs["inputs_embeds_proj"] = inputs_embeds_proj
        return inputs


AutoConfig.register("stream_omni_llama", StreamOmniConfig)
AutoModelForCausalLM.register(StreamOmniConfig, StreamOmniLlamaForCausalLM)
