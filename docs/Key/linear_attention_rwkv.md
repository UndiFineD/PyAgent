# Linear Attention & RWKV

The standard Transformer has a fatal flaw: **Quadratic Complexity** $O(N^2)$. Doubling the context length quadruples the compute and memory. Linear Attention architectures aim to fix this, achieving $O(N)$ complexity while maintaining Transformer-level performance.

## 1. The "RNN Strikes Back"

Standard RNNs (LSTMs) are $O(N)$ because they process tokens one by one, updating a fixed-size hidden state.
- **Pros**: Infinite context length (in theory), fast inference, low memory.
- **Cons**: Cannot be parallelized during training (must wait for step $t-1$ to compute step $t$).

**Linear Transformers** (like RWKV, Mamba, RetNet) try to get the best of both worlds:
- **Training**: Parallelizable like a Transformer.
- **Inference**: Recurrent like an RNN.

## 2. RWKV (Receptance Weighted Key Value)

RWKV is the most successful open-source project in this category.

### Architecture
It modifies the attention mechanism to be "linearizable."
$$ wkv_t = \frac{\sum_{i=1}^{t-1} e^{-(t-1-i)w + k_i} v_i}{\sum_{i=1}^{t-1} e^{-(t-1-i)w + k_i}} $$
This looks like attention (weighted sum of values), but because the decay $w$ is constant, it can be computed recurrently.
- **State**: Instead of keeping the full history of Key/Value pairs (KV Cache), RWKV keeps a single "state" vector that accumulates the information.

## 3. Linear Attention (Katharopoulos et al.)

Standard Attention:
$$ \text{Softmax}(QK^T)V $$
The Softmax prevents us from multiplying $K^T V$ first.
Linear Attention replaces Softmax with a kernel function $\phi(\cdot)$ that allows associativity:
$$ (\phi(Q) \phi(K)^T) V = \phi(Q) (\phi(K)^T V) $$
Now we can compute $\phi(K)^T V$ once (a matrix) and update it incrementally.

## 4. Trade-offs

| Feature | Transformer | RWKV / Linear Attention |
| :--- | :--- | :--- |
| **Complexity** | $O(N^2)$ | $O(N)$ |
| **In-Context Learning** | Excellent (Recall perfect copy) | Good, but "leaky" (State capacity is finite) |
| **Training Speed** | Fast (Parallel) | Fast (Parallel) |
| **Inference Memory** | Grows with context (KV Cache) | Constant (Fixed State) |

## Summary

Linear Architectures are crucial for **Edge AI** and **Long-Context** applications where the quadratic cost of standard Transformers is prohibitive.
