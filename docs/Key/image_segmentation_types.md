# Image Segmentation Types

## Overview
**Image Segmentation** is the process of partitioning an image into multiple segments (sets of pixels). Unlike object detection (boxes), segmentation provides pixel-perfect boundaries.

## 1. Semantic Segmentation
*   **Goal**: Classify *every pixel* in the image into a class (e.g., "road", "car", "sky").
*   **Key Characteristic**: It does **not** distinguish between different instances of the same class. All "car" pixels are colored the same, whether they belong to Car A or Car B.
*   **Architectures**: U-Net, DeepLab (using Atrous/Dilated Convolutions), SegNet.

## 2. Instance Segmentation
*   **Goal**: Detect and delineate each distinct object of interest (e.g., "Car #1", "Car #2", "Person #1").
*   **Key Characteristic**: It distinguishes between instances but usually ignores the background (stuff like "sky" or "grass").
*   **Architectures**: Mask R-CNN (extends Faster R-CNN by adding a mask prediction branch).

## 3. Panoptic Segmentation
*   **Goal**: The unification of Semantic and Instance segmentation.
*   **Task**: Assign a unique value `(class_id, instance_id)` to every pixel in the image.
    *   **Things** (countable objects like cars, people) have instance IDs.
    *   **Stuff** (amorphous regions like sky, road) share a single instance ID.
*   **Architectures**: Panoptic FPN, DETR (Detection Transformer) with segmentation heads.

## Applications
*   **Autonomous Driving**: Knowing exactly where the road ends and the sidewalk begins.
*   **Medical Imaging**: Segmenting tumors or organs from CT/MRI scans.
