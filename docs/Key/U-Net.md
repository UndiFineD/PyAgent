# U-Net

## Overview
**U-Net** is a convolutional neural network architecture designed for fast and precise image segmentation. It was introduced by Ronneberger et al. in 2015 for biomedical image segmentation but has since become the standard backbone for modern generative models (like Stable Diffusion).

## Architecture: The "U" Shape
The network consists of two paths that form a U-shape:

### 1. Contracting Path (Encoder)
*   Captures **context** (what is in the image).
*   Consists of repeated applications of two 3x3 convolutions (ReLU), followed by a 2x2 max pooling operation for downsampling.
*   At each downsampling step, the number of feature channels is doubled.
*   The spatial resolution decreases, but the semantic information increases.

### 2. Expansive Path (Decoder)
*   Enables precise **localization** (where is it).
*   Consists of upsampling of the feature map followed by a 2x2 convolution ("up-convolution") that halves the number of feature channels.
*   Concatenation with the correspondingly cropped feature map from the contracting path.
*   Two 3x3 convolutions followed by ReLU.

## Skip Connections
The key innovation of U-Net is the **long skip connections** between the Encoder and Decoder layers of the same resolution.
*   These connections concatenate the high-resolution features from the contracting path with the upsampled output.
*   This allows the network to recover fine-grained spatial details that are lost during pooling, which is crucial for pixel-perfect segmentation.

## Evolution: From Segmentation to Generation
While originally for segmentation (Output: Mask), U-Net became the dominant architecture for **Diffusion Models** (Output: Noise prediction).
*   In Diffusion, the U-Net takes a noisy image and (optionally) a time step and text embedding.
*   It outputs the predicted noise to be subtracted.
*   The multi-scale nature of U-Net allows it to attend to both global structure (low resolution) and fine details (high resolution).
