# Multi-Agent Reinforcement Learning (MARL)

## What is MARL?
Standard Reinforcement Learning (RL) involves a single agent interacting with a static environment. **Multi-Agent Reinforcement Learning (MARL)** involves multiple agents interacting with the environment *and* each other.

In MARL, the environment is **non-stationary** from the perspective of any single agent, because the other agents are also learning and changing their policies simultaneously.

## Types of Interactions

### 1. Cooperative (Team)
*   **Goal**: All agents share a common reward or goal. They must learn to collaborate.
*   **Examples**: A swarm of drones fighting a fire; warehouse robots coordinating to move packages; players in a MOBA game (on the same team).
*   **Challenge**: **Credit Assignment**. When the team succeeds, which agent's action was responsible?

### 2. Competitive (Zero-Sum)
*   **Goal**: One agent's gain is another's loss.
*   **Examples**: Chess, Go, StarCraft (1v1), Poker.
*   **Concept**: **Nash Equilibrium**. A state where no player can improve their outcome by changing their strategy alone, assuming other players keep theirs constant.

### 3. Mixed (General Sum)
*   **Goal**: Agents have their own self-interested goals which might align or conflict.
*   **Examples**: Self-driving cars in traffic (everyone wants to get home fast and safe, but they compete for road space).

## Key Algorithms & Approaches

### Centralized Training, Decentralized Execution (CTDE)
*   **Training**: The learning algorithm has access to the global state and all agents' actions (the "God view").
*   **Execution**: During deployment, each agent acts based only on its own local observations.
*   **Algorithms**:
    *   **QMIX / VDN**: Decomposes a global team reward into individual agent utilities.
    *   **MADDPG (Multi-Agent Deep Deterministic Policy Gradient)**: Extends DDPG to multi-agent settings using a centralized critic and decentralized actors.

### Independent Learning (IL)
*   Each agent treats other agents as part of the environment.
*   **Pros**: Simple to implement (just run PPO on each agent).
*   **Cons**: Often fails because the environment is unstable (non-stationary).

## Challenges
*   **Scalability**: The joint state-action space grows exponentially with the number of agents.
*   **Communication**: Learning *how* to communicate (sending messages) between agents to coordinate.
*   **Lazy Agent Problem**: In cooperative settings, one agent might learn to do nothing if the other agents are doing all the work and the team still gets the reward.
