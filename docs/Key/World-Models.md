# World Models

In Reinforcement Learning (RL), an agent usually learns by trial and error (Model-Free). **World Models** (Model-Based RL) take a different approach: the agent learns a simulation of the environment and plans inside its "dream" before acting in reality.

## 1. The Concept

Humans don't try to jump off a cliff to see if it hurts. We have an internal mental model of physics that predicts "Jump -> Fall -> Pain."
World Models try to build this internal simulator.
*   **Observation**: The agent sees the current state ($s_t$).
*   **Prediction**: The model predicts the next state ($s_{t+1}$) given an action ($a_t$).

## 2. The Architecture (Dreamer)

A typical World Model (like DreamerV3) has three parts:
1.  **Encoder (VAE)**: Compresses the visual input (pixels) into a compact latent state.
2.  **Dynamics Model (RNN/SSM)**: Predicts how the latent state changes over time. This is the "Simulator."
3.  **Controller (Policy)**: Uses the simulator to imagine future trajectories and chooses the action that maximizes reward.

## 3. JEPA (Joint Embedding Predictive Architecture)

Yann LeCun's proposal for World Models.
*   **Problem**: Predicting every pixel (Generative Model) is too hard and unnecessary. You don't need to predict the exact texture of the grass to know a car is coming.
*   **Solution**: Predict in **Latent Space**. The model predicts the *representation* of the future state, not the pixels.
*   **I-JEPA / V-JEPA**: Implementations for Images and Video. They learn semantic features by predicting missing parts of the input in abstract space.

## 4. Benefits

*   **Sample Efficiency**: An agent can learn millions of times faster by "dreaming" (simulating) experiences than by acting in the real world (which is slow and dangerous).
*   **Planning**: The agent can reason about long-term consequences.

## 5. LLMs as World Models?

There is a debate: Do LLMs just memorize statistics, or do they build an internal World Model (e.g., a map of New York, a model of a chess board)? Evidence suggests that as they scale, they do emerge rudimentary world models (e.g., Othello-GPT).
