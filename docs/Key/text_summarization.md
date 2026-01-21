# Text Summarization

## What is Text Summarization?
Text Summarization is the task of producing a concise and fluent summary of a longer text document while preserving its key information and overall meaning.

## Two Main Approaches

### 1. Extractive Summarization
This approach works by **selecting** a subset of existing sentences or phrases from the original text to form the summary. It does not generate new words.
*   **Mechanism**: It scores sentences based on importance (e.g., using TF-IDF, graph-based ranking like TextRank, or BERT embeddings) and picks the top N sentences.
*   **Pros**: Factually safer (harder to hallucinate), grammatically correct (assuming source is).
*   **Cons**: Can feel disjointed; lacks flow; cannot synthesize information from multiple parts of the text into a new sentence.

### 2. Abstractive Summarization
This approach **generates** new sentences that capture the essence of the original text, similar to how a human would write a summary.
*   **Mechanism**: Uses Seq2Seq models (like BART, T5, Pegasus, or GPT-4) to understand the input and write a new output.
*   **Pros**: More natural, fluent, and concise; can paraphrase and synthesize.
*   **Cons**: Prone to **hallucination** (making up facts not in the source); computationally more expensive.

## Key Models
*   **BERT (Extractive)**: Can be used to score sentence importance (BERTSum).
*   **BART (Bidirectional and Auto-Regressive Transformers)**: A denoising autoencoder excellent for abstractive summarization.
*   **T5 (Text-to-Text Transfer Transformer)**: Frames summarization as a "summarize: [text]" task.
*   **Pegasus**: Specifically pre-trained for summarization using "Gap Sentence Generation" (masking out whole sentences and trying to generate them).

## Evaluation Metrics
*   **ROUGE (Recall-Oriented Understudy for Gisting Evaluation)**: The standard metric for summarization. It measures the overlap of n-grams between the generated summary and human-written reference summaries.
    *   **ROUGE-N**: Overlap of N-grams (ROUGE-1, ROUGE-2).
    *   **ROUGE-L**: Longest Common Subsequence.
*   **BERTScore**: Uses contextual embeddings to measure similarity, capturing meaning better than exact word overlap.

## Challenges
*   **Factuality**: Ensuring the summary doesn't contradict the source or add false details.
*   **Length Control**: Generating a summary of a specific desired length.
*   **Long Documents**: Summarizing entire books or long reports is difficult due to the context window limits of many models (though models like Claude 3 and Gemini 1.5 are solving this).
