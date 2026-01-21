from __future__ import annotations
import numpy as np
from typing import TYPE_CHECKING, Optional
from .tensor import QuantizedTensor

if TYPE_CHECKING:
    from numpy.typing import NDArray

class DequantizedLinear:
    """Dequantized linear layer for inference."""

    def __init__(
        self,
        qweight: QuantizedTensor,
        bias: NDArray[np.float32] | None = None,
    ):
        self.qweight = qweight
        self.bias = bias
        self._dequant_cache: NDArray[np.float32] | None = None

    def forward(
        self,
        x: NDArray[np.float32],
        use_cache: bool = True,
    ) -> NDArray[np.float32]:
        if use_cache and self._dequant_cache is not None:
            weight = self._dequant_cache
        else:
            weight = self.qweight.dequantize()
            if use_cache:
                self._dequant_cache = weight

        output = x @ weight.T

        if self.bias is not None:
            output = output + self.bias

        return output

    def clear_cache(self):
        self._dequant_cache = None

    @property
    def in_features(self) -> int:
        return self.qweight.shape[1] if len(self.qweight.shape) >= 2 else self.qweight.shape[0]

    @property
    def out_features(self) -> int:
        return self.qweight.shape[0]
