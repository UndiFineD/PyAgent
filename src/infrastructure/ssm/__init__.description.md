# __init__

**File**: `src\infrastructure\ssm\__init__.py`  
**Type**: Python Module  
**Summary**: 0 classes, 0 functions, 14 imports  
**Lines**: 48  
**Complexity**: 0 (simple)

## Overview

State Space Model (SSM) Infrastructure.

Phase 38: Mamba SSM patterns from vLLM with beyond-vLLM innovations.

Modules:
    MambaMixer: Mamba-1 selective state space model
    MambaUtils: Utilities for Mamba computation

## Dependencies

**Imports** (14):
- `src.infrastructure.ssm.MambaMixer.CausalConv1d`
- `src.infrastructure.ssm.MambaMixer.HybridMambaMixer`
- `src.infrastructure.ssm.MambaMixer.Mamba2Mixer`
- `src.infrastructure.ssm.MambaMixer.MambaConfig`
- `src.infrastructure.ssm.MambaMixer.MambaMixer`
- `src.infrastructure.ssm.MambaMixer.MambaOutput`
- `src.infrastructure.ssm.MambaMixer.MambaState`
- `src.infrastructure.ssm.MambaMixer.SelectiveScan`
- `src.infrastructure.ssm.MambaUtils.apply_ssm_recurrence`
- `src.infrastructure.ssm.MambaUtils.compute_conv_state_shape`
- `src.infrastructure.ssm.MambaUtils.compute_ssm_state_shape`
- `src.infrastructure.ssm.MambaUtils.discretize_ssm`
- `src.infrastructure.ssm.MambaUtils.silu_activation`
- `src.infrastructure.ssm.MambaUtils.swish_activation`

---
*Auto-generated documentation*
