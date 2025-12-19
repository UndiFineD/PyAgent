# BERT (Bidirectional Encoder Representations from Transformers)

## Overview
**BERT** (2018) is a landmark model by Google that revolutionized Natural Language Processing (NLP). It demonstrated that a Transformer **Encoder** could be pre-trained on a massive amount of unlabeled text and then fine-tuned for specific tasks, achieving state-of-the-art results.

## Architecture
*   **Encoder-Only**: BERT uses only the Encoder stack of the Transformer. It does not generate text (it's not a chatbot); it *understands* text.
*   **Bidirectional**: Unlike GPT (which reads left-to-right), BERT reads the entire sequence at once. It can see the context from both the left and right of a token simultaneously.

## Pre-Training Objectives

### 1. Masked Language Modeling (MLM)
*   **The Task**: Randomly mask 15% of the tokens in the input and ask the model to predict the missing words.
*   **Example**: "The [MASK] sat on the mat." -> Model predicts "cat".
*   **Why**: Forces the model to understand context and relationships between words.

### 2. Next Sentence Prediction (NSP)
*   **The Task**: Given two sentences A and B, predict if B follows A in the original text.
*   **Why**: Helps the model understand relationships between sentences (crucial for QA and NLI).

## Fine-Tuning
After pre-training, BERT is fine-tuned on downstream tasks by adding a small classification layer on top:
*   **Sentiment Analysis**: [CLS] token -> Positive/Negative.
*   **Named Entity Recognition**: Token -> Person/Location/Org.
*   **Question Answering (SQuAD)**: Predicting the start and end span of the answer in a passage.

## Variants
*   **RoBERTa (Facebook)**: "Robustly Optimized BERT". Removed NSP, trained longer on more data. Better performance.
*   **DistilBERT (Hugging Face)**: A smaller, faster, cheaper version of BERT (40% smaller, 60% faster, 97% performance).
*   **DeBERTa (Microsoft)**: Disentangled Attention. Current SOTA for many NLU tasks.
