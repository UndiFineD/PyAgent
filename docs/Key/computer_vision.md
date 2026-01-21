# Computer Vision (CV)

Beyond generating images, Computer Vision is about *understanding* them.

## 1. Core Tasks

*   **Classification**: "Is this a cat?" (ResNet, EfficientNet).
*   **Object Detection**: "Where are the cats?" Returns Bounding Boxes. (YOLO, Faster R-CNN).
*   **Semantic Segmentation**: "Which pixels belong to the cat?" (UNet, Mask R-CNN).
*   **Instance Segmentation**: "Which pixels belong to *this specific* cat?" (Distinguishing between two overlapping cats).

## 2. Modern Architectures

*   **YOLO (You Only Look Once)**: The standard for real-time object detection. Treats detection as a single regression problem rather than a classification of region proposals.
*   **ViT (Vision Transformer)**: Applying Transformers to images by chopping them into 16x16 patches (tokens). Outperforms CNNs on massive datasets.
*   **SAM (Segment Anything Model)**: A foundation model from Meta that can "cut out" any object in an image given a simple prompt (click or box).

## 3. Specialized Tasks

*   **OCR (Optical Character Recognition)**: Reading text from images.
*   **Pose Estimation**: Detecting human joints (elbows, knees) for motion tracking.
*   **Depth Estimation**: Predicting the distance of objects from a single 2D image.
