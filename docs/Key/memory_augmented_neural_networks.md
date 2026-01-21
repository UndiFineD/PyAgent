# Memory-Augmented Neural Networks (MANNs)

Standard Neural Networks (RNNs, LSTMs) have memory, but it is tied to their hidden state and is transient. MANNs attempt to separate the **computation** (Controller) from the **memory** (External Storage), similar to a CPU and RAM in a classical computer.

## 1. Neural Turing Machines (NTM)

Introduced by DeepMind (Graves et al., 2014), the NTM consists of:
- **Controller**: A neural network (MLP or LSTM) that emits commands.
- **Memory Bank**: A large matrix $M$ of size $N \times W$.
- **Read/Write Heads**: Mechanisms to interact with the memory.

### Differentiable Attention
Crucially, the reading and writing are **differentiable**. The "address" is not a discrete index (like `0x00F1`), but a distribution over all rows.
$$ r_t \leftarrow \sum_i w_t(i) M_t(i) $$
This allows the entire system to be trained end-to-end via backpropagation.

## 2. Differentiable Neural Computers (DNC)

The DNC is an upgrade to the NTM with more sophisticated memory management:
- **Dynamic Memory Allocation**: It tracks which memory slots are "free" and allocates them to new data (like `malloc`).
- **Temporal Linkage**: It stores the order in which data was written, allowing it to iterate through sequences (like a Linked List).

## 3. Sparse Access Memories (SAM)

One issue with NTM/DNC is that reading requires touching *every* memory slot (soft attention), which is $O(N)$.
Newer architectures use **Sparse Attention** (like k-Nearest Neighbors) to access only relevant slots, allowing memory to scale to millions of entries.

## 4. Applications

- **Algorithmic Tasks**: Learning to copy, sort, or traverse graphs.
- **Question Answering**: Storing facts in memory and retrieving them to answer queries (e.g., bAbI tasks).
- **Few-Shot Learning**: Storing examples of a new class in memory to recognize it later without weight updates.

## Summary

MANNs are a step towards "Neural-Symbolic" AI, combining the learnability of neural networks with the persistent, structured storage of classical computers.
