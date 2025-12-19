# ONNX (Open Neural Network Exchange)

## Overview
**ONNX** is an open standard format for representing machine learning models. It allows models trained in one framework (e.g., PyTorch) to be deployed in another (e.g., ONNX Runtime, TensorRT) or on different hardware (Edge devices, Web).

## The Problem it Solves
Without ONNX, deploying a PyTorch model to a C++ production environment or a mobile app requires complex conversion scripts or heavy dependencies. ONNX provides a common intermediate representation (IR).

## How It Works
1.  **Export**: You train your model in PyTorch/TensorFlow/Scikit-Learn.
2.  **Convert**: You export the model to a `.onnx` file. This file contains the computation graph (nodes are operations like `Conv2d`, `Relu`, `MatMul`).
3.  **Run**: You load the `.onnx` file using an **ONNX Runtime**.

## ONNX Runtime (ORT)
A cross-platform inference engine built by Microsoft to run ONNX models efficiently.
*   **Execution Providers (EPs)**: ORT can delegate computation to hardware-specific accelerators:
    *   **CUDA**: NVIDIA GPUs.
    *   **TensorRT**: Optimized NVIDIA inference.
    *   **OpenVINO**: Intel CPUs.
    *   **CoreML**: Apple devices.
    *   **WebAssembly (WASM)**: Running models in the browser.

## Benefits
*   **Interoperability**: Train in PyTorch, deploy in C#, Java, or JavaScript.
*   **Performance**: ONNX Runtime often provides faster inference than the native framework (PyTorch/TF) due to graph optimizations (node fusion, constant folding).
*   **Hardware Support**: Write once, run anywhere (Cloud, Edge, Mobile, Web).

## Limitations
*   **Operator Support**: Not all PyTorch/TF operations have a corresponding ONNX operator. Complex dynamic control flow can be hard to export.
