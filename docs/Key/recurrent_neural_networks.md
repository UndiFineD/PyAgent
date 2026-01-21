# Recurrent Neural Networks (RNNs)

## What is an RNN?
A Recurrent Neural Network (RNN) is a type of neural network designed for sequential data (Time Series, Text, Audio). Unlike Feedforward networks, RNNs have a "data/memory" (hidden state) that captures information about what has been calculated so far.

## The Loop
In a standard neural network, inputs are independent. In an RNN, the output of step $t-1$ is fed back into the network as input for step $t$.
*   *Analogy*: Reading a sentence word by word. You understand the current word based on the context of the previous words you just read.

## The Problem: Vanishing Gradients
Standard RNNs struggle with long sequences. As the error signal is backpropagated through time (BPTT), it gets multiplied by the weights repeatedly.
*   If weights < 1, the gradient vanishes to zero (model stops learning).
*   If weights > 1, the gradient explodes (instability).
*   *Result*: Basic RNNs "forget" information from the beginning of a long sentence.

## The Solution: Gated Architectures

### 1. LSTM (Long Short-Term Memory)
*   Introduced by Hochreiter & Schmidhuber (1997).
*   Uses a complex cell with three "gates" to control information flow:
    *   **Forget Gate**: What to throw away from memory.
    *   **Input Gate**: What new information to store.
    *   **Output Gate**: What to output at this step.
*   This allows LSTMs to maintain dependencies over thousands of steps.

### 2. GRU (Gated Recurrent Unit)
*   A simplified version of LSTM (2014).
*   Combines the Forget and Input gates into a single "Update Gate."
*   Faster to train and often performs just as well.

## Legacy
While **Transformers** have largely replaced RNNs/LSTMs for NLP because Transformers can process the whole sequence in parallel (Attention), RNNs are still useful for:
*   Real-time streaming data (where you don't have the future context).
*   Low-power devices (smaller memory footprint than Attention).
