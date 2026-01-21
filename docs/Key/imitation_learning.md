# Imitation Learning (IL)

Reinforcement Learning requires a reward function, which is often hard to design (Reward Engineering).
**Imitation Learning** skips the reward function and tries to learn a policy by mimicking an expert demonstrator.

## 1. Behavior Cloning (BC)

The simplest form of IL.
- **Data**: A dataset of (State, Action) pairs collected from an expert.
- **Training**: Train a classifier/regressor (Supervised Learning) to map State $\rightarrow$ Action.
- **Problem**: **Covariate Shift**. If the agent makes a small mistake, it enters a state it has never seen before (because the expert never made mistakes). The errors compound, and the agent crashes.

## 2. DAgger (Dataset Aggregation)

DAgger fixes Covariate Shift by iteratively collecting more data.
1.  Train a policy $\pi$ using BC on the expert data.
2.  Run $\pi$ in the environment to collect a new trajectory.
3.  Ask the **Expert** to label the actions for the states visited in this new trajectory (Correcting the agent's mistakes).
4.  Add this new data to the dataset and retrain.

## 3. Generative Adversarial Imitation Learning (GAIL)

Uses the GAN framework.
- **Generator**: The Agent (Policy).
- **Discriminator**: Tries to distinguish between the Agent's trajectory and the Expert's trajectory.
- The Agent is rewarded for fooling the Discriminator (making its behavior look like the expert's).

## Summary

Imitation Learning is crucial for tasks where "showing" is easier than "specifying" (e.g., driving a car, folding laundry).
