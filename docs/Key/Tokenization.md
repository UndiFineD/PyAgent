# Tokenization

Tokenization is the fundamental first step in any NLP pipeline. It is the process of converting raw text strings into a sequence of integers (tokens) that a neural network can process.

## 1. Why not characters or words?

*   **Character-level**: Vocabulary is small (ASCII/Unicode), but sequences become incredibly long. "Hello" is 5 tokens. Hard for models to learn long-range dependencies.
*   **Word-level**: Vocabulary becomes massive (millions of words). Out-of-Vocabulary (OOV) words are a huge problem. "Unfriend" might be unknown even if "friend" is known.
*   **Subword-level (The Solution)**: Breaks words into meaningful chunks. "Unfriend" -> "Un" + "friend". Balances vocabulary size (~32k-100k) with sequence length.

## 2. Common Algorithms

### A. Byte-Pair Encoding (BPE)
Used by GPT-2, GPT-3, Llama.
1.  Start with a vocabulary of all individual characters.
2.  Find the most frequent *pair* of adjacent tokens in the training data (e.g., "e" and "s" -> "es").
3.  Merge them into a new token. Add to vocabulary.
4.  Repeat until vocabulary size limit is reached.

### B. WordPiece
Used by BERT. Similar to BPE but selects merges based on *likelihood* rather than just frequency.

### C. SentencePiece
Used by T5, Llama (internally). Treats the input as a raw stream of unicode characters, including spaces. This makes it language-agnostic and robust to messy text (no pre-tokenization splitting by space required).

## 3. Byte-Level BPE
GPT models use a trick: they define the base vocabulary as *bytes* (UTF-8), not unicode characters. This ensures that **any** string can be tokenized without OOV errors, even emojis or binary code.

## 4. Challenges

*   **Tokenization Glitches**: Why can't GPT-4 spell "Lollipop" backwards? Because "Lollipop" might be a single token. The model sees the integer ID, not the letters "L-o-l...".
*   **Math & Numbers**: Numbers are often tokenized inconsistently (e.g., "123" might be one token, "1234" might be "12" + "34"). This makes arithmetic hard for LLMs.
*   **Multilingualism**: A tokenizer trained on English is inefficient for other languages (e.g., representing a Japanese character might take 3-4 byte tokens instead of 1 native token).
