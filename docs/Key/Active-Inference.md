# Active Inference

Active Inference is a theoretical framework proposed by neuroscientist Karl Friston. It posits a unified theory for how biological brains (and potentially artificial agents) perceive and act. It is distinct from Reinforcement Learning.

## 1. The Free Energy Principle

The core axiom is that all self-organizing systems (like life) must resist the natural tendency towards disorder (entropy).
- **Surprise**: In information theory, "surprise" is high entropy. A living thing wants to minimize surprise (e.g., a fish is surprised if it finds itself on land; it will die).
- **Variational Free Energy**: An upper bound on surprise. Minimizing Free Energy $\approx$ Minimizing Surprise.

## 2. Perception vs. Action

To minimize surprise (prediction error), an agent has two choices:

1.  **Perception (Change your Mind)**: Update your internal model of the world to match the sensory data.
    - *Example*: You see a dark shape. You predict it's a bear. It doesn't move. You update your model: "It's a rock." Surprise minimized.
2.  **Action (Change the World)**: Act on the world to make the sensory data match your internal prediction.
    - *Example*: You feel cold (sensory data). Your model predicts "I should be warm." There is a mismatch (error). You put on a coat. Now you feel warm. Surprise minimized.

## 3. Comparison with Reinforcement Learning

| Feature | Reinforcement Learning (RL) | Active Inference |
| :--- | :--- | :--- |
| **Goal** | Maximize Reward | Minimize Free Energy (Surprise) |
| **Mechanism** | Value Functions / Policy Gradients | Predictive Coding / Belief Updating |
| **Exploration** | Added noise (epsilon-greedy) | Intrinsic: "Epistemic Value" (Resolving uncertainty reduces expected free energy) |
| **Philosophy** | Behaviorist (Stimulus-Response) | Bayesian / Enactivist (Model-Based) |

## 4. Why it Matters for AI

- **Unified Objective**: It combines perception, action, and learning into a single objective function (Free Energy).
- **Robustness**: Active Inference agents are naturally curious (to resolve uncertainty) and robust to noise.
- **Biologically Plausible**: It offers a path to AGI that mimics the energy-efficiency and adaptability of the brain.
