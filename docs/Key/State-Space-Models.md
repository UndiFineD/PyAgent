# State Space Models (SSMs)

Transformers are the dominant architecture in AI, but they have a weakness: **Quadratic Complexity**. The attention mechanism scales as $O(N^2)$ with sequence length. **State Space Models (SSMs)** are a class of architectures designed to solve this, offering $O(N)$ (linear) scaling.

## 1. The Problem with Attention

To generate the next token, a Transformer must look back at *every* previous token.
*   Context Length 10k -> 100M calculations.
*   Context Length 100k -> 10B calculations.
*   This makes "infinite context" computationally impossible for standard Transformers.

## 2. The SSM Solution (Mamba, S4)

SSMs are inspired by Recurrent Neural Networks (RNNs) and Control Theory.
*   **Recurrent Mode (Inference)**: Like an RNN, they maintain a fixed-size "state" ($h_t$) that compresses the history. To generate the next token, they only need the current input and the current state. This is $O(1)$ per step, or $O(N)$ total.
*   **Convolutional Mode (Training)**: Unlike RNNs (which are slow to train because they can't be parallelized), SSMs can be mathematically transformed into a convolution. This allows parallel training on GPUs, just like Transformers.

## 3. Key Architectures

### A. S4 (Structured State Space Sequence)
The foundational paper. It solved the "vanishing gradient" problem of RNNs by using a specific initialization matrix (HiPPO) that allows the model to remember long-range dependencies.

### B. Mamba
The current state-of-the-art.
*   **Selection Mechanism**: Standard SSMs are "time-invariant" (they process every token the same way). Mamba introduces a "Selection Mechanism" that allows the model to selectively remember or ignore information based on the input content.
*   **Hardware Aware**: Mamba is optimized to run efficiently on GPU SRAM (fast memory), minimizing data movement.

## 4. Jamba (Hybrid)

Recent models (like AI21's Jamba) combine layers of Mamba with layers of Attention.
*   **Mamba Layers**: Handle the bulk of the processing and long-term memory efficiently.
*   **Attention Layers**: Provide the "associative recall" (copy-paste) capability that Transformers excel at.
