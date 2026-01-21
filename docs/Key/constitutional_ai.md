# Constitutional AI (CAI)

Constitutional AI is a method developed by Anthropic to align AI systems using a set of principles (a "constitution") rather than relying solely on human feedback (RLHF). It aims to make the alignment process more scalable, transparent, and safer.

## 1. The Problem with RLHF

Standard RLHF (Reinforcement Learning from Human Feedback) has bottlenecks:
- **Scalability**: Requires massive amounts of human labor to label preferences.
- **Consistency**: Humans disagree, get tired, or have biases.
- **Safety**: Humans have to read toxic outputs to label them as "bad."

## 2. The CAI Process

CAI splits the process into two phases:

### Phase 1: Supervised Learning (Critique & Revision)
1. **Generate**: The model generates a response to a prompt (which might be harmful).
2. **Critique**: The model is asked to critique its own response based on the Constitution.
   - *Prompt*: "Critique this response based on the principle: 'Please choose the response that is most helpful, honest, and harmless.'"
3. **Revise**: The model rewrites the response to address the critique.
4. **Finetune**: The model is finetuned on these revised (safer) responses (SL-CAI).

### Phase 2: Reinforcement Learning (RLAIF)
1. **Generate Pairs**: The model generates two responses to a prompt.
2. **AI Feedback**: A "Feedback Model" (the model itself or another AI) evaluates the pair based on the Constitution and picks the better one.
3. **Train**: A Reward Model is trained on these AI-generated preferences.
4. **PPO**: The main model is optimized against this Reward Model using PPO (Proximal Policy Optimization).

## 3. The Constitution

The "Constitution" is simply a list of natural language instructions.
- *Example*: "Please choose the response that is most respectful and avoids stereotypes."
- *Example*: "Choose the response that sounds most like a helpful assistant."

## 4. Benefits

- **RLAIF (RL from AI Feedback)**: Removes the human bottleneck.
- **Transparency**: The values are explicitly written in the Constitution, not hidden in the aggregate preferences of crowd workers.
- **Harmlessness**: Humans don't have to read toxic outputs during training.

## Summary

Constitutional AI represents a shift from "Alignment by Labeling" to "Alignment by Principles," allowing us to scale safety measures alongside model capabilities.
