# Convolutional Neural Networks (CNNs)

## What is a CNN?
A Convolutional Neural Network (CNN or ConvNet) is a deep learning architecture designed specifically for processing grid-like data, such as images. Before Transformers took over, CNNs were the undisputed kings of Computer Vision.

## Core Concepts

### 1. Convolutional Layer (The "Eye")
*   Instead of connecting every pixel to every neuron (which would require billions of weights), a CNN uses a small **Kernel** (or Filter), e.g., a 3x3 matrix.
*   This kernel "slides" (convolves) across the image, looking for specific features like vertical edges, horizontal lines, or curves.
*   **Parameter Sharing**: The same kernel is used across the whole image, drastically reducing the number of parameters.

### 2. Pooling Layer (The "Zoom Out")
*   Reduces the spatial dimensions (Width x Height) of the image to reduce computation and make the model invariant to small translations.
*   **Max Pooling**: Takes the maximum value in a window (e.g., 2x2), keeping only the strongest feature.

### 3. Fully Connected Layer (The "Brain")
*   After extracting features via multiple convolution and pooling layers, the data is flattened and passed to a standard MLP to make the final classification (e.g., "Cat" vs "Dog").

## Famous Architectures
*   **LeNet-5 (1998)**: Yann LeCun's early model for reading handwritten digits (MNIST).
*   **AlexNet (2012)**: The breakthrough model that won ImageNet and started the Deep Learning boom.
*   **VGG (2014)**: Used very deep stacks of small 3x3 filters.
*   **ResNet (2015)**: Introduced **Residual Connections** (Skip Connections), allowing training of extremely deep networks (100+ layers) by preventing the vanishing gradient problem.

## Modern Usage
While Vision Transformers (ViTs) are now SOTA for massive datasets, CNNs (like EfficientNet and ConvNeXt) are still widely used because:
*   They are faster on smaller hardware (Edge AI).
*   They require less training data to converge (better inductive bias).
