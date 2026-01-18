"""
Quantization Engine - Weight compression framework for LLM inference.

Inspired by vLLM's quantization layers (AWQ, GPTQ, INT8, FP8) for
memory-efficient model deployment.

Phase 27: Attention, Quantization & LoRA Patterns
"""

from __future__ import annotations

import math
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING, Any, Callable, Protocol

import numpy as np

if TYPE_CHECKING:
    from numpy.typing import NDArray


class QuantScheme(Enum):
    """Quantization scheme types."""
    INT4 = "int4"
    INT8 = "int8"
    FP8 = "fp8"
    NF4 = "nf4"  # NormalFloat4 (QLoRA)
    AWQ = "awq"  # Activation-aware Weight Quantization
    GPTQ = "gptq"  # GPTQ quantization


class QuantStrategy(Enum):
    """Quantization granularity strategy."""
    TENSOR = "tensor"  # Single scale per tensor
    CHANNEL = "channel"  # Per output channel
    GROUP = "group"  # Per group of weights
    BLOCK = "block"  # Block-wise quantization


@dataclass
class QuantConfig:
    """Configuration for quantization.
    
    Attributes:
        bits: Number of bits for quantization (4, 8)
        scheme: Quantization scheme (INT4, INT8, AWQ, GPTQ, etc.)
        strategy: Quantization granularity
        group_size: Size of quantization groups (-1 for per-tensor)
        symmetric: Whether to use symmetric quantization
        zero_point: Whether to use zero-point (asymmetric only)
        desc_act: Whether to use descending activation order (GPTQ)
    """
    bits: int = 8
    scheme: QuantScheme = QuantScheme.INT8
    strategy: QuantStrategy = QuantStrategy.GROUP
    group_size: int = 128
    symmetric: bool = True
    zero_point: bool = False
    desc_act: bool = False
    
    def __post_init__(self):
        self._validate()
    
    def _validate(self):
        """Validate configuration."""
        if self.bits not in (4, 8):
            raise ValueError(f"bits must be 4 or 8, got {self.bits}")
        if self.group_size < -1 or self.group_size == 0:
            raise ValueError(f"group_size must be -1 or positive, got {self.group_size}")
        if self.symmetric and self.zero_point:
            raise ValueError("symmetric quantization cannot have zero_point")
    
    @property
    def pack_factor(self) -> int:
        """Number of quantized values per packed int32."""
        return 32 // self.bits
    
    @property
    def qmin(self) -> int:
        """Minimum quantized value."""
        if self.symmetric:
            return -(1 << (self.bits - 1))
        return 0
    
    @property
    def qmax(self) -> int:
        """Maximum quantized value."""
        if self.symmetric:
            return (1 << (self.bits - 1)) - 1
        return (1 << self.bits) - 1


