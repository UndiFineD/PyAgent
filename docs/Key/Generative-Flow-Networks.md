# Generative Flow Networks (GFlowNets)

Proposed by Yoshua Bengio, GFlowNets are a probabilistic framework for generating compositional objects (like molecules, graphs, or causal structures) where the probability of generating an object is proportional to a given reward.

## 1. The Problem: Sampling from Modes

In scientific discovery (e.g., drug design), we want to find molecules that bind well to a protein.
- **RL (PPO)**: Tends to find *one* high-reward solution and stick to it (mode collapse).
- **MCMC**: Can mix slowly between modes.
- **Goal**: We want to sample *diverse* high-reward candidates, not just the single best one.

## 2. The Water Flow Analogy

Imagine a network of pipes (a DAG - Directed Acyclic Graph).
- **Source**: Water enters at the start (empty state).
- **Sinks**: Water exits at various endpoints (finished objects).
- **Flow**: The amount of water flowing out of a sink should be proportional to the "Reward" of that object.

The GFlowNet learns a policy (how to split the water at each junction) such that the final distribution matches the reward landscape.

## 3. Training Objectives

### Trajectory Balance Loss
The most common loss function. It enforces that for any complete trajectory $\tau$:
$$ Z \cdot P_F(\tau) = R(x) \cdot P_B(\tau) $$
- $Z$: Total flow (partition function).
- $P_F$: Probability of choosing this path forward.
- $R(x)$: Reward of the final object.
- $P_B$: Probability of choosing this path backward (undoing the steps).

## 4. Applications

- **Drug Discovery**: Generating diverse molecular graphs that have high predicted binding affinity.
- **Causal Discovery**: Generating causal graphs that explain observed data.
- **Combinatorial Optimization**: Solving scheduling or chip design problems.

## Summary

GFlowNets sit somewhere between Reinforcement Learning and Generative Modeling. They are "RL for sampling," designed to explore the vast space of compositional objects and return a diverse set of high-value candidates.
