# PackKV: Reducing KV Cache Memory via LLM-Aware Lossy Compression
**arXiv ID**: 2512.24449
**Date**: December 21, 2025
**GitHub**: [BoJiang03/PackKV](https://github.com/BoJiang03/PackKV)

## Summary
PackKV is a lossy compression framework designed to tackle the memory bottleneck of long-context LLM inference. It uses "LLM-aware" quantization and a novel "encode-aware repacking" strategy to compress Keys ($K$) and Values ($V$) into a few bits while maintaining high attention fidelity.

## Technical Innovations
1.  **Bit-Packing & Quantization**: Maps floating-point tensors to low-bit integers (e.g., 4-bit) using adaptive per-token scaling.
2.  **Encode-Aware Repacking**: Leverages the **Permutation Invariance** of the attention mechanism. It reorders vectors within memory blocks to group similar values together, which significantly increases bit-packing efficiency and reduces reconstruction error.
3.  **Fused Decompression Kernels**: Instead of decompressing back to VRAM, PackKV decompresses directly into **GPU Registers** during the Matrix-Vector multiplication (attention score calculation). This saves immense global memory bandwidth ($75\%+$ Improvement).
4.  **Seamless Appending**: Unlike some compression schemes that require re-compressing the entire context, PackKV operates on independent 2D blocks (e.g., 64 tokens), making it compatible with **PagedAttention**.

## Performance Benchmarks
- **Memory Reduction**: **153.2%** better than KIVI for $K$, and **179.6%** better for $V$.
- **Throughput**: Improved by **75.7% (K)** and **171.7% (V)** over cuBLAS-based attention.
- **Hardware Tested**: NVIDIA A100 (40GB) and RTX Pro 6000.

## Implementation Details for PyAgent
- **Integration Point**: `src/infrastructure/engine/kv_cache/`
- **Key Modules**:
    - `PackKVQuantizer`: Handles per-token adaptive scaling.
    - `Repacker`: Groups similar vectors within blocks of 64.
    - `FusedAttentionKernel` (Rust/CUDA): Real-time register-level decompression.

## Mathematical Concepts
- **Permutation Invariance**: $Attention(Q, K_{permuted}) \approx Attention(Q, K)$.
- **Compression Ratio**: 4-bit quantization with bit-packing yields a theoretical $8x$ reduction in memory footprint over FP32.

## References
- [arXiv:2512.24449](https://arxiv.org/abs/2512.24449)
