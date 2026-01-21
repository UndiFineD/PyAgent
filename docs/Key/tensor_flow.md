# TensorFlow

TensorFlow (TF) is an end-to-end open-source platform for machine learning developed by Google. While PyTorch has become dominant in research, TensorFlow remains a powerhouse in production environments.

## Core Concepts

### 1. Static vs. Dynamic Graphs
*   **TensorFlow 1.x (Static)**: You defined a computational graph first, then compiled it, then ran data through it. Hard to debug, but easy to optimize.
*   **TensorFlow 2.x (Eager Execution)**: Runs operations immediately as they are called from Python (like PyTorch). Easier to debug.
*   **`@tf.function`**: A decorator that converts a Python function into a static TensorFlow graph (AutoGraph) for performance deployment.

### 2. Keras
The high-level API for TensorFlow.
*   **Sequential API**: Simple stack of layers. `model = Sequential([Dense(10), Dense(1)])`.
*   **Functional API**: More flexible, handles non-linear topologies, shared layers, and multiple inputs/outputs. `x = Dense(10)(input); output = Dense(1)(x)`.
*   **Model Subclassing**: Most flexible, similar to PyTorch `nn.Module`. You define `__init__` and `call`.

## TFX (TensorFlow Extended)
A production-ready machine learning platform. It's not just for training, but for the entire pipeline.
*   **TensorFlow Data Validation (TFDV)**: Detects anomalies in data (drift, missing values).
*   **TensorFlow Transform (TFT)**: Preprocessing data. Crucially, it saves the preprocessing logic as a graph so it can be applied identically during serving (preventing training-serving skew).
*   **TensorFlow Model Analysis (TFMA)**: Evaluates models on slices of data (e.g., "How does the model perform on users from Canada vs USA?").
*   **TensorFlow Serving**: A flexible, high-performance serving system for machine learning models, designed for production environments.

## TensorFlow Lite (TFLite)
A set of tools to run TensorFlow models on mobile, embedded, and IoT devices.
*   **Quantization**: Reducing the precision of the numbers (e.g., Float32 to Int8) to reduce model size and latency with minimal accuracy loss.

## TensorFlow.js
A library for machine learning in JavaScript. Allows you to train and deploy models in the browser or on Node.js.