@dataclass
class QuantizedTensor:
    """Quantized tensor representation.
    
    Attributes:
        data: Quantized values (int8 or packed int32)
        scale: Quantization scales
        zero_point: Zero points (for asymmetric)
        shape: Original tensor shape
        config: Quantization configuration
    """
    data: NDArray[np.int8] | NDArray[np.int32]
    scale: NDArray[np.float32]
    zero_point: NDArray[np.int32] | None
    shape: tuple[int, ...]
    config: QuantConfig
    
    def dequantize(self) -> NDArray[np.float32]:
        """Dequantize to full precision."""
        if self.config.bits == 4:
            # Unpack int4 from int8
            unpacked = unpack_int4(self.data)
        else:
            unpacked = self.data.astype(np.float32)
        
        # Reshape to original shape for dequantization
        unpacked_reshaped = unpacked.reshape(self.shape)
        
        # Handle different scale shapes (per-tensor, per-channel, per-group)
        if self.scale.size == 1:
            # Per-tensor quantization
            if self.zero_point is not None:
                result = (unpacked_reshaped - self.zero_point.item()) * self.scale.item()
            else:
                result = unpacked_reshaped * self.scale.item()
        elif self.scale.ndim == 1 and self.scale.shape[0] == self.shape[0]:
            # Per-channel quantization
            if self.zero_point is not None:
                result = (unpacked_reshaped - self.zero_point[:, None]) * self.scale[:, None]
            else:
                result = unpacked_reshaped * self.scale[:, None]
        elif self.scale.ndim == 2:
            # Per-group quantization [out_features, num_groups]
            out_features = self.shape[0]
            in_features = self.shape[1] if len(self.shape) > 1 else 1
            num_groups = self.scale.shape[1]
            group_size = (in_features + num_groups - 1) // num_groups
            
            result = np.zeros(self.shape, dtype=np.float32)
            flat = unpacked_reshaped.reshape(out_features, -1)
            
            for g in range(num_groups):
                start = g * group_size
                end = min(start + group_size, in_features)
                if self.zero_point is not None:
                    result[:, start:end] = (flat[:, start:end] - self.zero_point[:, g:g+1]) * self.scale[:, g:g+1]
                else:
                    result[:, start:end] = flat[:, start:end] * self.scale[:, g:g+1]
        else:
            # Fallback: try broadcasting
            if self.zero_point is not None:
                result = (unpacked_reshaped - self.zero_point) * self.scale
            else:
                result = unpacked_reshaped * self.scale
        
        return result.reshape(self.shape).astype(np.float32)
    
    @property
    def memory_bytes(self) -> int:
        """Memory usage in bytes."""
        data_bytes = self.data.nbytes
        scale_bytes = self.scale.nbytes
        zp_bytes = self.zero_point.nbytes if self.zero_point is not None else 0
        return data_bytes + scale_bytes + zp_bytes
    
    @property
    def compression_ratio(self) -> float:
        """Compression ratio compared to FP32."""
        original_bytes = np.prod(self.shape) * 4  # FP32
        return original_bytes / self.memory_bytes


class Quantizer(ABC):
    """Base class for quantization algorithms."""
    
    def __init__(self, config: QuantConfig):
        """Initialize quantizer.
        
        Args:
            config: Quantization configuration
        """
        self.config = config
    
    @abstractmethod
    def quantize(
        self,
        weight: NDArray[np.float32],
    ) -> QuantizedTensor:
        """Quantize a weight tensor.
        
        Args:
            weight: Weight tensor to quantize
            
        Returns:
            Quantized tensor
        """
        pass
    
    @abstractmethod
    def dequantize(
        self,
        qtensor: QuantizedTensor,
    ) -> NDArray[np.float32]:
        """Dequantize a tensor.
        
        Args:
            qtensor: Quantized tensor
            
        Returns:
            Dequantized float tensor
        """
        pass


