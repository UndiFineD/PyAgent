# Reflection and Self-Correction

One of the most powerful capabilities of modern AI agents is the ability to critique their own outputs and improve them iteratively. This mimics human problem-solving: we rarely get the perfect answer on the first try; we draft, review, and revise.

## Core Concepts

### 1. Self-Refine
A simple iterative loop where the model generates an initial output, then critiques it, and then generates a refined output based on the critique.
*   **Prompt Structure**:
    1.  `Generate code to solve X.` -> Output 1
    2.  `Critique Output 1. Is it efficient? Is it correct?` -> Critique
    3.  `Rewrite Output 1 based on the Critique.` -> Output 2
*   **Benefit**: Often improves performance on reasoning and coding tasks without needing external verifiers.

### 2. Reflexion
A framework that adds a "verbal reinforcement learning" layer.
*   **Mechanism**: When an agent fails a task (e.g., a unit test fails), it generates a text summary of *why* it failed (a "reflection").
*   **Memory**: This reflection is stored in a memory buffer.
*   **Next Attempt**: In the next trial, the agent reads its past reflections to avoid making the same mistake.
*   **Result**: Agents can "learn" to solve hard environments (like AlfWorld) over multiple episodes without updating their weights.

### 3. Chain of Hindsight (CoH)
Training models on a sequence of model outputs paired with feedback.
*   **Idea**: Instead of just RLHF (Good/Bad), give the model explicit feedback: "This summary is good, but it missed the second point. Here is a better version."

## Patterns

### The Critique Loop
1.  **Actor**: Generates a solution.
2.  **Critic**: Evaluates the solution against specific criteria (correctness, style, safety).
3.  **Refiner**: Takes the solution and the critique to produce a better version.
*   *Note*: The Actor, Critic, and Refiner can be the same LLM prompted differently, or different specialized models.

### Constitutional AI (Anthropic)
A form of self-correction used during training.
1.  **Critique**: The model generates a response. A "Constitution" (set of principles) is used to critique the response (e.g., "Is this harmful?").
2.  **Revision**: The model revises the response to align with the constitution.
3.  **Fine-Tuning**: The model is fine-tuned on these revised responses (RLAIF - RL from AI Feedback).

## When to Use
*   **Coding**: "Check your code for bugs."
*   **Math**: "Double check your calculation."
*   **Creative Writing**: "Make the tone more professional."
