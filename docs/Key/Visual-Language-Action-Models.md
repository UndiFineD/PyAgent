# Visual-Language-Action (VLA) Models

Traditional robotics pipelines are modular: Perception -> State Estimation -> Planning -> Control. VLA models replace this entire stack with a single end-to-end Transformer model that takes images and text as input and outputs robot actions.

## The Concept
Just as LLMs are trained on internet text to predict the next word, VLAs are trained on internet text, images, and *robot trajectories* to predict the next action.

## Key Models

### 1. RT-2 (Robotic Transformer 2) - Google DeepMind
*   **Architecture**: A Vision-Language Model (VLM) fine-tuned to output actions.
*   **Tokenization**: Robot actions (move arm x, y, z, rotate gripper) are discretized into text tokens (e.g., "128", "255").
*   **Input**: Image of the scene + Command ("Pick up the strawberry").
*   **Output**: A sequence of tokens representing the motion.
*   **Breakthrough**: It exhibits **Semantic Generalization**. If trained on "pick up apple" and knows what a "spiderman figure" looks like from web data, it can "pick up spiderman" without ever seeing a robot do it.

### 2. PaLM-E (PaLM-Embodied)
*   **Architecture**: A massive 562B parameter model combining PaLM (LLM) and ViT (Vision).
*   **Multimodal**: It processes visual, continuous state vectors, and text in the same embedding space.
*   **Reasoning**: It can perform high-level planning ("Bring me the rice chips from the drawer") by breaking it down into low-level steps.

## Challenges
*   **Data Scarcity**: Unlike text, there is no "internet of robot data". Collecting real-world robot trajectories is slow and expensive.
*   **Sim2Real Gap**: Models trained in simulation often fail in the real world due to physics discrepancies.
*   **Latency**: Running a 50B+ parameter model for real-time control (10-20Hz) is computationally prohibitive.