class LinearQuantizer(Quantizer):
    """Linear (uniform) quantization.
    
    Supports per-tensor and per-channel quantization.
    """
    
    def quantize(
        self,
        weight: NDArray[np.float32],
    ) -> QuantizedTensor:
        """Quantize using linear quantization."""
        original_shape = weight.shape
        
        if self.config.strategy == QuantStrategy.TENSOR:
            scale, zp = self._compute_tensor_params(weight)
            qweight = self._quantize_linear(weight, scale, zp)
        elif self.config.strategy == QuantStrategy.CHANNEL:
            scale, zp = self._compute_channel_params(weight)
            qweight = self._quantize_per_channel(weight, scale, zp)
        else:
            scale, zp = self._compute_group_params(weight)
            qweight = self._quantize_per_group(weight, scale, zp)
        
        # Pack if 4-bit
        if self.config.bits == 4:
            qweight = pack_int4(qweight)
        
        return QuantizedTensor(
            data=qweight,
            scale=scale,
            zero_point=zp,
            shape=original_shape,
            config=self.config,
        )
    
    def dequantize(
        self,
        qtensor: QuantizedTensor,
    ) -> NDArray[np.float32]:
        """Dequantize using stored scale and zero point."""
        return qtensor.dequantize()
    
    def _compute_tensor_params(
        self,
        weight: NDArray[np.float32],
    ) -> tuple[NDArray[np.float32], NDArray[np.int32] | None]:
        """Compute per-tensor quantization parameters."""
        if self.config.symmetric:
            max_val = np.max(np.abs(weight))
            scale = max_val / self.config.qmax if max_val > 0 else 1.0
            return np.array([scale], dtype=np.float32), None
        else:
            min_val = np.min(weight)
            max_val = np.max(weight)
            scale = (max_val - min_val) / (self.config.qmax - self.config.qmin)
            scale = max(scale, 1e-8)
            zp = int(round(-min_val / scale)) + self.config.qmin
            zp = np.clip(zp, self.config.qmin, self.config.qmax)
            return np.array([scale], dtype=np.float32), np.array([zp], dtype=np.int32)
    
    def _compute_channel_params(
        self,
        weight: NDArray[np.float32],
    ) -> tuple[NDArray[np.float32], NDArray[np.int32] | None]:
        """Compute per-channel quantization parameters."""
        num_channels = weight.shape[0]
        weight_flat = weight.reshape(num_channels, -1)
        
        if self.config.symmetric:
            max_vals = np.max(np.abs(weight_flat), axis=1)
            scales = np.where(max_vals > 0, max_vals / self.config.qmax, 1.0)
            return scales.astype(np.float32), None
        else:
            min_vals = np.min(weight_flat, axis=1)
            max_vals = np.max(weight_flat, axis=1)
            scales = (max_vals - min_vals) / (self.config.qmax - self.config.qmin)
            scales = np.maximum(scales, 1e-8)
            zps = np.round(-min_vals / scales).astype(np.int32) + self.config.qmin
            zps = np.clip(zps, self.config.qmin, self.config.qmax)
            return scales.astype(np.float32), zps.astype(np.int32)
    
    def _compute_group_params(
        self,
        weight: NDArray[np.float32],
    ) -> tuple[NDArray[np.float32], NDArray[np.int32] | None]:
        """Compute per-group quantization parameters."""
        out_features, in_features = weight.shape[:2] if weight.ndim >= 2 else (weight.shape[0], 1)
        flat = weight.reshape(out_features, -1)
        in_features = flat.shape[1]
        
        num_groups = (in_features + self.config.group_size - 1) // self.config.group_size
        
        scales = []
        zps = [] if not self.config.symmetric else None
        
        for g in range(num_groups):
            start = g * self.config.group_size
            end = min(start + self.config.group_size, in_features)
            group = flat[:, start:end]
            
            if self.config.symmetric:
                max_val = np.max(np.abs(group), axis=1)
                scale = np.where(max_val > 0, max_val / self.config.qmax, 1.0)
                scales.append(scale)
            else:
                min_val = np.min(group, axis=1)
                max_val = np.max(group, axis=1)
                scale = (max_val - min_val) / (self.config.qmax - self.config.qmin)
                scale = np.maximum(scale, 1e-8)
                zp = np.round(-min_val / scale).astype(np.int32) + self.config.qmin
                zp = np.clip(zp, self.config.qmin, self.config.qmax)
                scales.append(scale)
                zps.append(zp)
        
        scales = np.stack(scales, axis=1).astype(np.float32)
        zps = np.stack(zps, axis=1).astype(np.int32) if zps else None
        return scales, zps
    
    def _quantize_linear(
        self,
        weight: NDArray[np.float32],
        scale: NDArray[np.float32],
        zp: NDArray[np.int32] | None,
    ) -> NDArray[np.int8]:
        """Apply linear quantization."""
        scaled = weight / scale[0]
        if zp is not None:
            scaled = scaled + zp[0]
        clipped = np.clip(scaled, self.config.qmin, self.config.qmax)
        return np.round(clipped).astype(np.int8)
    
    def _quantize_per_channel(
        self,
        weight: NDArray[np.float32],
        scale: NDArray[np.float32],
        zp: NDArray[np.int32] | None,
    ) -> NDArray[np.int8]:
        """Apply per-channel quantization."""
        num_channels = weight.shape[0]
        weight_flat = weight.reshape(num_channels, -1)
        
        scaled = weight_flat / scale[:, None]
        if zp is not None:
            scaled = scaled + zp[:, None]
        clipped = np.clip(scaled, self.config.qmin, self.config.qmax)
        return np.round(clipped).reshape(weight.shape).astype(np.int8)
    
    def _quantize_per_group(
        self,
        weight: NDArray[np.float32],
        scale: NDArray[np.float32],
        zp: NDArray[np.int32] | None,
    ) -> NDArray[np.int8]:
        """Apply per-group quantization."""
        original_shape = weight.shape
        out_features = weight.shape[0]
        flat = weight.reshape(out_features, -1)
        in_features = flat.shape[1]
        
        qweight = np.zeros_like(flat, dtype=np.int8)
        
        for g in range(scale.shape[1]):
            start = g * self.config.group_size
            end = min(start + self.config.group_size, in_features)
            group = flat[:, start:end]
            
            scaled = group / scale[:, g:g+1]
            if zp is not None:
                scaled = scaled + zp[:, g:g+1]
            qweight[:, start:end] = np.clip(
                np.round(scaled), self.config.qmin, self.config.qmax
            ).astype(np.int8)
        
        return qweight.reshape(original_shape).astype(np.int8)


