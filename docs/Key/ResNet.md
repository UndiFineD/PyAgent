# ResNet (Residual Networks)

## Overview
**ResNet** (Residual Network), introduced by Microsoft Research in 2015 (He et al.), is one of the most influential architectures in Deep Learning history. It solved the problem of training very deep neural networks.

## The Problem: Vanishing Gradients & Degradation
Before ResNet, adding more layers to a network often made performance *worse*, not better.
1.  **Vanishing/Exploding Gradients**: As gradients backpropagate through many layers, they tend to shrink to zero or explode to infinity, making training impossible.
2.  **Degradation Problem**: Even with normalized initialization, deeper networks had higher training error than shallower ones. This suggested the solvers couldn't find the identity mapping (i.e., it's hard for a layer to learn to "do nothing" and just pass the data through).

## The Solution: Residual Blocks
ResNet introduced the **Residual Block** (or Skip Connection / Shortcut Connection).

Instead of trying to learn the underlying mapping $H(x)$ directly, the network tries to learn the **residual** mapping $F(x) = H(x) - x$.
The original mapping is then reconstructed as $H(x) = F(x) + x$.

### The Skip Connection
*   Input $x$ is added to the output of the weight layers: `Output = Activation(Layers(x) + x)`.
*   This creates a "highway" for gradients to flow backward without being attenuated by weight multiplications.
*   If the optimal function is the identity mapping, the weights can simply be driven to zero ($F(x) \to 0$), leaving $H(x) = x$.

## Architecture Variants
*   **ResNet-18 / ResNet-34**: Use basic residual blocks (two 3x3 convolutions).
*   **ResNet-50 / ResNet-101 / ResNet-152**: Use **Bottleneck Blocks** (1x1, 3x3, 1x1 convolutions) to reduce computational cost while increasing depth.

## Impact
*   Won the ILSVRC 2015 classification task with 3.57% error (beating human performance).
*   The concept of skip connections became a standard building block for almost all subsequent deep networks (including Transformers and U-Nets).
