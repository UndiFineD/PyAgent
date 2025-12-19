# Decision Transformers

Decision Transformers represent a paradigm shift in Reinforcement Learning (RL). Instead of using traditional RL algorithms (like PPO or DQN) that estimate value functions or gradients, Decision Transformers treat RL as a **Sequence Modeling** problem, solvable with standard Transformers (like GPT).

## 1. The Core Idea: Trajectory as a Sequence

In standard RL, an agent interacts with an environment in a loop: State $\rightarrow$ Action $\rightarrow$ Reward.
Decision Transformers flatten this history into a sequence of tokens:
$$ \tau = (R_1, s_1, a_1, R_2, s_2, a_2, \dots) $$
Where:
- $R_t$: The **Return-to-Go** (the total future reward expected from this point).
- $s_t$: The state.
- $a_t$: The action.

## 2. Training: Offline RL

The model is trained using **Supervised Learning** (Cross-Entropy Loss) on a dataset of offline trajectories (recorded gameplay or robot logs).
- **Input**: Past states, past actions, and the *desired* future reward.
- **Output**: The next action $a_t$.

It learns the conditional probability:
$$ P(a_t | R_t, s_t, a_{t-1}, \dots) $$
"Given that I am in this state and I *want* to achieve this much reward, what action should I take?"

## 3. Inference: Conditioning on Success

To make the agent perform well, you simply prompt it with a high desired reward.
- **Prompt**: "Return-to-Go = 1000 (High Score)"
- **Model**: Generates the actions that are most likely to lead to that score, based on its training data.

## 4. Advantages over Standard RL

- **Stability**: Uses standard Transformer training (stable, well-understood) instead of RL training (notoriously unstable, sensitive to hyperparameters).
- **Long-Term Credit Assignment**: Transformers (via Attention) are excellent at connecting distant events (e.g., a key picked up at step 10 opens a door at step 500). Standard RL struggles with this.
- **Data Efficiency**: Can leverage massive offline datasets without needing to interact with a simulator during training.

## Summary

Decision Transformers prove that if you have enough data, you don't need explicit "reinforcement" algorithms. You can just model the distribution of successful behaviors and ask the model to generate them.
