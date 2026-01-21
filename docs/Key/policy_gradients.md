# Policy Gradients

## Overview
**Policy Gradient** methods are a class of Reinforcement Learning algorithms that optimize the policy directly, rather than learning a value function (like Q-Learning).

## Value-Based vs. Policy-Based
*   **Value-Based (e.g., DQN)**: Learn a Q-function $Q(s, a)$ and pick the action with the highest value. The policy is deterministic (or $\epsilon$-greedy).
*   **Policy-Based**: Learn a policy function $\pi_\theta(a|s)$ that outputs a probability distribution over actions. We sample an action from this distribution.

## Advantages
1.  **Stochastic Policies**: Can learn optimal stochastic policies (e.g., in Rock-Paper-Scissors, you want to be random).
2.  **Continuous Action Spaces**: Can handle continuous outputs (e.g., robot arm torque) naturally, whereas Q-learning requires discretization.
3.  **Convergence**: Often have better convergence properties.

## The REINFORCE Algorithm
The simplest policy gradient algorithm is **REINFORCE** (Monte Carlo Policy Gradient).

### The Intuition
*   Run an episode.
*   If the episode resulted in a high reward, increase the probability of the actions taken.
*   If the episode resulted in a low reward, decrease the probability.

### The Gradient Update
The update rule is derived from the **Policy Gradient Theorem**:

$$\nabla_\theta J(\theta) \approx \sum_{t=0}^{T} \nabla_\theta \log \pi_\theta(a_t | s_t) \cdot G_t$$

Where:
*   $\nabla_\theta J(\theta)$: Gradient of the expected return.
*   $\log \pi_\theta(a_t | s_t)$: The "score function" (direction to move parameters to make action $a_t$ more likely).
*   $G_t$: The return (cumulative reward) from time step $t$.

## Challenges
*   **High Variance**: The gradient estimates can be very noisy, leading to unstable training.
*   **Sample Inefficiency**: Requires a lot of data because it throws away data after every update (on-policy).

## Improvements
To reduce variance, we often subtract a **Baseline** (usually the Value function $V(s)$) from the return $G_t$. This leads to **Actor-Critic** methods, where we learn both a Policy (Actor) and a Value function (Critic).
