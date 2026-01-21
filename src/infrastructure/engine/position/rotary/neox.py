from typing import Tuple, Any
from .base import HAS_TORCH, HAS_NUMPY, RotaryEmbeddingBase
from .config import RoPEConfig

if HAS_TORCH:
    import torch
if HAS_NUMPY:
    import numpy as np

class NeoxRotaryEmbedding(RotaryEmbeddingBase):
    """NeoX style rotary position embedding.

    Rotates pairs of dimensions (0, d/2), (1, d/2+1), etc.
    This is the standard implementation used in Llama, Mistral, and others.
    """

    def __init__(self, config: RoPEConfig):
        super().__init__(config)
        self.inv_freq = self._compute_inv_freq()

    def _compute_inv_freq(self) -> Any:
        """Compute inverse frequencies."""
        if HAS_TORCH:
            return 1.0 / (
                self.base ** (
                    torch.arange(0, self.rotary_dim, 2, dtype=torch.float32)
                    / self.rotary_dim
                )
            )
        elif HAS_NUMPY:
            return 1.0 / (
                self.base ** (
                    np.arange(0, self.rotary_dim, 2, axis=0) / self.rotary_dim
                )
            )
        raise RuntimeError("No numerical backend available")

    def _compute_cos_sin_cache(self, max_len: int) -> Tuple[Any, Any]:
        """Compute cos/sin cache."""
        if HAS_TORCH:
            t = torch.arange(max_len, dtype=torch.float32)
            freqs = torch.outer(t, self.inv_freq)
            # NeoX style expects [cos, cos] and [sin, sin] for symmetry
            emb = torch.cat((freqs, freqs), dim=-1)
            return torch.cos(emb), torch.sin(emb)
        elif HAS_NUMPY:
            t = np.arange(max_len, dtype=np.float32)
            freqs = np.outer(t, self.inv_freq)
            emb = np.concatenate((freqs, freqs), axis=-1)
            return np.cos(emb), np.sin(emb)
        raise RuntimeError("No numerical backend available")

    def forward_native(
        self,
        positions: Any,
        query: Any,
        key: Any,
    ) -> Tuple[Any, Any]:
        """Apply NeoX style rotary embeddings."""
        if HAS_TORCH and isinstance(positions, torch.Tensor):
            return self._forward_torch(positions, query, key)
        elif HAS_NUMPY:
            return self._forward_numpy(positions, query, key)
        else:
            raise RuntimeError("No numerical backend available")

    def _forward_torch(
        self,
        positions: "torch.Tensor",
        query: "torch.Tensor",
        key: "torch.Tensor",
    ) -> Tuple["torch.Tensor", "torch.Tensor"]:
        """PyTorch implementation of NeoX RoPE."""
        seq_len = int(positions.max().item()) + 1
        self._ensure_cache(seq_len)

        # Get cos/sin for positions
        cos = self._cos_cache[positions]  # [batch, seq, rotary_dim//2]
        sin = self._sin_cache[positions]

        # Apply rotation to query and key
        def rotate_half(x: "torch.Tensor") -> "torch.Tensor":
            x1 = x[..., : x.shape[-1] // 2]
            x2 = x[..., x.shape[-1] // 2 :]
            return torch.cat((-x2, x1), dim=-1)

        # Apply to query
        q_rotary = query[..., :self.rotary_dim]
        q_pass = query[..., self.rotary_dim:]

        cos_q = cos.unsqueeze(-2)  # Add head dimension
        sin_q = sin.unsqueeze(-2)

        q_rotated = q_rotary * cos_q + rotate_half(q_rotary) * sin_q
        query_out = torch.cat([q_rotated, q_pass], dim=-1) if q_pass.numel() > 0 else q_rotated

        # Apply to key
        k_rotary = key[..., :self.rotary_dim]
        k_pass = key[..., self.rotary_dim:]

        k_rotated = k_rotary * cos_q + rotate_half(k_rotary) * sin_q
        key_out = torch.cat([k_rotated, k_pass], dim=-1) if k_pass.numel() > 0 else k_rotated

        return query_out, key_out

    def _forward_numpy(
        self,
        positions: "np.ndarray",
        query: "np.ndarray",
        key: "np.ndarray",
    ) -> Tuple["np.ndarray", "np.ndarray"]:
        """NumPy implementation of NeoX RoPE."""
        seq_len = int(positions.max()) + 1
        self._ensure_cache(seq_len)

        cos = self._cos_cache[positions]
        sin = self._sin_cache[positions]

        def rotate_half(x: "np.ndarray") -> "np.ndarray":
            x1 = x[..., : x.shape[-1] // 2]
            x2 = x[..., x.shape[-1] // 2 :]
            return np.concatenate((-x2, x1), axis=-1)

        q_rotary = query[..., :self.rotary_dim]
        cos_q = np.expand_dims(cos, axis=-2)
        sin_q = np.expand_dims(sin, axis=-2)

        q_rotated = q_rotary * cos_q + rotate_half(q_rotary) * sin_q
        k_rotary = key[..., :self.rotary_dim]
        k_rotated = k_rotary * cos_q + rotate_half(k_rotary) * sin_q

        return q_rotated, k_rotated
