# Implicit Neural Representations (INRs)

Traditionally, signals (images, audio, 3D shapes) are represented discretely:
- **Images**: Grid of pixels.
- **Audio**: Sequence of samples.
- **3D**: Voxel grids or Point clouds.

INRs (or Coordinate-based Networks) represent a signal as a **continuous function** parameterized by a neural network (usually an MLP).
$$ f(x, y, z) \rightarrow (r, g, b, \sigma) $$
The network maps coordinates to values.

## 1. NeRF (Neural Radiance Fields)

The most famous application of INRs.
- **Input**: 3D coordinate $(x, y, z)$ and viewing direction $(\theta, \phi)$.
- **Output**: Color $(r, g, b)$ and density $\sigma$.
- **Rendering**: To render an image, we shoot rays through the scene and integrate the color/density along the ray (Volume Rendering).

## 2. The Spectral Bias Problem

Standard MLPs with ReLU activations are terrible at learning high-frequency details (fine textures). They tend to learn low-frequency (blurry) functions first.
This is known as **Spectral Bias**.

## 3. Solutions

### Fourier Features
Mapping the input coordinates to a higher-dimensional space using sine/cosine functions before passing them to the MLP allows it to learn high frequencies.
$$ \gamma(v) = [\sin(2\pi v), \cos(2\pi v), \dots] $$

### SIREN (Sinusoidal Representation Networks)
Instead of using ReLU, SIREN uses the **Sine** activation function for every layer.
$$ \phi(x) = \sin(w_0 x + b) $$
- **Derivatives**: The derivative of a sine is a cosine (another sine). This means SIRENs can model not just the signal, but its derivatives (gradients, Laplacians) accurately.
- **Application**: Solving partial differential equations (PDEs) and modeling complex physical fields.

## 4. Benefits

- **Infinite Resolution**: Since the function is continuous, you can query it at any resolution (zoom in infinitely).
- **Compression**: A 1MB network can store a complex 3D scene that would take gigabytes as a voxel grid.
- **Differentiable**: The entire representation is differentiable, allowing for inverse rendering and optimization.

## Summary

INRs are revolutionizing Computer Graphics and Scientific Computing by treating data as functional equations rather than discrete arrays.
