# Multi-Task Learning (MTL)

Training a single model to perform multiple tasks simultaneously.

## 1. Why?

*   **Inductive Bias**: Learning Task A helps Task B. (e.g., Learning to detect "Cars" helps the model understand "Roads" for lane detection).
*   **Regularization**: Prevents overfitting to a single task. The model must find a representation that is general enough for all tasks.
*   **Efficiency**: One model for 10 tasks is cheaper to deploy than 10 separate models.

## 2. Architectures

*   **Hard Parameter Sharing**:
    *   Shared "Backbone" (Encoder) for all tasks.
    *   Task-specific "Heads" (Decoders/Classifiers).
    *   Most common approach (e.g., Tesla Autopilot: One backbone, heads for Lane Lines, Traffic Lights, Objects).
*   **Soft Parameter Sharing**:
    *   Each task has its own model.
    *   Parameters are constrained to be similar (regularized distance).

## 3. Challenges

*   **Negative Transfer**: When Task A hurts Task B. (e.g., Learning to classify "Indoor vs. Outdoor" might conflict with "Day vs. Night" if the features are contradictory).
*   **Task Balancing**: If Task A has 1M examples and Task B has 1k, the model will ignore Task B. Requires careful weighting of Loss Functions.
