# YOLO (You Only Look Once)

## Overview
**YOLO** is a family of real-time Object Detection models. Before YOLO, detection systems (like R-CNN) were slow because they used a two-step process: (1) Propose regions, (2) Classify regions. YOLO reframed detection as a **single regression problem**, making it incredibly fast (45+ FPS).

## How It Works
1.  **Grid Division**: The image is divided into an $S \times S$ grid.
2.  **Bounding Boxes**: Each grid cell predicts $B$ bounding boxes and confidence scores.
3.  **Class Probabilities**: Each cell also predicts the class probabilities (e.g., "Dog", "Car").
4.  **Non-Max Suppression (NMS)**: Removes duplicate boxes for the same object, keeping only the one with the highest confidence.

## Evolution

### 1. YOLOv1 (2015)
*   **Innovation**: Single neural network (Darknet) predicts everything in one pass.
*   **Limitation**: Struggled with small objects and clustered objects.

### 2. YOLOv2 & YOLO9000 (2016)
*   **Anchor Boxes**: Used pre-defined box shapes (priors) to improve stability.
*   **Batch Norm**: Added to all layers.

### 3. YOLOv3 (2018)
*   **Multi-Scale Prediction**: Detects objects at 3 different scales (like Feature Pyramid Networks), drastically improving small object detection.

### 4. YOLOv4 & v5 (2020)
*   **Bag of Freebies**: Data augmentation techniques (Mosaic, CutMix) that improve accuracy without increasing inference cost.
*   **Bag of Specials**: Architectural tweaks (Mish activation, CSPNet).

### 5. YOLOv8 (Ultralytics - 2023)
*   **Anchor-Free**: Removed anchor boxes for simpler logic.
*   **Task Unified**: Supports Detection, Segmentation, Classification, and Pose Estimation in one framework.

## Impact
YOLO enabled real-time AI applications on edge devices:
*   **Autonomous Driving**: Detecting pedestrians and signs.
*   **Security Cameras**: Intruder detection.
*   **Sports Analytics**: Tracking players on a field.
