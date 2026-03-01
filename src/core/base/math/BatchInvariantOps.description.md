# BatchInvariantOps

**File**: `src\core\base\math\BatchInvariantOps.py`  
**Type**: Python Module  
**Summary**: 1 classes, 12 functions, 9 imports  
**Lines**: 653  
**Complexity**: 25 (complex)

## Overview

BatchInvariantOps - Deterministic GPU operations for reproducible inference.

Implements vLLM's batch_invariant.py patterns for deterministic execution:
- matmul_persistent: Triton persistent GEMM kernel
- softmax_batch_invariant: Numerically stable softmax
- mean_batch_invariant: Deterministic mean reduction
- mm/bmm_batch_invariant: Matrix multiplication wrappers

Beyond vLLM: Automatic precision selection based on input dtype.

## Classes (1)

### `BatchInvariantOps`

Container class for batch-invariant operations.

Provides a consistent interface and tracks usage statistics.

**Methods** (13):
- `__init__(self, device, dtype)`
- `matmul(self, a, b, bias)`
- `softmax(self, input, dim, dtype)`
- `log_softmax(self, input, dim)`
- `mean(self, input, dim, keepdim, dtype)`
- `mm(self, a, b, out)`
- `bmm(self, a, b, out)`
- `addmm(self, bias, a, b)`
- `gelu(self, input)`
- `layer_norm(self, input, normalized_shape, weight, bias, eps)`
- ... and 3 more methods

## Functions (12)

### `matmul_persistent(a, b, bias)`

Persistent GEMM using Triton kernel.

Provides deterministic matrix multiplication regardless of batch order.
Falls back to torch.matmul if Triton unavailable.

Args:
    a: Input tensor [M, K]
    b: Weight tensor [K, N]
    bias: Optional bias tensor [N]
    
Returns:
    Output tensor [M, N]

### `softmax_batch_invariant(input, dim, dtype)`

Numerically stable softmax that is deterministic across batch orderings.

Uses explicit max subtraction and normalization to ensure reproducibility.

Args:
    input: Input tensor
    dim: Dimension to apply softmax over
    dtype: Optional output dtype
    
Returns:
    Softmax output tensor

### `log_softmax_batch_invariant(input, dim)`

Numerically stable log softmax that is deterministic.

Args:
    input: Input tensor
    dim: Dimension to apply log softmax over
    
Returns:
    Log softmax output tensor

### `mean_batch_invariant(input, dim, keepdim, dtype)`

Deterministic mean reduction.

Uses sum/count instead of built-in mean for reproducibility.

Args:
    input: Input tensor
    dim: Dimension(s) to reduce
    keepdim: Whether to keep reduced dimensions
    dtype: Optional output dtype
    
Returns:
    Mean reduced tensor

### `mm_batch_invariant(a, b)`

Deterministic matrix multiplication (2D x 2D).

Args:
    a: First matrix [M, K]
    b: Second matrix [K, N]
    out: Optional output tensor
    
Returns:
    Result matrix [M, N]

### `bmm_batch_invariant(a, b)`

Deterministic batched matrix multiplication (3D x 3D).

Args:
    a: First batch of matrices [B, M, K]
    b: Second batch of matrices [B, K, N]
    out: Optional output tensor
    
Returns:
    Result batch [B, M, N]

### `addmm_batch_invariant(bias, a, b)`

Deterministic bias + matrix multiplication.

Args:
    bias: Bias vector [N]
    a: First matrix [M, K]
    b: Second matrix [K, N]
    
Returns:
    Result: bias + a @ b, shape [M, N]

### `gelu_batch_invariant(input)`

Deterministic GELU activation.

Uses the explicit formula instead of approximations.

Args:
    input: Input tensor
    
Returns:
    GELU output tensor

### `layer_norm_batch_invariant(input, normalized_shape, weight, bias, eps)`

Deterministic layer normalization.

Uses explicit mean/variance computation for reproducibility.

Args:
    input: Input tensor
    normalized_shape: Shape over which to normalize
    weight: Optional scale parameter
    bias: Optional shift parameter
    eps: Epsilon for numerical stability
    
Returns:
    Normalized tensor

### `rms_norm_batch_invariant(input, weight, eps)`

Deterministic RMS normalization.

RMS norm doesn't subtract mean, just divides by RMS.

Args:
    input: Input tensor
    weight: Optional scale parameter
    eps: Epsilon for numerical stability
    
Returns:
    RMS normalized tensor

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `logging`
- `math`
- `numpy`
- `scipy.special`
- `torch`
- `triton`
- `triton.language`
- `typing.Any`

---
*Auto-generated documentation*
