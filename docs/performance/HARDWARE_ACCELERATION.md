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

## Canonical AMD NPU Runtime Guidance

This section is the canonical runtime guidance location for amd_npu feature usage and verification.

### Activation Commands

PyAgent provides two command forms for AMD NPU feature verification:

**Feature-Off (Disabled) Path:**
```bash
cargo run --bin pyagent_cli -- amd-npu-status
```

**Feature-On (Enabled) Path:**
```bash
cargo run --features amd_npu --bin pyagent_cli -- amd-npu-status
```

### Supported Environments

The AMD NPU feature is supported on the following platforms:

- **OS**: Windows x86_64
- **Hardware**: AMD Ryzen AI series (Ryzen 7040/8040/9000 and compatible)
- **Dependency**: AMD Ryzen AI SDK (required for compilation and execution)

### Unsupported Paths

The following environments are explicitly unsupported:

- Linux/macOS systems (no AMD Ryzen AI SDK available)
- Non-AMD processors
- ARM64 or other non-x86_64 architectures
- Older AMD Ryzen processors without NPU hardware

### Fallback Semantics

When the AMD NPU feature is unavailable (not compiled in, SDK not installed, or unsupported hardware), the runtime returns a specific exit code:

- **Exit Status Code**: `-1` (AMD_NPU_STATUS_UNAVAILABLE)
- **Meaning**: The amd_npu feature is not available in this environment
- **Safe Interpretation**: Applications must check for this exit code and fall back to CPU execution without error

When you observe an exit status of `-1`, the safe interpretation is that the AMD NPU hardware or SDK is not available in the current environment, and the application should transparently fall back to standard CPU-based execution.

### Validation Evidence Schema

To verify AMD NPU feature support and behavior, use the following mandatory evidence schema:

| Field | Description | Mandatory |
|-------|-------------|-----------|
| Command | The exact shell command executed (e.g., `cargo run --features amd_npu --bin pyagent_cli -- amd-npu-status`) | Yes, all fields are mandatory |
| Exit Status | The exit code returned by the command | Yes |
| Observed Outcome | The actual output or behavior captured from stdout/stderr | Yes |
| Runner Context | The OS, hardware, and SDK information where the command was executed | Yes |

All fields are mandatory for complete evidence audit trails.

### Non-Goals

The following are explicitly **not** in scope for this documentation or the amd_npu feature:

- Automatic AMD SDK download or installation
- Cross-platform SDK compilation (Windows x86_64 only)
- Real-time NPU utilization monitoring (future work)
- Hardware feature detection beyond exit code checking

### CI Defer Contract

The amd_npu feature and its validation are **deferred from CI automation**. This is a deliberate design choice because:

1. CI environments may not have AMD Ryzen AI hardware
2. The SDK is Windows x86_64-only and requires manual installation
3. CI defer contract applies to all AMD NPU tests and validations
4. Feature validation is the responsibility of hardware-owning developers

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