class AWQQuantizer(Quantizer):
    """Activation-Aware Weight Quantization (AWQ).
    
    Protects salient weights by computing activation-based importance.
    Reference: https://arxiv.org/abs/2306.00978
    """
    
    def __init__(
        self,
        config: QuantConfig,
        calibration_data: NDArray[np.float32] | None = None,
    ):
        """Initialize AWQ quantizer.
        
        Args:
            config: Quantization configuration
            calibration_data: Calibration activations for importance
        """
        super().__init__(config)
        self.calibration_data = calibration_data
        self._importance_cache: dict[tuple[int, ...], NDArray[np.float32]] = {}
    
    def quantize(
        self,
        weight: NDArray[np.float32],
        activations: NDArray[np.float32] | None = None,
    ) -> QuantizedTensor:
        """Quantize with activation-aware scaling.
        
        Args:
            weight: Weight tensor [out_features, in_features]
            activations: Calibration activations [num_samples, in_features]
            
        Returns:
            Quantized tensor
        """
        activations = activations if activations is not None else self.calibration_data
        
        # Compute per-channel importance from activations
        if activations is not None:
            importance = self._compute_importance(activations, weight)
            # Apply importance-based scaling
            scaled_weight = weight * importance
        else:
            scaled_weight = weight
        
        # Use group quantization
        linear_quant = LinearQuantizer(self.config)
        qtensor = linear_quant.quantize(scaled_weight)
        
        # Store importance for dequantization
        if activations is not None:
            self._importance_cache[weight.shape] = importance
        
        return qtensor
    
    def dequantize(
        self,
        qtensor: QuantizedTensor,
    ) -> NDArray[np.float32]:
        """Dequantize with importance rescaling."""
        result = qtensor.dequantize()
        
        # Undo importance scaling if cached
        if qtensor.shape in self._importance_cache:
            importance = self._importance_cache[qtensor.shape]
            result = result / importance
        
        return result
    
    def _compute_importance(
        self,
        activations: NDArray[np.float32],
        weight: NDArray[np.float32],
    ) -> NDArray[np.float32]:
        """Compute channel importance from activations.
        
        Uses mean absolute activation as importance measure.
        """
        # Mean absolute activation per input channel
        act_importance = np.mean(np.abs(activations), axis=0)
        
        # Weight magnitude per channel
        weight_importance = np.max(np.abs(weight), axis=0)
        
        # Combined importance (salient = high activation * high weight)
        importance = act_importance * weight_importance
        importance = importance / (np.max(importance) + 1e-8)
        
        # Convert to scaling factors (protect high-importance channels)
        # Higher importance -> larger scale -> less quantization error
        scales = 1.0 + importance * 0.5  # Scale between 1.0 and 1.5
        
        return scales.astype(np.float32)


