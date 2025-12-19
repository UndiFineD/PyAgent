# GPT Series (Generative Pre-trained Transformer)

## Overview
The **GPT Series** by OpenAI represents the evolution of the **Decoder-only** Transformer architecture, focusing on generative capabilities. It shifted the paradigm from "Fine-tuning" (BERT era) to "Prompting" (In-context Learning).

## Architecture
*   **Decoder-Only**: Uses masked self-attention to ensure the model can only attend to previous tokens (Causal Masking).
*   **Autoregressive**: Predicts the next token based on the history, then feeds that token back in to predict the next one.

## Evolution

### 1. GPT-1 (2018)
*   **Idea**: Pre-train on a large corpus (BooksCorpus) and fine-tune on specific tasks.
*   **Scale**: 117 Million parameters.
*   **Impact**: Showed that generative pre-training works.

### 2. GPT-2 (2019)
*   **Idea**: "Language Models are Unsupervised Multitask Learners".
*   **Scale**: 1.5 Billion parameters.
*   **Impact**: Demonstrated **Zero-Shot** capabilities. It could translate, summarize, and answer questions without any fine-tuning, just by being prompted. Famous for being "too dangerous to release" initially.

### 3. GPT-3 (2020)
*   **Idea**: "Language Models are Few-Shot Learners".
*   **Scale**: 175 Billion parameters (100x larger than GPT-2).
*   **Impact**: Emergent behavior. The model could perform complex tasks (coding, creative writing) given just a few examples in the prompt (**In-Context Learning**). No gradient updates required.

### 4. GPT-3.5 (InstructGPT / ChatGPT - 2022)
*   **Idea**: Alignment. Raw GPT-3 was unruly and often toxic.
*   **Technique**: **RLHF** (Reinforcement Learning from Human Feedback). Trained to follow instructions and be helpful/harmless.
*   **Impact**: The "ChatGPT moment". AI became accessible to the general public.

### 5. GPT-4 (2023)
*   **Idea**: Scale + Multimodality + Reasoning.
*   **Scale**: Estimated ~1.8 Trillion parameters (likely Mixture of Experts).
*   **Impact**: Human-level performance on professional benchmarks (Bar Exam, SAT). Can process images and text.

## Scaling Laws
The GPT series proved the **Scaling Laws**: Performance improves predictably as you increase:
1.  Compute
2.  Dataset Size
3.  Parameter Count
