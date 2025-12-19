# Video Understanding

Video understanding extends computer vision by adding the dimension of **time**. It's not just about "what is in this frame?" but "what is happening over time?"

## 1. The Challenge: The Temporal Dimension

- **Data Volume**: Video is massive (30-60 frames per second). Processing every frame with a heavy CNN is computationally prohibitive.
- **Temporal Context**: An image of a person holding a cup could be "drinking" or "putting it down." Only the sequence of frames reveals the action.

## 2. Key Architectures

### 3D CNNs (C3D, I3D)
- **Concept**: Extend 2D convolutions to 3D ($Height \times Width \times Time$).
- **Mechanism**: The kernel slides across space and time, capturing motion patterns directly.
- **Pros/Cons**: Very effective but computationally expensive.

### Two-Stream Networks
- **Stream 1 (Spatial)**: Processes a single frame (RGB) to identify objects/scenes.
- **Stream 2 (Temporal)**: Processes "Optical Flow" (motion vectors between frames) to identify movement.
- **Fusion**: The outputs of both streams are combined.

### Video Transformers (TimeSformer, ViViT)
- **Concept**: Apply Vision Transformers (ViT) to video.
- **Space-Time Attention**:
    - **Joint Space-Time**: Attend to all patches in all frames (expensive).
    - **Divided Space-Time**: First attend to spatial patches within a frame, then attend to the same patch across time frames (efficient).

### VideoMAE (Masked Autoencoders)
- **Concept**: Self-supervised learning for video.
- **Mechanism**:
    1.  Mask out a huge percentage (e.g., 90%) of the video patches in space and time.
    2.  Train the model to reconstruct the missing pixels.
- **Why it works**: Video is highly redundant (background doesn't change much). Masking 90% forces the model to learn high-level semantic understanding of motion to fill in the gaps.

## 3. Tasks

- **Action Recognition**: Classifying a short clip (e.g., "Playing Tennis").
- **Temporal Action Localization**: Finding the start and end times of an action in a long video.
- **Video Captioning**: Generating a text description of a video event.
- **Video QA**: Answering questions about a video ("What color was the car that turned left?").

## Summary

| Architecture | Mechanism | Strength |
| :--- | :--- | :--- |
| **3D CNN** | Volumetric Conv | Captures fine-grained motion |
| **Two-Stream** | RGB + Optical Flow | Explicitly models motion |
| **Video Transformer** | Self-Attention | Long-range dependencies |
| **VideoMAE** | Masked Reconstruction | Data-efficient self-supervised learning |
