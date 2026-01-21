# Deep Q-Networks (DQN)

## Overview
**Deep Q-Networks (DQN)** combine Q-Learning with Deep Neural Networks. Instead of using a table to store Q-values (which is impossible for high-dimensional state spaces like images), DQN uses a neural network to *approximate* the Q-function.

## The Breakthrough: Atari Games (2013/2015)
DeepMind (now Google DeepMind) demonstrated an agent that could learn to play Atari 2600 games (Breakout, Pong, Space Invaders) directly from raw pixel inputs, achieving superhuman performance.

## Key Innovations
Training a neural network with standard Q-Learning is unstable. DQN introduced two key techniques to stabilize training:

### 1. Experience Replay
*   **Problem**: In RL, consecutive samples are highly correlated (e.g., video frames). Neural networks assume independent and identically distributed (i.i.d.) data.
*   **Solution**: Store the agent's experiences $(s_t, a_t, r_t, s_{t+1})$ in a replay buffer. During training, sample a random *minibatch* of experiences from the buffer. This breaks the correlation between consecutive samples.

### 2. Target Networks
*   **Problem**: In the Bellman equation, the target value depends on the same network parameters we are trying to update ($Q(s, a; \theta)$). This is like chasing a moving target.
*   **Solution**: Use a separate "Target Network" with parameters $\theta^-$ that are frozen for a fixed number of steps.
    *   Target: $r + \gamma \max_{a'} Q(s', a'; \theta^-)$
    *   Prediction: $Q(s, a; \theta)$
    *   Every $C$ steps, update $\theta^- \leftarrow \theta$.

## Architecture
*   **Input**: Stack of 4 consecutive frames (to capture motion).
*   **Network**: Convolutional Neural Network (CNN).
*   **Output**: Q-values for each possible action (joystick directions, button press).

## Impact
DQN proved that deep learning could be successfully applied to reinforcement learning, launching the field of **Deep Reinforcement Learning (Deep RL)**.
