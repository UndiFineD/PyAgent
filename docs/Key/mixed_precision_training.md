# Mixed Precision Training

## Overview
**Mixed Precision Training** involves using both 16-bit (half-precision) and 32-bit (single-precision) floating-point types during model training.
*   **Goal**: Speed up training (2x-3x) and reduce memory usage (allowing larger batch sizes) without sacrificing model accuracy.

## Data Types
1.  **FP32 (float32)**: Standard single precision. High range, high precision.
2.  **FP16 (float16)**: Half precision. Smaller range, lower precision.
3.  **BF16 (bfloat16)**: Brain Floating Point (Google). Same range as FP32, but lower precision (truncated mantissa).

## How it Works (Automatic Mixed Precision - AMP)
Modern frameworks (PyTorch AMP) automate this process:
1.  **Storage**: Weights are stored in FP32 (Master Copy).
2.  **Forward Pass**: Weights are cast to FP16/BF16. Activations are computed in FP16.
3.  **Backward Pass**: Gradients are computed in FP16.
4.  **Update**: Gradients are cast back to FP32 and applied to the Master Copy.

## The Problem: Underflow
FP16 has a very small range. Small gradients (e.g., $10^{-8}$) can underflow to zero, causing the model to stop learning.

## The Solution: Loss Scaling
*   **Mechanism**: Multiply the loss by a large factor (e.g., 65536) before backpropagation.
*   **Effect**: This shifts the gradients into the representable range of FP16.
*   **Unscaling**: Divide the gradients by the same factor before the optimizer update (in FP32).

## BF16 vs. FP16
*   **BF16** is preferred on newer hardware (NVIDIA Ampere A100/H100, TPUs) because it has the same dynamic range as FP32, so it rarely needs Loss Scaling.
*   **FP16** is used on older hardware (V100, T4) and requires Loss Scaling.
