# Embodied AI (Robotics)

**Embodied AI** is the intersection of Computer Vision, NLP, and Robotics. It deals with agents that have a physical body (or a simulation of one) and interact with the world.

## 1. The Challenge: Moravec's Paradox

"It is comparatively easy to make computers exhibit adult level performance on intelligence tests or playing checkers, and difficult or impossible to give them the skills of a one-year-old when it comes to perception and mobility."
*   Reasoning is high-level (abstract).
*   Movement is low-level (continuous, noisy, physics-dependent).

## 2. Sim2Real

Training robots in the real world is slow and expensive (robots break).
*   **Simulation**: Train the agent in a physics engine (MuJoCo, Isaac Gym) where it can run millions of steps per second.
*   **Domain Randomization**: Randomize the friction, gravity, colors, and lighting in the simulation.
*   **Transfer**: If the agent can handle the randomized simulation, the real world just looks like "another random variation" to it.

## 3. Visual-Language-Action (VLA) Models

The "LLM for Robots."
*   **RT-1 / RT-2 (Robotics Transformer)**: Google's models.
*   **Input**: Image (Camera) + Text Instruction ("Pick up the apple").
*   **Output**: Robot Actions (x, y, z, gripper_open).
*   **Training**: Trained on massive datasets of robot demonstrations.
*   **Generalization**: Because it uses a pre-trained LLM/VLM backbone, it can understand "Pick up the *extinct animal*" (dinosaur toy) even if it never saw that specific toy in training.

## 4. Foundation Models for Control

Instead of training a policy from scratch (RL), we use Foundation Models.
*   **Eureka (NVIDIA)**: Uses GPT-4 to write the *Reward Function* for the robot to learn from.
*   **VoxPoser**: Uses LLMs to generate 3D value maps ("affordances") to guide the robot's motion planning.
