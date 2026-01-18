"""
State Space Model (SSM) Infrastructure.

Phase 38: Mamba SSM patterns from vLLM with beyond-vLLM innovations.

Modules:
    MambaMixer: Mamba-1 selective state space model
    MambaUtils: Utilities for Mamba computation
"""

from src.infrastructure.ssm.MambaMixer import (
    MambaConfig,
    MambaState,
    MambaOutput,
    MambaMixer,
    Mamba2Mixer,
    CausalConv1d,
    SelectiveScan,
    HybridMambaMixer,
)

from src.infrastructure.ssm.MambaUtils import (
    compute_ssm_state_shape,
    compute_conv_state_shape,
    discretize_ssm,
    apply_ssm_recurrence,
    silu_activation,
    swish_activation,
)

__all__ = [
    # MambaMixer
    "MambaConfig",
    "MambaState",
    "MambaOutput",
    "MambaMixer",
    "Mamba2Mixer",
    "CausalConv1d",
    "SelectiveScan",
    "HybridMambaMixer",
    # MambaUtils
    "compute_ssm_state_shape",
    "compute_conv_state_shape",
    "discretize_ssm",
    "apply_ssm_recurrence",
    "silu_activation",
    "swish_activation",
]
