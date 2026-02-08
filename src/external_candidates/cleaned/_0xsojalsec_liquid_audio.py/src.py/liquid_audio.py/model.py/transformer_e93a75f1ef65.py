# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-liquid-audio\src\liquid_audio\model\transformer.py
import math
from abc import ABC, abstractmethod
from collections.abc import Iterable, Sequence
from functools import partial
from typing import Any, Literal, TypeGuard, cast

import torch
import torch.nn.functional as F
from einops import rearrange
from torch import nn
from torch.nn.attention.bias import causal_lower_right

type CacheType = torch.Tensor | None | Sequence["CacheType"]


class SequenceModel(nn.Module, ABC):
    """Models operating on sequences

    Assumptions:
        input shape [N, T, dim]
        output shape [N, T', dim_out]
    """

    dim: int
    dim_out: int

    @abstractmethod
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__()

    @abstractmethod
    def forward(self, x: torch.Tensor, cache: CacheType = None) -> torch.Tensor: ...

    @abstractmethod
    def forward_cached(self, x: torch.Tensor, cache: CacheType = None) -> tuple[torch.Tensor, CacheType]: ...


class LayerKVCache:
    """
    Assumes input cache is a tuple of two tensors (key, value)
    """

    def __init__(self, cache: tuple[torch.Tensor, torch.Tensor] | None = None) -> None:
        assert cache is None or len(cache) == 2
        self.key_cache = cache[0] if cache is not None else None
        self.value_cache = cache[1] if cache is not None else None

    def update(self, k: torch.Tensor, v: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        if self.key_cache is None or self.value_cache is None:
            # initialize
            self.key_cache = k
            self.value_cache = v
        else:
            self.key_cache = torch.cat([self.key_cache, k], dim=1)
            self.value_cache = torch.cat([self.value_cache, v], dim=1)
        return self.key_cache, self.value_cache

    def get_cache_size(self) -> int:
        if self.key_cache is None:
            return 0
        else:
            return self.key_cache.shape[1]


class RMSNorm(SequenceModel):
    def __init__(self, dim: int, eps: float = 1e-6) -> None:
        super().__init__()
        self.eps = eps
        self.weight = nn.Parameter(torch.ones(dim))

    def _norm(self, x: torch.Tensor) -> torch.Tensor:
        return x * torch.rsqrt(x.pow(2).mean(-1, keepdim=True) + self.eps)

    def forward(self, x: torch.Tensor, cache: CacheType = None) -> torch.Tensor:
        assert cache is None, "RMSNorm expects None cache"

        output = self._norm(x.float())
        return (output * self.weight).type_as(x)

    def forward_cached(self, x: torch.Tensor, cache: CacheType = None) -> tuple[torch.Tensor, CacheType]:
        return self(x, cache), None


class GLU(SequenceModel):
    def __init__(
        self,
        dim: int,
        ff_dim: int | None = None,
        mlp_init_scale: float = 1.0,
        out_init_scale: float = 0.14434,
        use_swiglu: bool = True,
        multiple_of: int = 256,
        ffn_dim_multiplier: float = 1.0,
    ):
        super().__init__()
        # linear_cls = FlexLinear
        self.dim = dim
        self.dim_out = dim
        self.use_swiglu = use_swiglu
        self.num_params = 0
        if ff_dim is None:  # from LFMv1Block
            ff_dim = 4 * dim
        if use_swiglu:
            ff_dim = int(2 * ff_dim / 3)
            # custom dim factor multiplier
            if ffn_dim_multiplier is not None:
                ff_dim = int(ffn_dim_multiplier * ff_dim)
            ff_dim = multiple_of * ((ff_dim + multiple_of - 1) // multiple_of)

        self.w1 = nn.Linear(dim, ff_dim, bias=False)

        self.num_params += dim * ff_dim
        std = mlp_init_scale / math.sqrt(dim)
        torch.nn.init.normal_(self.w1.weight, mean=0.0, std=std)

        if use_swiglu:
            self.w3 = nn.Linear(dim, ff_dim, bias=False)

            self.num_params += dim * ff_dim
            std = mlp_init_scale / math.sqrt(dim)
            torch.nn.init.normal_(self.w3.weight, mean=0.0, std=std)

        self.w2 = nn.Linear(ff_dim, dim, bias=False)

        self.num_params += ff_dim * dim
        std = out_init_scale * mlp_init_scale / math.sqrt(ff_dim)
        torch.nn.init.normal_(self.w2.weight, mean=0.0, std=std)

    def forward(self, x: torch.Tensor, cache: CacheType = None) -> torch.Tensor:
        assert cache is None, "expected None cache for GLU"
        if self.use_swiglu:
            return cast(torch.Tensor, self.w2(F.silu(self.w1(x)) * self.w3(x)))
        else:
            return cast(torch.Tensor, self.w2(F.gelu(self.w1(x))))

    def forward_cached(self, x: torch.Tensor, cache: CacheType = None) -> tuple[torch.Tensor, CacheType]:
        return self(x, cache), None


class BoundedAttention(nn.Module):
    def __init__(
        self,
        dim: int,
        num_heads: int = 32,
        head_style: Literal["mha", "gqa", "mqa"] = "mha",
        gqa_dim: int | None = None,
        qk_layernorm: bool = False,
        norm_eps: float = 1e-5,
    ) -> None:
        super().__init__()
        assert dim % num_heads == 0

        self.num_heads = num_heads
        self.head_dim = dim // num_heads

        self.head_style = head_style

        if self.head_style == "gqa":
            # only access attribute if using gqa head style
            assert gqa_dim is not None
            self.gqa_dim = gqa_dim
            assert self.num_heads % self.gqa_dim == 0, f"{self.gqa_dim} % {self.head_dim} != 0"

        self.qk_layernorm = qk_layernorm

        if self.qk_layernorm:
            self.q_layernorm = RMSNorm(self.head_dim, eps=norm_eps)

            self.k_layernorm = RMSNorm(self.head_dim, eps=norm_eps)

    def forward(
        self,
        q: torch.Tensor,
        k: torch.Tensor,
        v: torch.Tensor,
        freqs_cis: torch.Tensor | None = None,
        cache: LayerKVCache | None = None,
    ) -> tuple[torch.Tensor, tuple[torch.Tensor, torch.Tensor]]:
        bsz, seqlen = q.shape[0], q.shape[1]

        if self.head_style == "mqa":
            q = q.reshape(bsz, seqlen, self.num_heads, self.head_dim)
            k = k.reshape(bsz, seqlen, 1, self.head_dim)
            v = v.reshape(bsz, seqlen, 1, self.head_dim)
        elif self.head_style == "mha":
            q = q.reshape(bsz, seqlen, self.num_heads, self.head_dim)
            k = k.reshape(bsz, seqlen, self.num_heads, self.head_dim)
            v = v.reshape(bsz, seqlen, self.num_heads, self.head_dim)
        elif self.head_style == "gqa":
            q = q.reshape(bsz, seqlen, self.num_heads, self.head_dim)
            k = k.reshape(bsz, seqlen, self.gqa_dim, self.head_dim)
            v = v.reshape(bsz, seqlen, self.gqa_dim, self.head_dim)

        if self.qk_layernorm:
            q = self.q_layernorm(q)
            k = self.k_layernorm(k)

        if freqs_cis is not None:
            q, k = apply_rotary_emb(q, k, freqs_cis=freqs_cis)

        if cache is not None:
            k, v = cache.update(k, v)

        q_len = q.shape[1]
        kv_len = k.shape[1]

        query = q.transpose(1, 2)
        key = k.transpose(1, 2)
        value = v.transpose(1, 2)

        enable_gqa = self.head_style in ("mqa", "gqa")
        if q_len == kv_len:
            output = nn.functional.scaled_dot_product_attention(
                query, key, value, is_causal=True, enable_gqa=enable_gqa
            )
        else:
            if q_len == 1:
                attn_mask = None
            else:
                attn_mask = causal_lower_right(q_len, kv_len)
            output = nn.functional.scaled_dot_product_attention(
                query,
                key,
                value,
                is_causal=False,
                enable_gqa=enable_gqa,
                attn_mask=attn_mask,
            )

        output = output.transpose(1, 2)

        output = output.reshape(bsz, seqlen, self.num_heads * self.head_dim)
        return output, (k, v)


class MHA(SequenceModel):
    def __init__(
        self,
        dim: int,
        num_heads: int = 32,
        head_style: Literal["mha", "gqa", "mqa"] = "gqa",
        out_init_scale: float = 0.125,  # 1/sqrt(2*n_layers) (from  gpt3)
        proj_init_scale: float = 1.0,
        qk_layernorm: bool = True,
        norm_eps: float = 0.00001,
        gqa_dim: int = 8,  # Optional if head_style is not "gqa"
        freqs_cis: torch.Tensor | None = None,
        max_seq_len: int = 128_000,  # Stored positional encodings. Optional if freqs_cis is given
        theta: float = 1_000_000.0,  # Positional encoding theta. Optional if freqs_cis is given
    ):
        super().__init__()

        self.dim = self.dim_out = dim
        self.num_heads = num_heads
        assert self.dim % self.num_heads == 0, "expected dim to be divisible by num_heads"
        self.head_dim = self.dim // self.num_heads
        self.head_style = head_style

        if self.head_style == "gqa":
            # only access attribute if using gqa head style
            assert gqa_dim is not None
            self.gqa_dim = gqa_dim

        # q, k, v + optional w and z projections
        if self.head_style == "mha":
            self.total_width = 3 * self.dim
        elif self.head_style == "mqa":
            self.total_width = self.dim + 2 * self.head_dim
        elif self.head_style == "gqa":
            assert self.gqa_dim is not None
            self.total_width = self.dim + 2 * self.head_dim * self.gqa_dim
        else:
            raise NotImplementedError(f"head style {self.head_style} not implemented")

        self.qkv_proj = nn.Linear(
            self.dim,
            self.total_width,
            bias=False,
        )
        std = proj_init_scale / math.sqrt(self.dim)
        torch.nn.init.normal_(self.qkv_proj.weight, mean=0.0, std=std)

        self.out_proj = nn.Linear(self.dim, self.dim, bias=False)

        std = out_init_scale * proj_init_scale / math.sqrt(self.dim)
        torch.nn.init.normal_(self.out_proj.weight, mean=0.0, std=std)

        self.bounded_attention = BoundedAttention(
            dim=dim,
            num_heads=num_heads,
            head_style=head_style,
            gqa_dim=gqa_dim,
            qk_layernorm=qk_layernorm,
            norm_eps=norm_eps,
        )

        if freqs_cis is not None:
            self.freqs_cis = freqs_cis
        else:
            self.freqs_cis = precompute_freqs_cis(self.head_dim, max_seq_len, theta)

    def _validate_cache(self, cache: CacheType) -> TypeGuard[tuple[torch.Tensor, torch.Tensor]]:
        return (
            isinstance(cache, tuple)
            and len(cache) == 2
            and isinstance(cache[0], torch.Tensor)
            and isinstance(cache[1], torch.Tensor)
        )

    def forward(self, x: torch.Tensor, cache: CacheType = None) -> torch.Tensor:
        return self.forward_cached(x, cache)[0]

    def forward_cached(self, x: torch.Tensor, cache: CacheType = None) -> tuple[torch.Tensor, CacheType]:
        if cache is not None:
            assert self._validate_cache(cache)
            kv_cache = LayerKVCache(cache)
        else:
            kv_cache = None

        # x is (bsz, seqlen, d_model)
        seq_len = x.shape[1]

        x = self.qkv_proj(x)
        if self.head_style == "mha":
            xq, xk, xv = x.split(self.dim, dim=-1)
        elif self.head_style == "mqa":
            xq, xk, xv = x.split([self.dim, self.head_dim, self.head_dim], dim=-1)
        elif self.head_style == "gqa":
            xq, xk, xv = x.split(
                [self.dim, self.head_dim * self.gqa_dim, self.head_dim * self.gqa_dim],
                dim=-1,
            )

        # TODO: Need to clean up, hack for now to allow rpes in grafted model if using e.g. mqa for grafting
        self.freqs_cis = self.freqs_cis.to(xq.device)
        if kv_cache is not None:
            # If using cache, get freqs for all new tokens starting from cache size
            cache_size = kv_cache.get_cache_size()
            freqs_cis = self.freqs_cis[cache_size : cache_size + seq_len]
        else:
            # Otherwise get freqs for full sequence
            freqs_cis = self.freqs_cis[:seq_len]

        ys, new_cache = self.bounded_attention(xq, xk, xv, freqs_cis=freqs_cis, cache=kv_cache)

        ys = self.out_proj(ys)

        return cast(torch.Tensor, ys), new_cache


class StandardBlock(SequenceModel):
    """Block with an operator + norm + skip connection, followed by a GLU + norm + skip connection"""

    def __init__(
        self,
        operator: SequenceModel,
        ff_dim: int | None = None,
        mlp_init_scale: float = 1.0,
        out_init_scale: float = 0.125,  # 1/sqrt(2*n_layers) (from gpt3)
        use_swiglu: bool = True,
        multiple_of: int = 256,
        ffn_dim_multiplier: float = 1.0,
        norm_eps: float = 0.00001,
    ):
        super().__init__()
        self.operator = operator
        self.dim = self.dim_out = self.operator.dim

        if ff_dim is None:
            ff_dim = 4 * self.dim

        self.feed_forward = GLU(
            dim=self.dim,
            ff_dim=ff_dim,
            mlp_init_scale=mlp_init_scale,
            out_init_scale=out_init_scale,
            use_swiglu=use_swiglu,
            multiple_of=multiple_of,
            ffn_dim_multiplier=ffn_dim_multiplier,
        )

        self.operator_norm = RMSNorm(self.dim, eps=norm_eps)
        self.ffn_norm = RMSNorm(self.dim, eps=norm_eps)

    def forward(self, x: torch.Tensor, cache: CacheType = None) -> torch.Tensor:
        h = self.operator(self.operator_norm(x), cache)
        h += x
        h_glu = self.feed_forward(self.ffn_norm(h))
        out = h + h_glu
        return cast(torch.Tensor, out)

    def forward_cached(self, x: torch.Tensor, cache: CacheType | None = None) -> tuple[torch.Tensor, CacheType]:
        h, new_cache = self.operator.forward_cached(self.operator_norm(x), cache)
        h += x
        h_glu = self.feed_forward.forward(self.ffn_norm(h))
        out = h + h_glu
        return out, new_cache


def apply_rotary_emb(
    xq: torch.Tensor,
    xk: torch.Tensor,
    freqs_cis: torch.Tensor,
) -> tuple[torch.Tensor, torch.Tensor]:
    """
    Apply rotary embeddings to input tensors using the given frequency tensor.

    This function applies rotary embeddings to the given query 'xq' and key 'xk' tensors using the provided
    frequency tensor 'freqs_cis'. The input tensors are reshaped as complex numbers, and the frequency tensor
    is reshaped for broadcasting compatibility. The resulting tensors contain rotary embeddings and are
    returned as real tensors.

    Args:
        xq (torch.Tensor): Query tensor to apply rotary embeddings.
        xk (torch.Tensor): Key tensor to apply rotary embeddings.
        freqs_cis (torch.Tensor): Precomputed frequency tensor for complex exponentials.

    Returns:
        Tuple[torch.Tensor, torch.Tensor]: Tuple of modified query tensor and key tensor with rotary embeddings.



    """
    xq_ = torch.view_as_complex(rearrange(xq.float(), "... (D two) -> ... D two", two=2))
    xk_ = torch.view_as_complex(rearrange(xk.float(), "... (D two) -> ... D two", two=2))
    freqs_cis = reshape_for_broadcast(freqs_cis, xq_)
    xq_out = torch.view_as_real(xq_ * freqs_cis).flatten(3)
    xk_out = torch.view_as_real(xk_ * freqs_cis).flatten(3)
    return xq_out.type_as(xq), xk_out.type_as(xk)


def reshape_for_broadcast(freqs_cis: torch.Tensor, x: torch.Tensor) -> torch.Tensor:
    """
    Reshape frequency tensor for broadcasting it with another tensor.

    This function reshapes the frequency tensor to have the same shape as the target tensor 'x'
    for the purpose of broadcasting the frequency tensor during element-wise operations.

    Args:
        freqs_cis (torch.Tensor): Frequency tensor to be reshaped.
        x (torch.Tensor): Target tensor for broadcasting compatibility.

    Returns:
        torch.Tensor: Reshaped frequency tensor.

    Raises:
        AssertionError: If the frequency tensor doesn't match the expected shape.
        AssertionError: If the target tensor 'x' doesn't have the expected number of dimensions.
    """
    ndim = x.ndim
    assert 0 <= 1 < ndim
    assert freqs_cis.shape == (x.shape[1], x.shape[-1])
    shape = [d if i == 1 or i == ndim - 1 else 1 for i, d in enumerate(x.shape)]
    return freqs_cis.view(*shape)


def precompute_freqs_cis(dim: int, end: int, theta: float = 10000.0) -> torch.Tensor:
    """
    Precompute the frequency tensor for complex exponentials (cis) with given dimensions.

    This function calculates a frequency tensor with complex exponentials using the given dimension 'dim'
    and the end index 'end'. The 'theta' parameter scales the frequencies.
    The returned tensor contains complex values in complex64 data type.

    Args:
        dim (int): Dimension of the frequency tensor.
        end (int): End index for precomputing frequencies.
        theta (float, optional): Scaling factor for frequency computation. Defaults to 10000.0.

    Returns:
        torch.Tensor: Precomputed frequency tensor with complex exponentials.
    """
    freqs = 1.0 / (theta ** (torch.arange(0, dim, 2)[: (dim // 2)].float() / dim))
    t = torch.arange(end, device=freqs.device)
    freqs = torch.outer(t, freqs).float()
    freqs_cis = torch.polar(torch.ones_like(freqs), freqs)  # complex64
    return freqs_cis


class SharedEmbedding(nn.Module):
    def __init__(
        self,
        dim: int,
        vocab_size: int = 65_536,
        embed_init_scale: float = 1.0,
        norm_eps: float = 0.00001,
        *,
        tie_embedding: bool = True,
    ) -> None:
        super().__init__()

        self.embedding = torch.nn.Embedding(vocab_size, dim)

        std = embed_init_scale / math.sqrt(dim)
        torch.nn.init.normal_(self.embedding.weight, mean=0.0, std=std)

        self.embedding_norm = RMSNorm(dim, eps=norm_eps)  # Note: this is really the norm before output projection
        self.to_logits = nn.Linear(dim, vocab_size, bias=False)

        if tie_embedding:
            self.to_logits.weight = self.embedding.weight
        else:
            # If not tying embedding, scale the output weights
            std = embed_init_scale / math.sqrt(dim)
            torch.nn.init.normal_(self.to_logits.weight, mean=0.0, std=std)

    def forward(self, tokens: torch.Tensor) -> torch.Tensor:
        return self.embed(tokens)

    def embed(self, tokens: torch.Tensor) -> torch.Tensor:
        return cast(torch.Tensor, self.embedding(tokens))

    def get_logits(self, embeddings: torch.Tensor) -> torch.Tensor:
        return cast(torch.Tensor, self.to_logits(self.embedding_norm(embeddings)))


class RawLMBackbone(SequenceModel):
    """
    "Raw" Backbone for LM models:
    - input: continuous embeddings
    - output: continuous embeddings
    """

    def __init__(
        self,
        layers: Iterable[SequenceModel],
        vocab_size: int = 65_536,
        norm_eps: float = 0.00001,
        embed_init_scale: float = 1.0,
        *,
        has_embedding: bool = True,
        tie_embedding: bool = True,
    ) -> None:
        super().__init__()

        self.layers = cast(Sequence[SequenceModel], nn.ModuleList(layers))
        self.dim = self.layers[0].dim
        self.dim_out = self.layers[-1].dim_out
        assert self.dim == self.dim_out, "expected first layer input dim to be equal to last layer's output dim"

        if has_embedding:
            # TODO: possibly wrap in wrap_sharded
            self.embedding = SharedEmbedding(
                self.dim,
                vocab_size,
                embed_init_scale=embed_init_scale,
                norm_eps=norm_eps,
                tie_embedding=tie_embedding,
            )
        self.has_embedding = has_embedding
        self.vocab_size = vocab_size

    def forward(self, x: torch.Tensor, cache: CacheType | None = None) -> torch.Tensor:
        if cache is not None:
            assert isinstance(cache, list)
            assert len(cache) == len(self.layers)
        else:
            cache = [None] * len(self.layers)

        for layer, layer_cache in zip(self.layers, cache, strict=True):
            x = layer(x, layer_cache)

        return x

    def forward_cached(self, x: torch.Tensor, cache: CacheType | None = None) -> tuple[torch.Tensor, CacheType]:
        if cache is not None:
            assert isinstance(cache, list)
            assert len(cache) == len(self.layers)
        else:
            cache = [None] * len(self.layers)

        cache_out: list[CacheType] = []
        for layer, layer_cache in zip(self.layers, cache, strict=True):
            x, new_cache = layer.forward_cached(x, layer_cache)
            cache_out.append(new_cache)

        return x, cache_out


def wrap_activation_checkpoint[T: nn.Module](mod: T) -> T:
    # NOTE: we're using torch.utils.checkpoint.checkpoint here to avoid the error in backward pass when using zero-3 + activation checkpointing (https://github.com/microsoft/DeepSpeed/issues/4595)
    checkpoint_fn = partial(torch.utils.checkpoint.checkpoint, use_reentrant=False)
    mod.forward_ = mod.forward  # type: ignore[assignment]

    def forward(*args, **kwargs):
        return checkpoint_fn(mod.forward_, *args, **kwargs)

    mod.forward = forward
    return mod
