# Self-Supervised Learning (SSL)

Learning from unlabeled data by creating "pretext tasks" where the data itself provides the supervision. This is the key to training Foundation Models (LLMs, Vision Models) on internet-scale data.

## 1. Contrastive Learning (SimCLR, CLIP)

*   **Idea**: "These two crops come from the same image, so their vectors should be close. This crop comes from a different image, so push it away."
*   **Result**: The model learns high-level semantic features without needing labels like "Cat" or "Dog".

## 2. Masked Image Modeling (MAE)

*   **Inspired by BERT**: Just as BERT masks words, MAE (Masked Autoencoders) masks 75% of the image patches.
*   **Task**: The model must reconstruct the missing pixels from the visible ones.
*   **Result**: The model learns a deep understanding of visual structures (shapes, textures, objects) to fill in the blanks.

## 3. Next Token Prediction (GPT)

*   **The Ultimate SSL Task**: "Given the text so far, predict the next word."
*   **Why it works**: To predict the next word accurately, the model must eventually learn grammar, facts, reasoning, and sentiment. It is a compression task that forces understanding.

## 4. DINO (Self-Distillation with No Labels)

*   **Teacher-Student**: A Student network tries to match the output of a Teacher network (which is an exponential moving average of the Student).
*   **Emergent Properties**: DINO models automatically learn to segment objects (e.g., separating a bird from the background) without ever being told what an object is.