class GPTQQuantizer(Quantizer):
    """GPTQ Quantization using Hessian-based optimal rounding.
    
    Uses second-order information for optimal weight rounding.
    Reference: https://arxiv.org/abs/2210.17323
    """
    
    def __init__(
        self,
        config: QuantConfig,
        damp_percent: float = 0.01,
        block_size: int = 128,
    ):
        """Initialize GPTQ quantizer.
        
        Args:
            config: Quantization configuration
            damp_percent: Damping factor for Hessian
            block_size: Block size for GPTQ
        """
        super().__init__(config)
        self.damp_percent = damp_percent
        self.block_size = block_size
    
    def quantize(
        self,
        weight: NDArray[np.float32],
        hessian: NDArray[np.float32] | None = None,
    ) -> QuantizedTensor:
        """Quantize using GPTQ algorithm.
        
        Args:
            weight: Weight tensor [out_features, in_features]
            hessian: Hessian matrix (H = X^T X for input X)
            
        Returns:
            Quantized tensor
        """
        out_features, in_features = weight.shape
        
        # If no Hessian, fall back to linear quantization
        if hessian is None:
            linear_quant = LinearQuantizer(self.config)
            return linear_quant.quantize(weight)
        
        # Add damping to Hessian
        diag_mean = np.mean(np.diag(hessian))
        hessian_damp = hessian + self.damp_percent * diag_mean * np.eye(in_features)
        
        # Compute inverse Hessian
        try:
            hessian_inv = np.linalg.inv(hessian_damp)
        except np.linalg.LinAlgError:
            # Fall back if inversion fails
            linear_quant = LinearQuantizer(self.config)
            return linear_quant.quantize(weight)
        
        # GPTQ quantization
        qweight = self._gptq_quantize(weight, hessian_inv)
        
        # Compute scales
        linear_quant = LinearQuantizer(self.config)
        scale, zp = linear_quant._compute_group_params(weight)
        
        # Pack if 4-bit
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
        """Dequantize GPTQ quantized tensor."""
        return qtensor.dequantize()
    
    def _gptq_quantize(
        self,
        weight: NDArray[np.float32],
        hessian_inv: NDArray[np.float32],
    ) -> NDArray[np.int8]:
        """Apply GPTQ quantization with error compensation.
        
        Processes columns in blocks, compensating quantization
        error in subsequent columns.
        """
        out_features, in_features = weight.shape
        qweight = np.zeros_like(weight, dtype=np.int8)
        w = weight.copy()
        
        for block_start in range(0, in_features, self.block_size):
            block_end = min(block_start + self.block_size, in_features)
            
            for col in range(block_start, block_end):
                # Compute scale for this group
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
                
                # Quantize column
                col_data = w[:, col]
                q = np.round(col_data / scale).astype(np.int8)
                q = np.clip(q, self.config.qmin, self.config.qmax)
                qweight[:, col] = q
                
                # Compute quantization error
                dequant = q.astype(np.float32) * scale
                error = col_data - dequant
                
                # Compensate error in remaining columns using Hessian
                for j in range(col + 1, block_end):
                    h_ratio = hessian_inv[col, j] / (hessian_inv[col, col] + 1e-8)
                    w[:, j] += error * h_ratio
        
        return qweight


class DequantizedLinear:
    """Dequantized linear layer for inference.
    
    Performs fused dequantization and matrix multiplication.
    """
    
    def __init__(
        self,
        qweight: QuantizedTensor,
        bias: NDArray[np.float32] | None = None,
    ):
        """Initialize dequantized linear.
        
        Args:
            qweight: Quantized weight tensor
            bias: Optional bias vector
        """
        self.qweight = qweight
        self.bias = bias
        self._dequant_cache: NDArray[np.float32] | None = None
    
    def forward(
        self,
        x: NDArray[np.float32],
        use_cache: bool = True,
    ) -> NDArray[np.float32]:
        """Forward pass with dequantization.
        
        Args:
            x: Input tensor [..., in_features]
            use_cache: Whether to cache dequantized weights
            
        Returns:
            Output tensor [..., out_features]
        """
        # Dequantize weights (with caching)
        if use_cache and self._dequant_cache is not None:
            weight = self._dequant_cache
        else:
            weight = self.qweight.dequantize()
            if use_cache:
                self._dequant_cache = weight
        
        # Matrix multiplication
        output = x @ weight.T
        
        if self.bias is not None:
            output = output + self.bias
        
        return output
    
    def clear_cache(self):
        """Clear dequantization cache."""
        self._dequant_cache = None
    
    @property
    def in_features(self) -> int:
        """Input feature dimension."""
        return self.qweight.shape[1] if len(self.qweight.shape) >= 2 else self.qweight.shape[0]
    
    @property
    def out_features(self) -> int:
        """Output feature dimension."""
        return self.qweight.shape[0]


# Utility functions

def pack_int4(data: NDArray[np.int8]) -> NDArray[np.int8]:
    """Pack two int4 values into one int8.
    
    Args:
        data: Int4 values as int8 [-8, 7] or [0, 15]
        
    Returns:
        Packed int8 array (half the size)
    """
    flat = data.flatten()
    if len(flat) % 2 != 0:
        flat = np.pad(flat, (0, 1), constant_values=0)
    
    # Pack pairs of int4 into int8
    evens = flat[0::2].astype(np.int8)
    odds = flat[1::2].astype(np.int8)
    
    # Lower 4 bits from evens, upper 4 bits from odds
    packed = (evens & 0x0F) | ((odds & 0x0F) << 4)
    return packed.astype(np.int8)


