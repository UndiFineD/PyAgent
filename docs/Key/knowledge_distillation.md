# Knowledge Distillation

Knowledge Distillation (KD) is a compression technique where a small "Student" model learns to mimic the behavior of a large "Teacher" model. It is one of the primary ways to create efficient models for mobile devices or real-time applications.

## 1. How it Works

Standard training uses "Hard Labels" (Ground Truth).
*   Image: Dog. Label: `[0, 1, 0]` (Cat, Dog, Bird).
*   The model is punished if it predicts anything other than 100% Dog.

Distillation uses "Soft Labels" (Teacher's Output).
*   Teacher (GPT-4) Output: `[0.05, 0.90, 0.05]`.
*   The Teacher says: "It's definitely a dog, but it looks 5% like a cat and 5% like a bird."
*   **Dark Knowledge**: This 5% uncertainty contains valuable information about the *relationship* between classes (cats look more like dogs than cars do). The Student learns this rich structure.

## 2. Types of Distillation

*   **Response-Based**: The Student tries to match the final output logits of the Teacher. (KL Divergence Loss).
*   **Feature-Based**: The Student tries to match the *intermediate* activation layers of the Teacher. This forces the Student to "think" like the Teacher, not just give the same answers.
*   **Relation-Based**: The Student tries to match the relationships between examples (e.g., if Image A and Image B are similar in the Teacher's view, they should be similar in the Student's view).

## 3. Distillation in LLMs

*   **White-Box Distillation**: You have access to the Teacher's weights/logits. (Rare for proprietary models like GPT-4).
*   **Black-Box Distillation (Model Imitation)**: You only have the Teacher's text output.
    *   You generate 1M questions.
    *   You ask GPT-4 to answer them.
    *   You Fine-Tune Llama-7B on these (Question, Answer) pairs.
    *   *Note*: This is technically "Supervised Fine-Tuning on Synthetic Data," but often called distillation in the LLM context.

## 4. The "Model Collapse" Risk

If you train a Student on a Teacher, then train a new Student on that Student, and repeat... the quality degrades. The models lose the "tails" of the distribution (rare knowledge) and converge to the average.
