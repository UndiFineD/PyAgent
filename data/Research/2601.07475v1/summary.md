# ARCQuant: Augmented Residual Channels for NVFP4 Quantization
**arXiv ID**: 2601.07475
**Date**: January 11, 2026
**Authors**: Unknown (Survey identification)

## Summary
ARCQuant is a post-training quantization (PTQ) framework designed to optimize 4-bit floating-point (NVFP4) inference. It identifies "outlier" channels that are most sensitive to quantization error and "augments" the residual stream to compensate for the precision loss in those specific channels.

## Key Innovations
1.  **Augmented Residual Channels (ARC)**: Adds a low-rank or sparse compensation term to the residual stream that specifically targets the errors introduced by 4-bit quantization.
2.  **Sensitivity Analysis**: Automatically detects which layers and channels require augmentation based on a calibration dataset.
3.  **Hardware Optimization**: Designed for the latest NVIDIA Blackwell architectures which native support FP4.

## Performance
-   Boosts 4-bit (NVFP4) accuracy to within 0.5% of FP8 performance.
-   Reduces model VRAM requirements by 50% vs FP8 with minimal latency penalty.

## Implementation Details for PyAgent
-   **Integration Point**: `src/infrastructure/quantization/ARCQuantizer.py`.
-   **Mechanism**:
    -   Apply standard 4-bit quantization to weights.
    -   Maintain a small `residual_compensator` matrix for sensitive channels.
    -   Apply the compensator during the forward pass in the `LogicEngine`.
