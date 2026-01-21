from __future__ import annotations
import numpy as np
from typing import TYPE_CHECKING
from .base import Quantizer
from .linear import LinearQuantizer
from .tensor import QuantizedTensor
from .config import QuantConfig

if TYPE_CHECKING:
    from numpy.typing import NDArray

class GPTQQuantizer(Quantizer):
    """GPTQ Quantization using Hessian-based optimal rounding."""

    def __init__(
        self,
        config: QuantConfig,
        damp_percent: float = 0.01,
        block_size: int = 128,
    ):
        super().__init__(config)
        self.damp_percent = damp_percent
        self.block_size = block_size

    def quantize(
        self,
        weight: NDArray[np.float32],
        hessian: NDArray[np.float32] | None = None,
    ) -> QuantizedTensor:
        from .utils import pack_int4
        out_features, in_features = weight.shape

        if hessian is None:
            linear_quant = LinearQuantizer(self.config)
            return linear_quant.quantize(weight)

        diag_mean = np.mean(np.diag(hessian))
        hessian_damp = hessian + self.damp_percent * diag_mean * np.eye(in_features)

        try:
            hessian_inv = np.linalg.inv(hessian_damp)
        except np.linalg.LinAlgError:
            linear_quant = LinearQuantizer(self.config)
            return linear_quant.quantize(weight)

        qweight = self._gptq_quantize(weight, hessian_inv)

        linear_quant = LinearQuantizer(self.config)
        scale, zp = linear_quant._compute_group_params(weight)

        if self.config.bits == 4:
            qweight = pack_int4(qweight)

        return QuantizedTensor(
            data=qweight,
            scale=scale,
            zero_point=zp,
            shape=weight.shape,
            config=self.config,
        )

    def dequantize(
        self,
        qtensor: QuantizedTensor,
    ) -> NDArray[np.float32]:
        return qtensor.dequantize()

    def _gptq_quantize(
        self,
        weight: NDArray[np.float32],
        hessian_inv: NDArray[np.float32],
    ) -> NDArray[np.int8]:
        out_features, in_features = weight.shape
        qweight = np.zeros_like(weight, dtype=np.int8)
        w = weight.copy()

        for block_start in range(0, in_features, self.block_size):
            block_end = min(block_start + self.block_size, in_features)

            for col in range(block_start, block_end):
                group_idx = col // self.config.group_size
                group_start = group_idx * self.config.group_size
                group_end = min(group_start + self.config.group_size, in_features)

                group = w[:, group_start:group_end]
                if self.config.symmetric:
                    max_val = np.max(np.abs(group), axis=1)
                    scale = np.where(max_val > 0, max_val / self.config.qmax, 1.0)
                else:
                    min_val = np.min(group, axis=1)
                    max_val = np.max(group, axis=1)
                    scale = (max_val - min_val) / (self.config.qmax - self.config.qmin)
                    scale = np.maximum(scale, 1e-8)

                col_data = w[:, col]
                q = np.round(col_data / scale).astype(np.int8)
                q = np.clip(q, self.config.qmin, self.config.qmax)
                qweight[:, col] = q

                dequant = q.astype(np.float32) * scale
                error = col_data - dequant

                for j in range(col + 1, block_end):
                    h_ratio = hessian_inv[col, j] / (hessian_inv[col, col] + 1e-8)
                    w[:, j] += error * h_ratio

        return qweight
