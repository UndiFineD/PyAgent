# PyTorch

## Overview
**PyTorch** is an open-source machine learning library developed by Meta AI. It is currently the dominant framework for AI research due to its flexibility and "Pythonic" nature.

## Key Features

### 1. Dynamic Computation Graphs (Eager Execution)
Unlike TensorFlow 1.x (which built a static graph first), PyTorch builds the graph on-the-fly as you execute code.
*   **Benefit**: You can use standard Python control flow (`if`, `for`, `while`) within your model definition. Debugging is easy because you can print tensor values at any step.

### 2. The `torch.Tensor`
The fundamental data structure. Similar to a NumPy array but runs on GPU.
*   **Autograd**: Tensors track their history. If you set `requires_grad=True`, PyTorch records every operation performed on the tensor to automatically calculate gradients later (`tensor.backward()`).

### 3. `torch.nn.Module`
The base class for all neural network modules.
*   **Structure**: You define layers in `__init__` and connectivity in `forward`.
*   **Parameter Management**: Automatically tracks all learnable weights (`nn.Parameter`) inside the module.

### 4. `torch.optim`
Implements optimization algorithms like SGD, Adam, and RMSprop.
*   **Usage**: `optimizer.step()` updates the weights based on the computed gradients.

### 5. `torch.utils.data`
*   **Dataset**: An abstract class representing a dataset.
*   **DataLoader**: Wraps a dataset to provide batching, shuffling, and parallel data loading (multiprocessing).

## PyTorch vs. TensorFlow
| Feature | PyTorch | TensorFlow (Keras) |
| :--- | :--- | :--- |
| **Graph Type** | Dynamic (Define-by-Run) | Static/Dynamic (Define-and-Run) |
| **Debugging** | Easy (Standard Python) | Harder (Graph context) |
| **Deployment** | TorchScript / ONNX | TF Serving / TFLite (Mature) |
| **Research** | Dominant | Declining |
| **Industry** | Growing rapidly | Established |

## Ecosystem
*   **TorchVision**: Datasets and models for Computer Vision.
*   **TorchAudio**: Audio processing.
*   **TorchText**: NLP (though Hugging Face is preferred now).
*   **PyTorch Lightning**: A wrapper to reduce boilerplate code (training loops).
