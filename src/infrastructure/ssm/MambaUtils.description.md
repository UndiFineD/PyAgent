# MambaUtils

**File**: `src\infrastructure\ssm\MambaUtils.py`  
**Type**: Python Module  
**Summary**: 1 classes, 13 functions, 7 imports  
**Lines**: 388  
**Complexity**: 17 (moderate)

## Overview

Mamba Utilities.

vLLM Pattern: vllm/model_executor/layers/mamba/mamba_utils.py
Utility functions for Mamba computation.

## Classes (1)

### `MambaBlockState`

State for a block of Mamba layers.

**Methods** (4):
- `zeros(cls, num_layers, batch_size, d_inner, conv_kernel_size, ssm_state_size, dtype)`
- `get_layer(self, layer_idx)`
- `set_layer(self, layer_idx, conv_state, ssm_state)`
- `clone(self)`

## Functions (13)

### `compute_ssm_state_shape(batch_size, d_inner, ssm_state_size)`

Compute shape for SSM state tensor.

vLLM Pattern: MambaStateShapeCalculator

### `compute_conv_state_shape(batch_size, d_inner, conv_kernel_size)`

Compute shape for conv state tensor.

vLLM Pattern: MambaStateShapeCalculator

### `compute_state_dtype(input_dtype, force_fp32)`

Determine appropriate dtype for state tensors.

vLLM Pattern: MambaStateDtypeCalculator

### `discretize_ssm(A, B, dt)`

Discretize continuous SSM matrices.

Zero-order hold discretization:
    dA = exp(dt * A)
    dB = (dA - I) * inv(A) * B ≈ dt * B (for small dt)

Args:
    A: State transition [d_inner, ssm_state_size]
    B: Input projection [batch, seq_len, ssm_state_size] or [batch, ssm_state_size]
    dt: Time step [batch, seq_len, d_inner] or [batch, d_inner]

Returns:
    dA: Discretized state transition
    dB: Discretized input projection

### `apply_ssm_recurrence(x, dA, dB, C, D, initial_state)`

Apply SSM recurrence.

h_t = dA * h_{t-1} + dB * x_t
y_t = C @ h_t + D * x_t

Args:
    x: Input [batch, seq_len, d_inner]
    dA: Discretized A [batch, seq_len, d_inner, ssm_state_size]
    dB: Discretized B [batch, seq_len, d_inner, ssm_state_size]
    C: Output projection [batch, seq_len, ssm_state_size]
    D: Skip connection [d_inner]
    initial_state: Initial state [batch, d_inner, ssm_state_size]

Returns:
    output: SSM output [batch, seq_len, d_inner]
    final_state: Final state [batch, d_inner, ssm_state_size]

### `silu_activation(x)`

SiLU (Swish) activation: x * sigmoid(x).

More numerically stable than naive implementation.

### `swish_activation(x, beta)`

Swish activation with configurable beta: x * sigmoid(beta * x).

### `softplus(x, beta, threshold)`

Softplus activation: (1/beta) * log(1 + exp(beta * x)).

Reverts to linear for large values.

### `chunk_sequence(x, chunk_size)`

Split sequence into chunks for memory-efficient processing.

Args:
    x: Input [batch, seq_len, hidden]
    chunk_size: Maximum chunk length

Returns:
    List of chunks

### `merge_chunks(chunks)`

Merge chunked outputs back to single sequence.

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `dataclasses.dataclass`
- `math`
- `numpy`
- `rust_core`
- `typing.Any`
- `typing.TYPE_CHECKING`

---
*Auto-generated documentation*
