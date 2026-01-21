# Neural Cellular Automata (NCA)

Cellular Automata (like Conway's Game of Life) are systems where a grid of cells evolves based on local rules.
**Neural Cellular Automata** replace the hand-coded rules with a Neural Network (usually a CNN) that is learned via backpropagation.

## 1. Morphogenesis

The most famous NCA paper is "Growing Neural Cellular Automata" (Mordvintsev et al., 2020).
- **Goal**: Grow a target image (e.g., a lizard) starting from a single seed pixel.
- **Rule**: Every cell runs the *same* small neural network to decide its new state based on its neighbors.
- **Robustness**: If you damage the image (erase half the lizard), the NCA "heals" itself, regenerating the missing parts. This mimics biological regeneration.

## 2. Architecture

- **State**: A grid of size $H \times W \times C$ (e.g., 16 channels: RGB + Hidden).
- **Perception**: A fixed kernel (Sobel filter) senses the gradient of neighbors.
- **Update**: A small MLP takes the perception vector and outputs an update $\Delta S$.
- **Stochasticity**: Updates are applied stochastically (to simulate asynchronous biological processes).

## 3. Applications

- **Texture Synthesis**: Generating infinite textures.
- **Self-Repairing Systems**: Creating robust agents that can survive damage.
- **Differentiable Physics**: Modeling fluid dynamics or reaction-diffusion systems.

## Summary

NCAs bridge the gap between Deep Learning and **Artificial Life**, showing how complex global patterns can emerge from simple, learnable local rules.