def unpack_int4(packed: NDArray[np.int8]) -> NDArray[np.int8]:
    """Unpack int8 into two int4 values.
    
    Args:
        packed: Packed int8 array
        
    Returns:
        Unpacked int4 values as int8
    """
    flat = packed.flatten()
    
    # Extract lower and upper 4 bits
    lower = flat & 0x0F
    upper = (flat >> 4) & 0x0F
    
    # Sign extend if using signed int4
    lower = np.where(lower > 7, lower - 16, lower)
    upper = np.where(upper > 7, upper - 16, upper)
    
    # Interleave
    unpacked = np.empty(len(flat) * 2, dtype=np.int8)
    unpacked[0::2] = lower
    unpacked[1::2] = upper
    
    return unpacked


def compute_scales_minmax(
    weight: NDArray[np.float32],
    bits: int = 8,
    symmetric: bool = True,
) -> tuple[NDArray[np.float32], NDArray[np.int32] | None]:
    """Compute min-max quantization scales.
    
    Args:
        weight: Weight tensor
        bits: Number of bits
        symmetric: Whether to use symmetric quantization
        
    Returns:
        Tuple of (scale, zero_point)
    """
    qmax = (1 << (bits - 1)) - 1 if symmetric else (1 << bits) - 1
    qmin = -(1 << (bits - 1)) if symmetric else 0
    
    if symmetric:
        max_val = np.max(np.abs(weight))
        scale = max_val / qmax if max_val > 0 else 1.0
        return np.array([scale], dtype=np.float32), None
    else:
        min_val = np.min(weight)
        max_val = np.max(weight)
        scale = (max_val - min_val) / (qmax - qmin)
        scale = max(scale, 1e-8)
        zp = int(round(-min_val / scale)) + qmin
        zp = np.clip(zp, qmin, qmax)
        return np.array([scale], dtype=np.float32), np.array([zp], dtype=np.int32)


def quantize_tensor(
    tensor: NDArray[np.float32],
    bits: int = 8,
    group_size: int = 128,
    symmetric: bool = True,
    scheme: str = "linear",
) -> QuantizedTensor:
    """Convenience function to quantize a tensor.
    
    Args:
        tensor: Tensor to quantize
        bits: Number of bits (4 or 8)
        group_size: Quantization group size
        symmetric: Whether symmetric quantization
        scheme: Quantization scheme ("linear", "awq", "gptq")
        
    Returns:
        Quantized tensor
    """
    config = QuantConfig(
        bits=bits,
        scheme=QuantScheme[scheme.upper()] if scheme.upper() in QuantScheme.__members__ else QuantScheme.INT8,
        strategy=QuantStrategy.GROUP if group_size > 0 else QuantStrategy.TENSOR,
        group_size=group_size,
        symmetric=symmetric,
    )
    
    if scheme.lower() == "awq":
        quantizer = AWQQuantizer(config)
    elif scheme.lower() == "gptq":
        quantizer = GPTQQuantizer(config)
    else:
        quantizer = LinearQuantizer(config)
    
    return quantizer.quantize(tensor)


def get_quantization_error(
    original: NDArray[np.float32],
    qtensor: QuantizedTensor,
) -> dict[str, float]:
    """Compute quantization error metrics.
    
    Args:
        original: Original tensor
        qtensor: Quantized tensor
        
    Returns:
        Dictionary with error metrics
    """
    dequant = qtensor.dequantize()
    
    mse = np.mean((original - dequant) ** 2)
    mae = np.mean(np.abs(original - dequant))
    max_error = np.max(np.abs(original - dequant))
    
    # Signal-to-noise ratio
    signal_power = np.mean(original ** 2)
    noise_power = mse
    snr = 10 * np.log10(signal_power / (noise_power + 1e-10))
    
    return {
        "mse": float(mse),
        "mae": float(mae),
        "max_error": float(max_error),
        "snr_db": float(snr),
        "compression_ratio": float(qtensor.compression_ratio),
    }
