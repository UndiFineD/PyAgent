# Hardware Acceleration in PyAgent

PyAgent is designed to be hardware-agnostic but optimized for specific "hot paths" using specialized acceleration engines. This document outlines the strategies for leveraging advanced hardware like NPUs, GPUs, and specialized AI accelerators.

## AMD Ryzen AI (NPU)

AMD's NPUs (found in Ryzen 7040/8040/9000 series) provide a high-efficiency alternative to GPU/CPU inference for mobile and edge devices. PyAgent integrates support for these via the following strategies:

### 1. Direct Rust NPU Bindings (FFI)
Since the AMD Ryzen AI SDK primarily exposes C APIs, PyAgent's `rust_core` provides (or plans to provide) FFI wrappers to interact directly with the NPU.

```rust
// Strategic implementation path for AMD NPU in rust_core
#[link(name = "amd_npu")] 
extern "C" {
    fn amd_npu_init() -> i32;
    fn amd_npu_run_model(model_path: *const i8) -> i32;
}
```

### 2. FastFlowLM Integration
For high-level orchestration, PyAgent utilizes `FastFlowLM` (https://github.com/FastFlowLM/FastFlowLM) as a preferred NPU execution backend.
- **Optimization Strategy**: Identified as `FastFlowLM (NPU Optimized)` in `ModelOptimizerAgent`.
- **Command Routing**: Automatically generated via `get_fastflow_command`.

### 3. ONNX Runtime with AMD Execution Provider (EP)
PyAgent supports ONNX Runtime as a fallback or secondary engine.
- **AMD EP**: If an AMD-compatible ONNX Execution Provider is detected, PyAgent configures the runtime to offload kernels to the NPU or ROCm-compatible GPUs.

---

## AMD GPU (ROCm)

For high-throughput server tasks, ROCm (AMD’s GPU compute stack) is utilized over CUDA when AMD hardware is detected.

- **HIP Bindings**: `rust_core` utilizes HIP (Heterogeneous-compute Interface for Portability) for GPU-accelerated math kernels.
- **rocBLAS**: Preferred for dense matrix multiplications in `LogicCore` and `InferenceCore`.

---

## NVIDIA (Hopper/H100)

For high-end data center hardware, PyAgent implements optimizations for the NVIDIA Hopper architecture.

- **FP8 Precision**: Native Support for H100 FP8 via the Transformer Engine.
- **HopperSim**: Simulated performance modeling for task scheduling and model partitioning.

---

## Future Directions
- **XDNA2 Support**: Enhanced support for AMD's next-gen XDNA architecture.
- **Unified Acceleration Layer**: Developing a common interface in `rust_core` that automatically detects and wraps available NPUs (AMD, Qualcomm, Apple Neural Engine).
