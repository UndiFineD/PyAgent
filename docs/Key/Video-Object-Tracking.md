# Video Object Tracking

## Overview
**Object Tracking** involves locating an object in successive frames of a video.
*   **Single Object Tracking (SOT)**: Initialize one object in frame 1 and follow it.
*   **Multi-Object Tracking (MOT)**: Detect and track all objects of a certain class (e.g., all cars).

## Tracking by Detection
The standard paradigm for MOT:
1.  **Detection**: Run an object detector (YOLO) on every frame.
2.  **Data Association**: Match the detections in the current frame to the tracks from the previous frame.

## Algorithms

### SORT (Simple Online and Realtime Tracking)
*   **Kalman Filter**: Predicts the future position of a track based on its velocity.
*   **IoU Matching**: Matches new detections to predicted tracks based on spatial overlap (Intersection over Union).
*   **Pros**: Extremely fast.
*   **Cons**: Fails if objects move too fast or are occluded (ID switching).

### DeepSORT
*   **Appearance Features**: Adds a "Re-ID" (Re-Identification) neural network to extract a visual feature vector for each detection.
*   **Matching**: Uses both motion (Kalman Filter) and appearance (Cosine distance of feature vectors) to match tracks.
*   **Pros**: Robust to occlusions (can re-identify an object after it reappears).

### ByteTrack
*   **Innovation**: Instead of discarding low-confidence detections (which might be occluded objects), it associates high-confidence detections first, and then tries to match the remaining tracks to low-confidence detections.
*   **Result**: State-of-the-art performance on MOT benchmarks.
