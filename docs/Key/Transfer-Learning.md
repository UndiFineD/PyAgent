# Transfer Learning

The practice of storing knowledge gained while solving one problem and applying it to a different but related problem. This is the foundation of the "Pre-training + Fine-tuning" paradigm.

## 1. Types of Transfer

*   **Inductive Transfer**: Same domain, different task. (e.g., ImageNet Pre-training -> Medical X-Ray Classification).
*   **Transductive Transfer**: Different domain, same task. (e.g., Sentiment Analysis trained on Movie Reviews -> Applied to Product Reviews).

## 2. Strategies

*   **Feature Extraction**: Freeze the pre-trained model (the "Backbone") and only train a new "Head" (Classifier) on top.
    *   Fast and requires less data.
*   **Fine-Tuning**: Unfreeze the entire model (or parts of it) and train on the new dataset with a low learning rate.
    *   Better performance but risk of **Catastrophic Forgetting** (forgetting the original knowledge).

## 3. Zero-Shot & Few-Shot Learning

*   **Zero-Shot**: The model can perform a task without seeing *any* examples during training (e.g., CLIP classifying an image as "A photo of a platypus" despite never being explicitly trained on platypus labels).
*   **Few-Shot**: The model learns a new task from just 1-5 examples (e.g., GPT-3 in-context learning).
