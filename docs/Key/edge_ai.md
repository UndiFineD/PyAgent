# Edge AI & TinyML

Running AI on small devices (phones, microcontrollers, IoT) rather than massive cloud servers.

## 1. Why Edge AI?

*   **Latency**: No need to send data to the cloud and wait for a response (critical for self-driving cars).
*   **Privacy**: Data (voice, video) stays on the device.
*   **Bandwidth**: Sending 4K video streams to the cloud is expensive.
*   **Power**: Radios (Wi-Fi/5G) consume more power than local computation.

## 2. Optimization Techniques

To fit a 100MB model onto a 256KB microcontroller:

*   **Quantization**: Convert 32-bit floats (FP32) to 8-bit integers (INT8).
    *   Reduces size by 4x.
    *   Often speeds up inference (integer math is faster).
*   **Pruning**: Remove connections (weights) that are close to zero.
    *   Sparse models are smaller and faster.
*   **Knowledge Distillation**: Train a tiny "Student" network to mimic a giant "Teacher" network.

## 3. Hardware

*   **Microcontrollers (MCU)**: ARM Cortex-M, ESP32. (TensorFlow Lite for Microcontrollers).
*   **Mobile**: Apple Neural Engine, Qualcomm Hexagon DSP.
*   **Edge TPU**: Google's Coral USB accelerator (ASIC for running TFLite models).
*   **NPU (Neural Processing Unit)**: Specialized silicon in modern CPUs/SoCs designed solely for matrix multiplication.
