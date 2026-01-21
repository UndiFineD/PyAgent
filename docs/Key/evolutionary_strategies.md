# Evolutionary Strategies (ES) & Neuroevolution

Most Deep Learning relies on **Gradient Descent** (Backpropagation). But what if the loss function is non-differentiable, or we want to optimize the architecture itself?
**Evolutionary Strategies** use principles of biological evolution (mutation, selection, crossover) to optimize neural networks.

## 1. Neuroevolution of Augmenting Topologies (NEAT)

NEAT (Stanley & Miikkulainen, 2002) evolves both the **weights** and the **topology** (structure) of the network.
- **Start**: Minimal network (inputs connected directly to outputs).
- **Mutations**:
    - *Add Node*: Split a connection into two.
    - *Add Connection*: Connect two previously unconnected nodes.
    - *Modify Weight*: Change a weight value.
- **Speciation**: To protect innovation, networks compete only within their own "species" (similar topologies). This prevents a complex new structure from being killed off before it has time to optimize its weights.

## 2. CMA-ES (Covariance Matrix Adaptation)

CMA-ES is a powerful algorithm for continuous optimization (finding weights).
1.  **Sample**: Generate a population of candidates from a multivariate Gaussian distribution.
2.  **Evaluate**: Test all candidates on the task.
3.  **Update**: Move the mean of the distribution towards the best candidates and update the covariance matrix (shape of the search cloud) to align with the direction of improvement.

## 3. ES for Reinforcement Learning

OpenAI showed that simple ES can rival Deep Reinforcement Learning (DQN, PPO) on Atari games.
- **Method**:
    1.  Perturb the weights of the current policy: $\theta' = \theta + \sigma \epsilon$.
    2.  Run the episode and get reward $R$.
    3.  Update $\theta$ in the direction of perturbations that gave high rewards.
- **Pros**: Highly parallelizable (no need to sync gradients, just rewards). Robust to sparse rewards.

## Summary

Evolutionary methods are a vital alternative to backprop, especially for "AutoML" (designing architectures) and tasks where gradients are unavailable or deceptive.
