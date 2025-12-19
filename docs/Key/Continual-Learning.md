# Continual Learning (Lifelong Learning)

Standard machine learning assumes a static dataset. You train a model once, and it's done. **Continual Learning** addresses the reality of the world: data changes over time, and agents must learn new tasks without forgetting old ones.

## 1. The Core Problem: Catastrophic Forgetting

When a neural network trained on Task A is subsequently trained on Task B, it tends to drastically forget how to perform Task A.
- **Cause**: The weights optimized for Task A are overwritten to minimize the loss for Task B.
- **Goal**: Stability-Plasticity Dilemma. The model must be plastic enough to learn new things, but stable enough to preserve old knowledge.

## 2. Key Approaches

### Regularization-Based (Constraints)
Constrain the weight updates so they don't move too far from the solution for previous tasks.
- **Elastic Weight Consolidation (EWC)**:
    - Calculates the "importance" of each parameter for Task A (using the Fisher Information Matrix).
    - When training on Task B, adds a penalty term to the loss function that prevents important parameters from changing too much.
    - *Analogy*: "You can change the paint color (unimportant), but don't move the load-bearing walls (important)."

### Replay-Based (Memory)
Store a small subset of data from previous tasks and mix it with new data.
- **Experience Replay**: Keep a buffer of old examples. In every training step, mix new data with a random batch from the buffer.
- **Generative Replay**: Instead of storing raw data (privacy/storage issues), train a separate generative model (GAN/VAE) to *generate* examples of old tasks to rehearse.

### Architecture-Based (Expansion)
Dedicate different parts of the neural network to different tasks.
- **Progressive Neural Networks**: Freeze the columns of the network used for Task A. Add a new column for Task B, with lateral connections from A to B.
- **Parameter Isolation**: Use a mask to ensure Task B only updates neurons that were unused by Task A.

## 3. Scenarios

1.  **Task-Incremental**: The model is told which task it is performing (e.g., "Now classify dogs," "Now classify cars").
2.  **Domain-Incremental**: The task is the same, but the input distribution changes (e.g., "Classify digits," but the handwriting style changes over decades).
3.  **Class-Incremental**: The hardest scenario. The model must learn to distinguish between all classes seen so far, without being told which task ID the current input belongs to.

## Summary

| Approach | Mechanism | Pros | Cons |
| :--- | :--- | :--- | :--- |
| **Regularization (EWC)** | Penalty on weight changes | No extra memory needed | Performance degrades with many tasks |
| **Replay** | Re-training on old data | High accuracy | Privacy/Storage costs |
| **Architecture** | Growing the network | Zero forgetting | Model size grows indefinitely |
