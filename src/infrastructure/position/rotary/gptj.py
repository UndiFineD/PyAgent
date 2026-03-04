from typing import Tuple, Any, TYPE_CHECKING
from .base import HAS_TORCH, HAS_NUMPY, RotaryEmbeddingBase
from .config import RoPEConfig

if HAS_TORCH:
    import torch
else:
    torch = None

if HAS_NUMPY:
    import numpy as np
else:
    np = None

if TYPE_CHECKING:
    import torch as torch_type

class GptJRotaryEmbedding(RotaryEmbeddingBase):
    """GPT-J style rotary position embedding.
    
    Interleaved rotation pattern where pairs of dimensions
    are rotated together.
    """


    def __init__(self, config: RoPEConfig):
        config.is_neox_style = False
        super().__init__(config)
        self.inv_freq = self._compute_inv_freq()


    def _compute_inv_freq(self) -> Any:
        """Compute inverse frequencies."""
        if HAS_TORCH and torch is not None:
            return 1.0 / (
                self.base ** (
                    torch.arange(0, self.rotary_dim, 2, dtype=torch.float32)
                    / self.rotary_dim
                )
            )
        elif HAS_NUMPY and np is not None:
            return 1.0 / (
                self.base ** (
                    np.arange(0, self.rotary_dim, 2, dtype=np.float32)
                    / self.rotary_dim
                )
            )
        raise RuntimeError("No numerical backend available")


    def _compute_cos_sin_cache(self, max_len: int) -> Tuple[Any, Any]:
        """Compute cos/sin cache."""
        if HAS_TORCH and torch is not None:
            t = torch.arange(max_len, dtype=torch.float32)
            freqs = torch.outer(t, self.inv_freq)
            # Interleaved pattern: [cos0, cos0, cos1, cos1, ...]
            cos_cache = torch.cos(freqs).repeat_interleave(2, dim=-1)
            sin_cache = torch.sin(freqs).repeat_interleave(2, dim=-1)
            return cos_cache, sin_cache
        elif HAS_NUMPY and np is not None:
            t = np.arange(max_len, dtype=np.float32)
            freqs = np.outer(t, self.inv_freq)
            cos_cache = np.repeat(np.cos(freqs), 2, axis=-1)
            sin_cache = np.repeat(np.sin(freqs), 2, axis=-1)
            return cos_cache, sin_cache
        raise RuntimeError("No numerical backend available")


    def forward_native(
        self,
        positions: Any,
        query: Any,
        key: Any,
    ) -> Tuple[Any, Any]:
        """Apply GPT-J style rotary embeddings."""
        seq_len = int(positions.max()) + 1 if HAS_NUMPY else positions.max().item() + 1

        if self._cache_seq_len < seq_len:
            self._cos_cache, self._sin_cache = self._compute_cos_sin_cache(
                max(seq_len, 2048)
            )
            self._cache_seq_len = max(seq_len, 2048)

        if HAS_TORCH and torch is not None and isinstance(positions, torch.Tensor):
            if self._cos_cache is None or self._sin_cache is None:
                raise RuntimeError("Cosine/sine cache not initialized")
            cos = self._cos_cache[positions].unsqueeze(-2)
            sin = self._sin_cache[positions].unsqueeze(-2)

            def rotate_interleaved(x: Any) -> Any:
                x1 = x[..., ::2]
                x2 = x[..., 1::2]
                if torch is None:
                    raise RuntimeError("PyTorch is not available")
                rotated = torch.stack((-x2, x1), dim=-1).flatten(-2)
                return rotated

            q_rotated = query * cos + rotate_interleaved(query) * sin
            k_rotated = key * cos + rotate_interleaved(key) * sin
            return q_rotated, k_rotated

        raise RuntimeError("GPT-J RoPE requires PyTorch")
