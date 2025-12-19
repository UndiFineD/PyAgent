# 3D Generation

Creating 3D assets (meshes, textures) is the bottleneck of the gaming and movie industry. AI is automating this pipeline.

## 1. Representations

*   **Mesh**: Vertices and faces. Standard for GPUs, but hard for Neural Networks to generate (topology issues).
*   **Voxel**: 3D pixels (Minecraft blocks). Easy for CNNs (3D Conv), but memory expensive ($N^3$).
*   **Point Cloud**: A list of (x, y, z) coordinates. Sparse and efficient, but lacks surface definition.
*   **Implicit Functions (NeRF)**: A neural network $F(x, y, z) \rightarrow (Color, Density)$. Infinite resolution, but slow to render.

## 2. NeRF (Neural Radiance Fields)

*   **Input**: A set of 2D photos of an object from different angles.
*   **Training**: Train a small MLP to predict the color of any point in 3D space such that it matches the photos when "ray-traced."
*   **Result**: A photorealistic 3D representation that can be viewed from any angle.

## 3. Gaussian Splatting

The successor to NeRF.
*   Instead of a neural network, represent the scene as millions of 3D Gaussians (blobs).
*   **Rasterization**: These blobs can be projected onto the screen instantly.
*   **Speed**: Real-time rendering (60 FPS) vs. NeRF's seconds-per-frame.

## 4. Text-to-3D (DreamFusion)

*   **SDS (Score Distillation Sampling)**: Use a 2D Text-to-Image model (Stable Diffusion) to guide the optimization of a 3D NeRF.
*   "Does this view look like a 'blue frog'? No? Adjust the 3D model."
*   Repeat for all angles until the 3D model looks like a blue frog from every side.
