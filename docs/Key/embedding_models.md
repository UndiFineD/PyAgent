# Embedding Models

## Overview
**Embedding Models** are the bridge between raw data (text, images, audio) and the mathematical world of vectors. They convert discrete inputs into continuous, high-dimensional vectors where semantic similarity is preserved (similar concepts are close in space).

## Evolution of Text Embeddings

### 1. Static Embeddings (2013-2017)
*   **Word2Vec (Google)**: Learned vector representations for words by predicting surrounding words (Skip-gram/CBOW).
    *   *Limitation*: "Bank" has the same vector in "River bank" and "Bank account". Context-independent.
*   **GloVe (Stanford)**: Global Vectors. Based on matrix factorization of word co-occurrence counts.
*   **FastText (Facebook)**: Uses subword information (n-grams) to handle out-of-vocabulary words.

### 2. Contextual Embeddings (2018-Present)
*   **ELMo**: Uses LSTM to generate embeddings based on the full sentence context.
*   **BERT**: Uses Transformers. The embedding for "Bank" changes depending on the sentence.

### 3. Sentence Embeddings
Standard BERT gives embeddings for *tokens*. To get an embedding for a whole *sentence*, we need pooling.
*   **Sentence-BERT (SBERT)**: A modification of BERT that uses Siamese networks to derive semantically meaningful sentence embeddings that can be compared using Cosine Similarity.
*   **OpenAI `text-embedding-3`**: The current industry standard for RAG. High performance, variable dimensions.
*   **MTEB Leaderboard**: Massive Text Embedding Benchmark. Tracks the best models (e.g., E5, BGE, Cohere).

## Multimodal Embeddings
*   **CLIP (OpenAI)**: Maps text and images to the same vector space. "A photo of a dog" and an image of a dog have high cosine similarity.

## Key Properties
*   **Dimensions**: The size of the vector (e.g., 768, 1536, 3072). Higher dimension = more nuance but higher storage cost.
*   **Matryoshka Embeddings**: Models trained so that the first $n$ dimensions contain the most important information. Allows truncating vectors to save space with minimal accuracy loss.
