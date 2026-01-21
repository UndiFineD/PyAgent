# 3D Reconstruction

## Overview
**3D Reconstruction** is the process of capturing the shape and appearance of real objects and creating a 3D model (mesh or point cloud) from 2D images.

## Photogrammetry / Structure from Motion (SfM)
*   **Concept**: If you take multiple photos of an object from different angles, you can triangulate the position of points in 3D space.
*   **Pipeline**:
    1.  **Feature Extraction**: Find keypoints (SIFT/ORB) in all images.
    2.  **Matching**: Find the same keypoints across different images.
    3.  **SfM**: Estimate the camera positions and a sparse 3D point cloud.
    4.  **MVS (Multi-View Stereo)**: Generate a dense point cloud.
    5.  **Meshing**: Convert points to a surface (Poisson Reconstruction).
*   **Tools**: COLMAP, Meshroom.

## NeRF (Neural Radiance Fields)
*   **Concept**: Instead of storing a mesh, represent the scene as a continuous function (a neural network) $F(x, y, z, \theta, \phi) \to (RGB, \sigma)$.
*   **Mechanism**: The network takes a 3D coordinate and viewing direction and outputs the color and density.
*   **Rendering**: Use **Volume Rendering** (ray marching) to generate new views.
*   **Pros**: Photorealistic quality, handles reflections/transparency better than meshes.
*   **Cons**: Slow to train and render (though Instant-NGP is fast).

## Gaussian Splatting (3DGS)
*   **Concept**: Represents the scene as a cloud of 3D Gaussians (blobs), each with position, covariance (shape), color, and opacity.
*   **Rendering**: Rasterizes these Gaussians onto the screen.
*   **Pros**: Real-time rendering (much faster than NeRF) with similar quality.
