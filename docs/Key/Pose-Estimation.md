# Pose Estimation

## Overview
**Pose Estimation** is the task of detecting the position and orientation of a person or object. In computer vision, it usually refers to **Human Pose Estimation**: detecting keypoints (joints like elbows, knees, shoulders) to construct a skeletal model.

## Approaches

### Top-Down
1.  **Detect Person**: Use an object detector (like YOLO) to find bounding boxes for all people.
2.  **Detect Keypoints**: Run a pose estimator on each cropped person image.
*   **Pros**: High accuracy.
*   **Cons**: Slow if there are many people (runtime scales linearly with the number of people).

### Bottom-Up (OpenPose)
1.  **Detect All Keypoints**: Find all "left elbows", "right knees", etc., in the entire image at once (using heatmaps).
2.  **Group Keypoints**: Use algorithms (like Part Affinity Fields) to connect the keypoints into valid skeletons.
*   **Pros**: Constant runtime regardless of the number of people. Real-time performance.
*   **Cons**: Can struggle with complex occlusions.

## MediaPipe (Google)
*   **Concept**: A cross-platform framework for building multimodal ML pipelines.
*   **BlazePose**: A lightweight pose estimation model designed for mobile devices. It infers 33 3D landmarks from a single frame.
*   **Usage**: Widely used in AR filters (Snapchat/TikTok), fitness apps, and gesture control.

## 3D Pose Estimation
Estimating the 3D coordinates $(x, y, z)$ of joints from a 2D image. This is an ill-posed problem (multiple 3D shapes can project to the same 2D image), solved by learning priors about human anatomy.
