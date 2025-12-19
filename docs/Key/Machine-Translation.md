# Machine Translation (NMT)

## What is Machine Translation?
Machine Translation (MT) is the subfield of computational linguistics focused on translating text or speech from one language to another. Modern systems are primarily **Neural Machine Translation (NMT)**, which use deep neural networks to learn the mapping between languages.

## Evolution of MT
1.  **Rule-Based MT (RBMT)**: (1970s-1990s) Relied on explicit linguistic rules and dictionaries. Very rigid and failed on idioms.
2.  **Statistical MT (SMT)**: (1990s-2010s) Used statistical models (like n-grams) to find the most probable translation based on huge parallel corpora. (e.g., early Google Translate).
3.  **Neural MT (NMT)**: (2014-Present) Uses a single large neural network to translate end-to-end.

## Core Architecture: Sequence-to-Sequence (Seq2Seq)
NMT relies on the **Encoder-Decoder** architecture:
1.  **Encoder**: Reads the input sentence (source language) and compresses it into a fixed-length "context vector" or a sequence of hidden states.
2.  **Decoder**: Takes the context vector and generates the output sentence (target language) one word at a time.

### The Role of Attention
Early Seq2Seq models (using RNNs/LSTMs) struggled with long sentences because the entire meaning had to be compressed into a single vector.
**Attention Mechanisms** solved this by allowing the Decoder to "look back" at specific parts of the input sentence relevant to the current word being generated.
*   *Example*: When generating the French word "pomme", the model attends strongly to the English word "apple".

### The Transformer Revolution
The **Transformer** architecture (2017) replaced RNNs entirely, allowing for parallel processing and better handling of long-range dependencies. Most modern NMT systems (Google Translate, DeepL) are Transformer-based.

## Key Concepts
*   **Parallel Corpora**: Datasets containing sentence pairs in two languages (e.g., English-French) used for training.
*   **Back-Translation**: A data augmentation technique where a model translates target text *back* to the source language to create synthetic training data.
*   **Beam Search**: An algorithm used during inference to explore multiple possible translations and choose the most likely sequence, rather than just picking the single best word at each step (Greedy Decoding).

## Evaluation Metrics
*   **BLEU (Bilingual Evaluation Understudy)**: Measures the overlap of n-grams between the machine translation and one or more human reference translations. Higher is better.
*   **METEOR**: Considers synonyms and stemming, often correlating better with human judgment than BLEU.
*   **COMET / BLEURT**: Neural-based metrics that use embeddings to assess semantic similarity, not just exact word matches.

## Challenges
*   **Low-Resource Languages**: Languages with very little parallel training data.
*   **Idioms and Cultural Nuance**: Literal translations often fail to capture the intended meaning.
*   **Gender Bias**: Models may default to stereotypes (e.g., translating "doctor" as male and "nurse" as female) when the source language is gender-neutral.
