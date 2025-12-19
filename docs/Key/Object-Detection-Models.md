# Object Detection Models

## Overview
**Object Detection** goes beyond image classification (what is in the image?) to answer: **what** is where? It involves drawing a bounding box around each object and assigning a class label.

## Two-Stage Detectors (The R-CNN Family)
These models first propose regions of interest (RoIs) and then classify them. They are generally more accurate but slower.
1.  **R-CNN (2014)**: Uses Selective Search to propose regions, then runs a CNN on each. Very slow.
2.  **Fast R-CNN (2015)**: Runs the CNN on the whole image once, then extracts features for each region (RoI Pooling). Much faster.
3.  **Faster R-CNN (2015)**: Replaces Selective Search with a **Region Proposal Network (RPN)**, making the entire pipeline end-to-end trainable. This is still a gold standard for accuracy.

## One-Stage Detectors
These models skip the region proposal step and predict bounding boxes and classes directly from the image in a single pass. They are faster but historically less accurate (though the gap has closed).
1.  **YOLO (You Only Look Once)**: Divides the image into a grid. Each cell predicts bounding boxes and probabilities. Extremely fast (real-time).
2.  **SSD (Single Shot MultiBox Detector)**: Predicts boxes from feature maps at multiple scales (to handle small and large objects).
3.  **RetinaNet**: Introduced **Focal Loss** to solve the class imbalance problem (too many background boxes vs. few object boxes), allowing one-stage detectors to match two-stage accuracy.

## Metrics
*   **IoU (Intersection over Union)**: Measures overlap between predicted and ground truth boxes.
*   **mAP (mean Average Precision)**: The standard metric, calculating the area under the Precision-Recall curve for all classes.
