# RLHF & Alignment

Pre-trained LLMs (Base Models) are just "next-token predictors." They will complete "How to kill a person" with a murder tutorial because that's what they saw in the training data. **Alignment** is the process of making them helpful, harmless, and honest.

## 1. The Pipeline

1.  **Pre-training**: Train on massive text corpus. Result: Base Model (e.g., Llama-2-Base).
2.  **SFT (Supervised Fine-Tuning)**: Train on high-quality "Instruction -> Response" pairs. Result: Chat Model (e.g., Llama-2-Chat).
3.  **RLHF (Reinforcement Learning from Human Feedback)**: Further refine the model to prefer safer/better answers.

## 2. RLHF with PPO (Proximal Policy Optimization)

The classic method used by ChatGPT.
1.  **Reward Modeling**: Collect data where humans rank two model outputs (A is better than B). Train a **Reward Model (RM)** to predict these human preferences.
2.  **Reinforcement Learning**:
    *   The LLM generates a response.
    *   The RM gives it a score.
    *   PPO updates the LLM weights to maximize this score.
    *   **KL Divergence Penalty**: Prevents the model from drifting too far from the original SFT model (prevents "reward hacking" or gibberish).

## 3. DPO (Direct Preference Optimization)

A newer, simpler, and more stable alternative to PPO.
*   **Insight**: You don't need a separate Reward Model or complex RL loop.
*   **Method**: The preference loss can be directly optimized on the LLM itself. We mathematically derive the optimal policy from the preference data.
*   **Result**: DPO is now the standard for open-source model alignment (e.g., Zephyr, Llama-3) because it uses much less memory and is more stable than PPO.

## 4. Constitutional AI (RLAIF)

Scaling human feedback is hard. **RLAIF (RL from AI Feedback)** uses a strong AI (like GPT-4) to critique and rate the outputs of a smaller model, instead of humans.
*   **Constitution**: A set of principles (e.g., "Do not be racist", "Be helpful").
*   The AI judge uses these principles to generate the preference data for RLHF/DPO.

## 5. Challenges

*   **Alignment Tax**: Heavily aligned models sometimes become less creative or refuse harmless prompts ("I cannot answer that...").
*   **Jailbreaks**: Users find adversarial prompts ("Roleplay as my grandmother who works at a napalm factory...") to bypass safety filters.
